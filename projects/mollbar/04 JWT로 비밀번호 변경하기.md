# JWT로 비밀번호 변경하기

### 상황 분석

비밀번호 변경은 크게 아래의 순서로 이루어진다.

1. `기존 비밀번호`, `새 비밀번호`, `새 비밀번호 확인`을 입력받는다.

2. 아래의 3가지 조건이 만족된다면 비밀번호를 변경한다.

   - `기존 비밀번호`가 로그인한 유저의 비밀번호와 일치함.
   
   - `새 비밀번호`와 `새 비밀번호 확인`에 입력한 값이 일치함.
   
   - `새 비밀번호`가 비밀번호로서 유효함.
   
3. 유저를 로그인 페이지로 이동시키거나, 새 비밀번호로 자동 로그인시킨다.

<br>

### 문제 1 - 기존 비밀번호 일치 여부 판단

문제는 `기존 비밀번호`의 값을 직접 알 방법이 없다는 점이다. 보안을 위해 회원가입 시 유저의 비밀번호는 해시 함수로 암호화한 상태로 저장되기 때문이다. 단방향이기 때문에 원본을 알 수 없는 해시 함수의 특성 때문에, 원본 비밀번호를 넣어 맞는지 확인할 수는 있지만, 반대로 암호화된 값으로부터 원본 비밀번호를 구할 수는 없다. 

따라서 사용자가 입력한 `기존 비밀번호`가 유효한지 확인하기 위해, client에서 로그인 URL에 현재 로그인한 유저의 username과 사용자가 입력한 `기존 비밀번호`를 담은 요청을 보내서 확인하도록 구현했다. 이 요청에서 오류가 발생한다면 `기존 비밀번호`가 틀린 것이고, 응답이 잘 온다면 `기존 비밀번호`가 맞는 것이다.

```javascript
axios({
  method: 'post',
  url: <<LOGIN_URL>>,
  data: {
    'username': <<현재 로그인 유저의 username>>,
    'password': <<사용자가 입력한 기존 비밀번호>>
  }
})
  .then(res => ...)   // 이후 필요한 작업을 진행
  .catch(err => ...)  // 기존 비밀번호가 일치하지 않음을 알림.
```

Mollbar 프로젝트에서는 JWT(Json Web Token) 인증 방식을 사용하기 때문에, 로그인 URL에 위와 같이 요청을 보내면 새로운 토큰 정보가 반환된다. 이때 새로 발급받은 토큰 정보를 저장해도 되지만, 기존 토큰도 여전히 사용 가능하기 때문에 새로운 토큰을 따로 저장하지는 않았다. (이후에 blacklist를 이용하여 기존 토큰의 효력을 없애고 새로운 토큰을 추가하는 방식도 검토해볼 계획이다.)

<br>

### 새로운 비밀번호 검증

위의 요청에서 오류가 없다면, client에서는 다시 `새 비밀번호`와 `새 비밀번호 확인` 값을 비밀번호 변경 URL에 요청을 보낸다. 이제 해당 URL에서는 `새 비밀번호`와 `새 비밀번호 확인`이 일치하는지, 그리고 `새 비밀번호`가 유효한 비밀번호 값인지를 판단한다. 

- 판단 결과 문제가 있다면, server에서는 해당 내용을 담은 응답을 다시 client로 보낸다.

- 판단 결과 문제가 없다면, server에서는 기존 유저 정보에 새로운 유저 정보를 덮어쓴다.

<br>

### 문제 2 - 유저 정보 업데이트하기

여기에서 다시 어떻게 새로운 유저 정보를 덮어쓸 것인가가 문제가 된다. 기존 유저 자체를 삭제한 뒤 새로운 유저 정보를 저장하는 방법도 있지만, 이 경우 기존 유저가 쓴 게시글, 댓글, 평가 정보 등이 사라지기 때문에 적절하지 않다. 기존 유저 정보를 유지한 채로 비밀번호만 변경해야 한다.

이를 위해, 회원가입 시 사용한 UserSerializer를 사용하되, 현재 유저를 인스턴스로 넣어주어 CREATE가 아니라 UPDATE가 되도록 했다. `request.user`가 현재 로그인한 유저이므로, 그 유저의 다른 필드 값들과 새로 받은 비밀번호 값을 UserSerializer에 넣었다.

```python
# accounts/serializers.py

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = get_user_model()
        fields = ('username', 'password', 'email')
```

```python
# accounts/views.py

@api_view(['PUT'])
def change_password(request):
    new_password = request.data['newPwd']
    new_password_confirmation = request.data['newPwdConfirmation']
    
    """
    1. 비밀번호 유효성 확인 (글자수, 대소문자 및 숫자로 이루어졌는지 여부)
       (유효하지 않은 경우 상태 코드 400의 응답을 리턴한다.)
    
    2. 비밀번호 일치 여부 확인 (new_password와 new_password_confirmation이 같은지 여부)
       (일치하지 않는 경우 상태 코드 400의 응답을 리턴한다.)
    """

    user_data = {
        'username': request.user.username,
        'password': new_password,
        'email': request.user.email,
    }
    
    serializer = UserSerializer(request.user, data=user_data)

    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        user.set_password(new_password)  # 비밀번호 암호화
        user.save()                      # 유저 정보 DB에 저장 (덮어쓰기)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
```

이제 client에서는 비밀번호가 변경되었다는 응답을 받은 경우, 기존 token을 삭제한 뒤 로그인 창으로 리다이렉트하거나 자동으로 로그인되게 만들면 된다. DB에서 새 비밀번호가 저장되었으므로, 변경 이전의 비밀번호로 로그인을 시도하는 경우 토큰을 받지 못한다.

<br>

### 정리

전체 과정을 정리하면 다음과 같다.

1. `기존 비밀번호`, `새 비밀번호`, `새 비밀번호 확인` 값을 입력받는다.

2. 현재 로그인한 유저의 username과 `기존 비밀번호` 값을 loginURL로 요청을 보낸다. (POST)
   
3. 만약 오류가 발생한다면, `기존 비밀번호`가 일치하지 않음을 보여준다.

4. 오류가 없다면, 다시 `새 비밀번호`와 `새 비밀번호 확인` 값을 비밀번호 변경 URL로 요청을 보낸다. (PUT)

5. 서버에서는 `새 비밀번호`와 `새 비밀번호 확인`의 일치 여부, `새 비밀번호`의 유효성을 판단한다.

6. 비밀번호가 유효함이 확인되었다면, 기존 유저 정보 + `새 비밀번호` 값을 UserSerializer에 담아 직렬화한다.

7. 비밀번호를 암호화한 뒤, 새로운 유저 정보를 DB에 저장한다.

8. client에서 기존 token 정보를 삭제한다.

9. 로그인 창으로 보낸다. (혹은 자동으로 로그인되게 만든다.)