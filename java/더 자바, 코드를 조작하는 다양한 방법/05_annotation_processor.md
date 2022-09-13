### Lombok

- `@Getter`, `@Setter` 등의 어노테이션으로 표준적인 메소드를 자동 생성해주는 라이브러리
- 어노테이션 종류
  - `@Getter`, `@Setter`
    - 클래스에 사용시, 모든 필드의 getter/setter 메소드
    - 변수에 사용시, 해당 필드의 getter/setter 메소드
  - `@AllArgsConstructor`
    - 모든 필드를 사용하는 생성자
  - `@NoArgsConstructor`
    - 기본 생성자
  - `@RequiredArgsConstructor`
    - final 키워드나 @NotNull이 붙은 필드만으로 구성된 생성자
  - `@EqualsAndHashCode`
    - 클래스의 equals() 메소드, hashCode() 메소드
  - `@ToString()`
    - toString() 메소드
    - `@ToString(exclude = "password")`와 같이, 특정 필드를 제외할 수 있다.
- 동작 원리
  - 컴파일 시점에 **어노테이션 프로세서**를 사용하여 소스코드의 **AST(abstract syntax tree)**를 조작한다.
  - 공개되지 않은 API를 사용하기 때문에 일종의 해킹이라는 의견도 있다. 다만 사용의 편리함 때문에 여전히 널리 사용되고 있다.

<br>

### Annotation Processor

- 컴파일 시점에 특정 어노테이션이 붙은 소스 코드를 사용하여 새로운 소스 코드를 만들어준다.
  - 롬복에서는 기존의 소스 코드 자체를 변화시킨다.

- **Processor 인터페이스**
  - 여러 rounds에 거쳐 소스 및 컴파일된 코드를 처리할 수 있다.

- **AutoService**
  - 어노테이션 프로세서의 일종
  - `@AutoService(Processor.class)`
    - 컴파일 시점에 어노테이션 프로세서를 사용하여 MANIFEST 파일을 자동으로 생성해준다.
- **JavaPoet 라이브러리**
  - 소스 코드를 쉽게 생성해주는 라이브러리
- 어노테이션 프로세서 사용 예시

```java
@AutoService(Processor.class)  // 컴파일 시 MANIFEST 파일을 자동으로 만들어준다.
public class MagicMojaProcessor extends AbstractProcessor {

    @Override  // 'Magic'이라는 이름을 가진 어노테이션 타입을 지원한다.
    public Set<String> getSupportedAnnotationTypes() {
        return Set.of(Magic.class.getName());
    }

    @Override  // 최신 버전의 소스 코드 버전을 지원한다.
    public SourceVersion getSupportedSourceVersion() {
        return SourceVersion.latestSupported();
    }

    @Override  // process()는 어노테이션 프로세서의 main() 메소드
    public boolean process(Set<? extends TypeElement> set, RoundEnvironment roundEnv) {
        Set<? extends Element> elements = roundEnv.getElementsAnnotatedWith(Magic.class);

        for (Element element : elements) {
            Name elementName = element.getSimpleName();

            // 인터페이스에만 해당 어노테이션을 달 수 있도록 한다.
            if (element.getKind() != ElementKind.INTERFACE) {  // 인터페이스 X => Error 발생시키기
                processingEnv.getMessager().printMessage(
                        Diagnostic.Kind.ERROR,
                        "Magic 어노테이션은 " + elementName + "에 사용할 수 없습니다.");
            } else {  // 인터페이스 O => 로깅
                processingEnv.getMessager().printMessage(Diagnostic.Kind.NOTE, "Processing " + elementName);
            }

            TypeElement typeElement = (TypeElement) element;
            ClassName className = ClassName.get(typeElement);

            // 메서드 생성
            MethodSpec pullOut = MethodSpec.methodBuilder("pullOut")  // 메서드명
                    .addModifiers(Modifier.PUBLIC)
                    .returns(String.class)
                    .addStatement("return $S", "Rabbit!")
                    .build();

            // 클래스 생성
            TypeSpec magicMoja = TypeSpec.classBuilder("MagicMoja")  // 클래스명
                    .addModifiers(Modifier.PUBLIC)
                    .addSuperinterface(className)  // 상위 인터페이스 타입 추가
                    .addMethod(pullOut)            // pullOut 메소드 추가
                    .build();

            Filer filer = processingEnv.getFiler();

            try {
                JavaFile.builder(className.packageName(), magicMoja)
                        .build()
                        .writeTo(filer);
            } catch (IOException e) {
                processingEnv.getMessager().printMessage(Diagnostic.Kind.ERROR, "FATAL ERROR: " + e);
            }
        }

        return true;  // true 리턴 => 다음 프로세서에 넘기지 않는다.
    }
}
```

- 사용 예시
  - Lombok
  - AutoService
  - `@Override`
    - 안정성 : 문법 오류가 있는 경우 컴파일 에러가 발생한다.
- 장점
  - 런타임 비용이 없다. 
  - java agent를 사용한 바이트코드 조작의 경우, 런타임시 추가 비용이 발생한다. 
  - 반면 어노테이션 프로세서는 컴파일 시에 미리 필요한 조작을 끝낸다.