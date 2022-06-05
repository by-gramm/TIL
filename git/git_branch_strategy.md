# git 브랜치 전략

> 여러 개발자가 하나의 git 저장소를 사용하는 환경에서, git 저장소를 효과적으로 활용하기 위한 전략 (ex. git-flow, github-flow)



### git = 버전 관리 시스템

- **버전 관리** = 이전 버전의 상태를 기억하는 것
  - How? 시간순으로 프로젝트의 **스냅샷(snapshot)**을 저장한다.
  - 프로젝트 전체를 사진으로 찍어서 관리하는 것과 같은 방식
- Q. 버전 관리는 왜 필요한가?
  - 이전 버전의 상태를 기억하기 때문에
    - 각 파일 or 프로젝트를 이전 상태를 되돌릴 수 있고
    - 오류 발생시 쉽게 복구할 수 있고
    - 시간에 따른 변경 내용을 비교할 수 있고
    - 문제의 발생 원인을 추적할 수 있다

<br>

### git-flow 전략

![](./git.assets/git-flow.png)

(이미지 출처 : [A successful git branching model](https://nvie.com/posts/a-successful-git-branching-model/))

- **feature > develop > release > hotfix > master** 브런치가 존재한다.
  - 메인 브랜치인 master, develop 브랜치는 항상 남아있는다.
  - 보조 브랜치인 feature, release, hotfix 브랜치는 사용을 마치면 삭제한다.
- feature 브랜치에서 merge시 `--no-ff` 옵션 사용이 권장된다.
  - non fast-forward
  - 병합 대상 브랜치가 fast-forward 관계인 경우에도, 반드시 merge  커밋을 만든다.
  - 어떤 브랜치로부터 merge되었는지의 이력이 남기 때문에  commit 기록을 되돌리기 쉬워진다.
- 개발 프로세스
  1. **develop** 브랜치로부터 각 기능별로 **feature** 브랜치를 만들어 기능을 개발한다.
     - `feature/기능명`
  2. **feature** 브랜치에서 기능이 완성되면 **develop** 브랜치에 merge한다.
  3. 배포할 버전의 기능이 모두 merge된 경우, **release** 브랜치를 생성한 뒤 QA를 통해 버그를 수정한다.
     - `release/버전명	`
  4. **release** 브랜치에서 수정이 완료된 경우, **master** 브랜치로 merge한다. 변경 내용이 있는 경우 **develop** 브랜치에도 merge한다.
  5. **master** 브랜치에서 버그 발생시, **hotfix** 브랜치를 만든다.
     - `hotfixes/차기버전명`
  6. **hotfix** 브랜치에서 버그를 수정한 뒤, 변경 내용을 **develop, master** 브랜치에 merge한다.

- 장점
  - 대규모 프로젝트 관리에 적합하다.
  - 주기적으로 배포하는 서비스에 적합하다.
- 단점
  - 브런치가 많아서 사용하기 복잡하다.
  - 규모가 작은 프로젝트의 경우, 불필요한 절차가 많아 효율성을 저하시킨다.

<br>

### github-flow 전략

![img](./git.assets/github-flow.png)

- git-flow 전략과 달리 기능 개발, 버그 수정 등의 작업용 브랜치를 구분하지 않는다.

- master 브랜치의 코드는 항상 배포 가능해야 한다.

- 개발 프로세스

  1. **master** 브랜치로부터 기능을 명확히 보여주는 이름의 브랜치를 생성한다.

  2. 작업 내용을 기능별로 commit하고, 정기적으로 원격 브랜치에 push한다.
  3. 기능 구현이나 오류 수정이 완료된 경우, **pull request**를 보낸다.
  4. PR 내용에 대해 팀원들과 리뷰와 논의를 한다.
  5. merge하기 전에 브랜치 내에서 코드를 배포하여 테스트한다. (Github가 제공하는 기능) 해당 브랜치에서 문제가 발생하는 경우, 기존 master 브랜치를 다시 배포한다.
  6. 개발 브랜치의 검증이 완료되면 **master** 브랜치에 merge한다.

- 장점
  - 브랜치 전략이 간단하여 이해하기 쉽다.
  - CI/CD가 자연스럽게 이루어진다.
- 단점
  - develop 브랜치의 부재로 인해 master 브랜치의 코드가 정리되지 않거나, 버그가 발생할 확률이 높아진다.

<br>

### 브랜치 전략의 선택 기준

- 프로젝트 규모가 큰 경우, Production의 공식 배포 주기가 긴 경우 => **git-flow**

- 프로젝트 규모가 작은 경우, 지속적으로 테스트 및 배포를 하는 경우 => **github-flow**



개인적으로 참여한 프로젝트에서는 **git-flow 전략**을 사용했는데, 그 이유는 아래와 같다.

- 수시로 배포하는 대신 주기적으로 배포하는 방식을 택했는데, 이에 더 적합한 전략이다.

- 많은 기업에서 표준으로 사용하는 전략이기 때문에 익혀두면 좋겠다는 생각도 있었다.

<br>

### 참고 출처

https://git-scm.com/book/ko/v2

https://www.youtube.com/watch?v=EzcF6RX8RrQ

https://www.youtube.com/watch?v=wtsr5keXUyE

https://www.gitkraken.com/learn/git/best-practices/git-branch-strategy