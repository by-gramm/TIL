# httpOnly 쿠키에 refresh token 저장하기


### ✅ simplejwt의 인증 방식

- `TokenObtainPairView` : 전달 받은 유저 인증 정보가 유효한 경우, `access_token` 값과 `refresh_token` 값을 반환한다. 
- `TokenRefreshView` : `refresh_token`을 전달 받아, 유효한 토큰인 경우 새로운 `access_token`을 반환한다. 

현재 Django REST Framework를 활용하는 프로젝트에서 `dj_rest_auth`와 `simplejwt`를 통해 인증을 처리하고 있다.  인증 과정을 client와 server를 기준으로 정리하면 아래와 같다.

1. 유저가 이메일 및 비밀번호 값을 입력한 뒤 로그인을 시도한다.
2. client는 유저가 입력한 `email`, `password` 정보를 담은 요청을 server의 `TokenObtainPairView`에 보낸다.
3. `TokenObtainPairView`에서 받은 유저 인증 정보가 유효하다면, `access_token` 값과 `refresh_token` 값이 리턴된다.
4. server는 `access_token`과 `refresh_token` 정보를 client에 전달한다.
5. client는 전달받은 `access_token` 및 `refresh_token` 정보를 저장한다.
6. 이후 client에서는 인증이 필요한 요청을 server에 보낼 때마다 `access_token` 정보를 함께 보낸다.
7. `access_token`의 유효 기간이 만료된 경우, client는 `refresh_token` 정보를 담은 요청을 `TokenRefreshView`에 보낸다.
8. 해당 토큰 정보가 유효하다면, 새로 갱신된 `access_token` 정보가 리턴된다.

이번 글에서 주목하고자 하는 부분은 토큰 정보를 저장하는 5번이다.

<br>

### 💾 토큰 정보 저장하기 (httpOnly 쿠키)

토큰 정보를 저장하는 방법 중 제일 구현하기 쉬운 것은 **localStorage**에 저장하는 것이다. 하지만 localStorage에 저장한 정보는 JS에서 접근이 가능하다. 따라서 client 브라우저에 Javascript 코드를 삽입해 공격하는 **XSS 공격**에 취약하다.

다음으로 생각할 수 있는 방법은 토큰 정보를 **쿠키**에 저장하는 것이다. 하지만 이 또한 JS에서 접근이 가능해서, 마찬가지로 XSS 공격에 취약하다.

XSS 공격에 대비하기 위해서는, 토큰 정보를 **httpOnly 쿠키**에 저장해야 한다. httpOnly 쿠키의 경우 JS에서 접근이 불가능하기 때문에, XSS 공격 방어가 가능하다.

하지만 `access_token` 정보의 경우, httpOnly 쿠키에 저장하더라도 여전히 위험하다. 유저의 인증 정보를 바탕으로 사이트를 공격하는 **CSRF 공격**의 위험이 있기 때문이다.

따라서, XSS 공격과 CSRF 공격을 대비하기 위해서

- `access_token` 정보는 Javascript 로컬 변수로 저장하고,

- `refresh_token` 정보는 httpOnly 쿠키에 저장하기로 한다.

