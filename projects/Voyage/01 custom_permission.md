# [DRF] Custom Permission 적용하기

<br>

## ❗ 문제 발견

현재 진행중인 토이 프로젝트에서, 게시글을 READ/UPDATE/DELETE하는 함수 기반 뷰(`article_detail`)를 작성했다.

그리고 조회는 인증된 유저 모두에게 허용하며, 수정 및 삭제는 게시글 작성자에 한하여 허용하는 Custom Permission 클래스(`IsAuthorOrReadOnly`)를 만들어, `article_detail` 함수에 적용했다.

```python
# permissions.py
from rest_framework import permissions


class IsAuthorOrReadonly(permissions.BasePermission):
    """
    조회(GET)는 인증된 유저 모두에게 허용한다.
    수정(PUT) 및 삭제(DELETE)는 작성자에 한하여 허용한다.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user
```

```python
# views.py
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import Article
from .serializers import ArticleSerializer
from .permissions import IsAuthorOrReadonly


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthorOrReadonly])
def article_detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)

    # 게시물 상세 페이지 READ
    if request.method == 'GET':
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    # 게시글 UPDATE
    elif request.method == 'PUT':
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data)

    # 게시글 DELETE
    else:
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

그런데 POSTMAN으로 테스트해보니, 글의 작성자가 아닌 유저도 글을 삭제하거나 수정할 수 있는 문제가 있었다.

<br>

## 🔎 문제 위치 탐색 

일단 코드의 어떤 부분에서 문제가 발생했는지 알아보기로 했다. 

1. 처음 생각한 가능성은 `IsAuthorOrReadOnly` 클래스 자체가 적용되지 않는 것이었다. 이를 확인하기 위해 `has_permission` 메서드가 무조건 False를 리턴하도록 하고, GET 요청을 보냈는데 오류가 났다. 커스텀 클래스 자체는 적용되고 있었다.

```python
class IsAuthorOrReadonly(permissions.BasePermission):
    def has_permission(self, request, view):
        return False
```

2. 다음으로 생각한 가능성은 `IsAuthorOrReadOnly` 클래스 내의 `has_object_permission` 메서드가 적용되지 않는 것이었다. 이를 확인하기 위해 `has_object_permission` 메서드가 무조건 False를 리턴하도록 하고, PUT 요청을 보냈는데 오류가 나지 않았다. 또한 해당 메서드가 호출될 때 작동하도록 만든 print 함수도 호출되지 않았다. 결국 `has_object_permission` 메서드가 호출되지 않는 것이 문제였다.

```python
class IsAuthorOrReadonly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        print("호출")
        return False
```

<br>

## 🔑 문제 해결

여러 블로그와 stackoverflow 게시글을 돌고 돌아, 결국 공식 문서에서 해결의 실마리를 찾았다.

> Note: (중략) Also note that in order for the instance-level checks to run, the view code should explicitly call `.check_object_permissions(request, obj)`. If you are using the generic views then this will be handled for you by default. (Function-based views will need to check object permissions explicitly, raising PermissionDenied on failure.)

`has_permission` 메서드와 달리, `has_object_permission` 메서드는 인스턴스 레벨에서 유효성을 검사한다.

그런데 인스턴스 레벨의 검사가 작동하려면, view의 코드가 명시적으로 `.check_object_permissions` 메서드를 호출해야 한다고 한다. (제네릭 뷰에서는 따로 호출하지 않아도 자동으로 작동한다.) 

그런데 해당 메서드는 APIView의 내장 메서드이기 때문에, 함수 기반 뷰에서는 호출할 수가 없다. 내부 로직 자체를 직접 구현하는 방법도 있지만, 이는 매우 어려울 것이다. 결국 해당 부분을 클래스 기반 뷰로 수정하고, 클래스 내의 `get_object` 메서드에서 `check_object_permissions`을 호출하여 검사하는 방식으로 코드를 수정했다.

```python
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from diary.models import Article
from diary.permissions import IsAuthorOrReadonly
from diary.serializers import ArticleSerializer


class ArticleDetailView(APIView):
    """
    Custom Permission 클래스를 적용하기 위해, FBV를 CBV로 수정함.
    """
    permission_classes = [IsAuthorOrReadonly]

    def get_object(self, article_pk):
        article = get_object_or_404(Article, pk=article_pk)
        self.check_object_permissions(self.request, article)
        return article

    # 게시글 상세 페이지 READ
    def get(self, request, article_pk):
        article = self.get_object(article_pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    # 게시글 UPDATE
    def put(self, request, article_pk):
        article = self.get_object(article_pk)
        serializer = ArticleSerializer(article, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data)

    # 게시글 DELETE
    def delete(self, request, article_pk):
        article = self.get_object(article_pk)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

이제 게시글의 작성자만 해당 게시글을 수정/삭제할 수 있게 되었다!

<br>

## ✅ 정리

- 함수 기반 뷰에서는 `has_object_permission` 메서드를 사용할 수 없어서, Custom Permission을 사용하기 어렵다.

- Custom Permission을 사용하기 위해서는 제네릭 뷰를 사용하거나, 클래스 기반 뷰에 `check_object_permissions` 메서드를 호출하여 사용하면 된다.

- 공식 문서가 최고다.

<br>

### 참고 출처

https://www.django-rest-framework.org/api-guide/permissions/

https://stackoverflow.com/questions/35520592/django-custom-permissions-for-function-based-views

https://ssungkang.tistory.com/entry/Django-APIView%EC%97%90-permission-%EC%A7%80%EC%A0%95%ED%95%98%EA%B8%B0