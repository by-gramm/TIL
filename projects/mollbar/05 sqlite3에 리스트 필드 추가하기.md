# sqlite3에 리스트 필드 추가하기

### 배경 : 영화 데이터에 감독/배우 정보 추가하기

1번 글에서  TMDB API를 통해 영화 데이터를 가져와서, DB에 저장하는 방법을 살펴보았다. 

이번에는 영화 데이터를 가져오되, 감독과 배우 정보를 추가로 가져오기로 했다. 그런데 인기순으로 영화 정보를 가져오는 API에는 감독/배우의 정보는 없었다. 감독/배우 정보는 독립된 API를 통해서 정보를 가져올 수 있었다.

그래서 일단 인기순으로 영화 정보를 가져온 뒤, 각 영화의 id로 감독/배우 정보 API에 다시 요청을 보내 정보를 하나씩 추가했다.

```python
def get_movie_datas():
    total_data = []
    BASE_URL = "https://api.themoviedb.org/3/movie/"

    # 1페이지부터 500페이지까지 (총 10,000개)
    for i in range(1, 501):
        request_url = f"{BASE_URL}popular?api_key={TMDB_API_KEY}&language=ko-KR&page={i}"
        movies = requests.get(request_url).json()
        
        for movie in movies['results']:
            # 개봉 날짜가 있는 영화의 데이터만 추가한다.
            if movie.get('release_date', ''):

                fields = {
                    'movie_id': movie['id'],
                    'title': movie['title'],
                    ...
                    'director': '',
                    'actors': [],
                }
                
                data = {
                    "pk": movie['id'],
                    "model": "movies.movie",
                    "fields": fields
                }

                total_data.append(data)
    
    # 감독/배우 정보가 있는 경우, 추가로 받아온다.
    for data in total_data:
        movie_id = data['fields']['movie_id']
        
        credit_request_url = f"{BASE_URL}{movie_id}/credits?api_key={TMDB_API_KEY}"
        credit_info = requests.get(credit_request_url).json()

        # 배우는 최대 10명까지만 저장한다.
        for cast in credit_info['cast'][:10]:
            data['fields']['actors'].append(cast['name'])
        
        if credit_info['crew']:
            data['director'] = credit_info['crew'][0]['name']

    with open("movie_data3.json", "w", encoding="utf-8") as w:
        json.dump(total_data, w, indent="\t", ensure_ascii=False)

get_movie_datas()
```

시간이 아주 오래 걸리긴 했지만, 무사히 정보를 받아올 수 있었다.

<br>

### 문제 : sqlite3에 리스트 필드 추가하기

이제 영화 데이터 필드에 `director`와 `actors`가 추가되었으므로, Movie 모델에도 두 필드를 추가해야 한다. `director`는 감독 1명의 이름이므로 간단하게 `CharField`로 추가했다. 문제는 `actors`였다. 

`actors`는 배열 안에 여러 배우들의 이름이 문자열로 담겨 있다. 따라서 리스트를 담을 수 있는 필드가 필요하다. 그런데 PostgreSQL의 경우 리스트를 담을 수 있는 `ArrayField`를 지원하지만, sqlite3에는 `ArrayField`가 없다.

<br>

### 해결 : JSONField 활용

다행히도 Django 3.1부터 (원래는 Postgresql로만 사용 가능하던) `JSONField`를 다른 DB에서도 사용할 수 있게 되었다. 

Django 공식 문서에 따르면, sqlite3에서 `JSONField`를 사용하려면 JSON1 extension을 enable해야 한다. (JSON1 extension을 enable하는 방법은 [다음 링크](https://code.djangoproject.com/wiki/JSON1Extension)에서 볼 수 있다.)

해당 링크에 따르면 macOS에서는 python 3.7부터, Windows에서는 python 3.9부터 JSON1 extension을 기본으로 지원한다고 한다. 나의 경우 Windows 운영체제를 사용 중이며, python 3.9 버전을 사용 중이기 때문에, 별도의 설정 없이 바로 `JSONField`를 이용할 수 있었다.

```python
# movies/models.py

class Movie(models.Model):
    movie_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=100)
    ...
    actors = models.JSONField(null=True)
    director = models.CharField(max_length=100, null=True)
```

<br>


### 참고 출처

https://docs.djangoproject.com/en/3.1/ref/models/fields/#django.db.models.JSONField

https://docs.djangoproject.com/en/3.2/ref/databases/

https://code.djangoproject.com/wiki/JSON1Extension