(토큰 저장에 대한 보다 자세한 설명은 [다음 링크](https://velog.io/@yaytomato/%ED%94%84%EB%A1%A0%ED%8A%B8%EC%97%90%EC%84%9C-%EC%95%88%EC%A0%84%ED%95%98%EA%B2%8C-%EB%A1%9C%EA%B7%B8%EC%9D%B8-%EC%B2%98%EB%A6%AC%ED%95%98%EA%B8%B0#-%EB%B3%B4%EC%95%88%EC%9D%80-%EC%96%B4%EB%96%BB%EA%B2%8C-%EB%9A%AB%EB%A6%AC%EB%82%98)를 참고하면 좋을 것이다.)

<br>

### 🍪 simplejwt에서 httpOnly 쿠키 사용하기

`access_token`을 Javascript 로컬 변수로 저장하는 것은 frontend의 역할이다. backend에서는 `refresh_token`을 httpOnly 쿠키에 담아 보내주면 된다.

이제 simplejwt에서 `refresh_token`을 httpOnly 쿠키에 담아 보내는 방법을 알아보자.

`TokenObtainPairView`에서는 원래 아래와 같이 토큰 정보를 응답한다.

```json
data: {
    "access_token": "1234567812345678.asdfghjkasdfghjk.12341234...",
    "refresh_token": "1234567812345678.asdfghjkasdfghjk.12341234...",
    "user": {
        "pk": 1,
        "email": "abcdefg@naver.com"
    }
}
```

그런데 지금은 client에 응답을 보낼 때, `access_token`만 data에 담아 보내고, `refresh_token`은 httpOnly 쿠키에 담아 보내고자 한다. 

이를 위해서는, `TokenObtainPairView`를 상속받은 커스텀 View에서 `refresh_token`을 httpOnly 쿠키에 추가하고, 응답 데이터에서는 지워주면 된다. (`TokenRefreshView`도 같은 방식으로 구현하면 된다.)

```python
# views.py
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import InvalidToken

class CookieTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = None
    def validate(self, attrs):
        attrs['refresh'] = self.context['request'].COOKIES.get('refresh_token')
        if attrs['refresh']:
            return super().validate(attrs)
        else:
            raise InvalidToken('No valid token found in cookie \'refresh_token\'')

class CookieTokenObtainPairView(TokenObtainPairView):
  def finalize_response(self, request, response, *args, **kwargs):
    if response.data.get('refresh'):
        cookie_max_age = 3600 * 24 * 14 # 14 days
        response.set_cookie('refresh_token', response.data['refresh'], max_age=cookie_max_age, httponly=True )
        del response.data['refresh']
    return super().finalize_response(request, response, *args, **kwargs)

class CookieTokenRefreshView(TokenRefreshView):
    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get('refresh'):
            cookie_max_age = 3600 * 24 * 14 # 14 days
            response.set_cookie('refresh_token', response.data['refresh'], max_age=cookie_max_age, httponly=True )
            del response.data['refresh']
        return super().finalize_response(request, response, *args, **kwargs)
    serializer_class = CookieTokenRefreshSerializer
```

```python
# url.py

from .views import CookieTokenRefreshView, CookieTokenObtainPairView 

urlpatterns = [
    # url 주소는 원하는 대로 지정 가능
    path('auth/token/', CookieTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
    ...
]
```

<br>

### 🔑 dj_rest_auth 로그인과 결합하기

현재 프로젝트에서 `TokenRefreshView`의 경우 위 방식을 그대로 사용할 수 있었다. 하지만 `TokenObtainPairView`에서는 그럴 수 없었다. 로그인 시 `TokenObtainPairView`에 직접 요청을 보내지 않기 때문이다.

대신 `dj_rest_auth` 라이브러리의 로그인 API로 요청을 보내면, 해당 API에서 `TokenObtainPairView`로 다시 요청을 보내 인증을 처리한다. 그렇기 때문에 `TokenObtainPairView`를 커스텀하더라도, 여전히 로그인을 하면 기존`TokenObtainPairView`로 요청을 보내게 된다. 따라서 현재의 로그인 방식에서 httpOnly 쿠키를 활용하려면, `dj_rest_auth`의 로그인 View 자체를 커스텀해야 한다.

코드를 뒤져보니 `dj_rest_auth`에서 토큰 정보를 리턴하는 곳은 `LoginView` 내의 `get_response` 메소드였다. ([소스 코드](https://github.com/iMerica/dj-rest-auth/blob/eeaaab44845723d1eff51fc4dcdf2b6d7e7f0f10/dj_rest_auth/views.py#L82)) 그래서 `LoginView`를 상속받은 커스텀 View를 정의한 뒤, `get_response` 메소드에 `refresh_token`을 httpOnly 쿠키에 추가하고, 응답 데이터에서는 지우는 코드를 추가했다.

```python
class CustomLoginView(LoginView):
    def get_response(self):
        # response에 토큰 정보를 담는 기존 코드 부분 (83 ~ 115줄)

        # refresh token을 httpOnly cookie로 저장하기 위해 커스텀한 부분
        if response.data.get('refresh_token'):
            cookie_max_age = 3600 * 24 * 30  # 30일
            response.set_cookie('refresh_token', response.data['refresh_token'], max_age=cookie_max_age, httponly=True )
            del response.data['refresh_token']

        if getattr(settings, 'REST_USE_JWT', False):
            set_jwt_cookies(response, self.access_token, self.refresh_token)
        return response
```

이를 통해 `refresh_token` 정보를 httpOnly 쿠키에 담아서 보낼 수 있었다.

<br>

### 참고 출처

[Velog - 프론트에서 안전하게 로그인 처리하기 (ft. React)](https://velog.io/@yaytomato/%ED%94%84%EB%A1%A0%ED%8A%B8%EC%97%90%EC%84%9C-%EC%95%88%EC%A0%84%ED%95%98%EA%B2%8C-%EB%A1%9C%EA%B7%B8%EC%9D%B8-%EC%B2%98%EB%A6%AC%ED%95%98%EA%B8%B0#-%EB%B3%B4%EC%95%88%EC%9D%80-%EC%96%B4%EB%96%BB%EA%B2%8C-%EB%9A%AB%EB%A6%AC%EB%82%98)

[StackOverFlow - Where to store the refresh token on the Client?](https://stackoverflow.com/questions/57650692/where-to-store-the-refresh-token-on-the-client)

[simplejwt Github - Issue71 (Allow httpOnly cookie storage)](https://github.com/jazzband/djangorestframework-simplejwt/issues/71.Is)

[dj_rest_auth 라이브러리 소스 코드](https://github.com/iMerica/dj-rest-auth)

