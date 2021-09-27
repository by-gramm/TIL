# [django] redirect

## redirect()

`redirect(to, *args, permanent=False, **kwargs)`

> 주어진 인자에 알맞은 URL로 HttpResponseRedirect을 리턴한다.

- 인자로는 절대 경로가 주어질 수도 있고, 상대 경로가 주어질 수도 있다.

- 내부적으로는 `resolve_url()`을 사용한다.

- 주로 `urls.py`에 `app_name`을 지정하고, 해당 이름을 통해 탐색하는 방식을 사용한다.

- 사용 예시

```python
# accounts/urls.py

from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
	path('login/', views.login, name='login')
]
```

```python
# books/views.py

from django.shortcuts import redirect

def func(request):
    (중략)
    if request.user.is_authenticated:
        # 절대 경로 사용 => "https://www.naver.com"으로 이동
    	return redirect('https://www.naver.com')
    # 상대 경로 사용 => accounts 앱의 login 이름을 가진 url로 이동
    return redirect('accounts:login')
```

<br>

## render와의 비교

`render(request, template_name, context=None, content_type=None, status=None, using=None)`

> 주어진 템플릿과 context를 결합하여, HttpResponse 객체를 리턴한다.

- 사용 예시

```python
def index(request):
    books = Book.objects.all()
    
    context = {
        'books': books,
    }
    
    return render(request, 'books/index.html', context)
```

- `render`는 우리가 요청한 페이지를 템플릿과 문맥을 결합하여 리턴한다.
- `redirect`는 특정한 URL로 요청을 보낸다. 예를 들어, `redirect('accounts:login')`로 redirect하면, accounts 앱의 login 이름을 가진 URL로 이동하고, 이 URL에 연결된 `accounts/views.py`의 함수가 다시 실행된다.

<br>

## 방금 작성한 글의 상세 페이지로 redirect하기

함수 기반 뷰를 사용하여 books 앱의 CRUD 기능을 구현한다고 하자. Update 기능을 구현할 때는 우선 수정하려는 게시물 인스턴스를 받아온다. 그래서 게시물을 수정한 이후, 해당 게시물의 상세 페이지로 바로 이동할 수 있다.

```python
# books/urls.py

app_name = 'books'

urlpatterns = [
    path('<int:pk>/', views.detail, name='detail'),
]
```

```python
# books/views.py

def update(request, pk):
    # pk를 통해 수정하고자 하는 게시물을 가져온다.
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)

        if form.is_valid():
            # 게시물을 수정한 이후
            form.save()
            # 수정한 게시물로 리다이렉트한다.
            return redirect('books:detail', book.pk)
        
    (중략)
```

그런데 Create 기능, 다시 말해 게시물을 처음 작성하는 경우에는 미리 해당 게시물을 가져올 수 없다. 게시물을 생성하기 전에는 게시물 자체가 없기 때문이다. 그렇다면 어떻게 방금 작성한 글의 상세 페이지로 redirect할 수 있을까?

```python
# books/views.py

def create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)

        if form.is_valid():
            # 글을 생성하긴 했는데
            form.save()
            # 어떻게 방금 생성한 글로 리다이렉트하지?
    
    (중략)
```

`save()` 메서드는 form이 저장한 model의 인스턴스를 반환한다. `form.save()`를 통해 새로운 게시물을 생성했다면, 해당 게시물을 리턴한다는 것이다. 그래서 아래와 같이 방금 생성한 게시물을 받아온 뒤, 접근할 수 있다. 

```python
def create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)

        if form.is_valid():
            # 글을 생성하고, 방금 생성한 글을 book 변수에 저장한다.
            book = form.save()
            # book의 pk를 통해 방금 생성한 글로 redirect한다.
            return redirect('books:detail', book.pk)
    
    (중략)
```

<br>

+) `save()` 메서드의 다음과 같은 성질을 활용하여, 회원가입 후 자동 로그인 기능도 구현할 수 있다.

```python
# accounts/views.py

from django.contrib.auth import login as auth_login

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            # 회원가입 후, 해당 유저 정보를 user 변수에 저장한다.
            user = form.save()
            # user 변수를 활용하여, 방금 가입한 유저를 로그인시킨다.
            auth_login(request, user)
            
    (중략)
```

<br>

## 로그인 후 원래 요청한 페이지로 리다이렉트하기

글을 수정하는 페이지에 접근했는데, 로그인이 되어 있지 않아서 로그인 페이지로 redirect된 경우를 생각해보자. 이때 로그인을 완료한 후, 권한이 있다면 원래 요청한 수정 페이지로 바로 redirect해주면 좋을 것이다. 

`next` 쿼리 스트링 인자가 이를 가능하게 한다. `next` 인자는 로그인이 성공한 이후, 이동할 페이지를 나타낸다. 예를 들어, 글 수정 페이지로 요청을 보냈는데 로그인 페이지로 redirect된 경우, URL은 아래와 같다.

```bash
https://bookgram.com/accounts/login/?next=/book/update/
```

그래서 login 함수에서 로그인 성공 후 next 쿼리문이 나타내는 URL로 redirect를 하게 하면, 로그인 후 원래 요청한 페이지로 redirect해줄 수 있다.

```python
# accounts/views.py

from django.contrib.auth import login as auth_login

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)

        if form.is_valid():
            # 로그인을 시킨 후
            auth_login(request, form.get_user())
            # next 인자가 있다면 해당 인자가 가리키는 URL로 리다이렉트한다.
            # next 인자가 없다면 books 앱의 index 페이지로 리다이렉트한다.
            return redirect(request.GET.get('next') or 'books:index')
```

<br>

### 참고 출처

[Django 공식 문서 - Django shortcut functions](https://docs.djangoproject.com/en/3.2/topics/http/shortcuts/)

https://stackoverflow.com/questions/39930414/what-is-the-difference-render-and-redirect-in-django
