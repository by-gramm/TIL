## command

> git 명령어 정리



### 생성

##### init

- 현재 폴더를 git으로 관리하겠다고 선언
- 현재 폴더에 `.git` 폴더를 생성
-  최초 한번만 실행하는 명령어
- 프로젝트 단위에서 실행

```bash
git init
```



### 확인

##### status

- 현재 git이 관리하고 있는 파일들의 상태를 보여주는 명령어

```bash
git status
```



##### log

- 커밋 히스토리를 보여주는 명령어
  - `--oneline` : 각 로그를 한 줄에 출력함.
  - `--graph` : 커밋 히스토리를 그래프 형식으로 출력함.

```bash
git log
```

```bash
git log --oneline
```

```bash
git log --oneline --all --graph
```



### 관리 (로컬)

>  working directory : 내가 작업하고 있는 공간

>  staging area : 임시 저장 공간



##### add

- working directory에서 staging area에 파일을 업로드하는 명령어
  - `.` : 현재 폴더, 하위 폴더, 하위 파일 모두
- add 뒤에 디렉토리명이 오는 경우, 해당 디렉토리 내에 수정사항이 있는 모든 파일을 staging area에 업로드

```bash
git add <filename>
git add <directory name>
```

```bash
git add .
```



##### reset

- staging area에 업로드한 파일을 다시 내리는 명령어

```bash
git reset <filename>
```

##### commit

- staging area에 올라온 파일들을 하나의 커밋으로 만들어 주는 (스냅샷 찍는) 명령어
  - `--amend` : 직전에 생성한 커밋을 새로운 커밋으로 대체

```bash
git commit -m "commit message"
```

```bash
git commit --amend
```



### 관리 (원격)

##### remote add

- 원격 저장소 주소를 로컬에 저장하는 명령어
  - nickname에는 일반적으로 `origin`을 사용

```bash
git remote add <nickname> <url>
```



##### push

- 원격 저장소로 로컬의 커밋 기록을 업로드하는 명령어


```bash
git push <nickname> <branch name>
```

- 로컬 저장소의 내용을 처음 원격 저장소에 올릴 때는 아래의 명령어를 사용함.

```bash
git push -u origin master
```

##### clone

- 원격 저장소(ex. Github)의 프로젝트를 로컬에 가져오는 명령어

```bash
git clone <remote repository address>
```

### 브랜치 관리

##### branch

- 새로운 브랜치를 생성하는 명령어

```bash
git branch <branchname>
```

##### branch -d

- 브랜치를 삭제하는 명령어

```bash
git branch -d <branchname>
```

##### switch

- 현재 작업 중인 브랜치를 (switch 뒤의 브랜치로) 이동하는 명령어

```bash
git switch <branchname>
```

##### merge

- 현재 브랜치에 다른 브랜치를 병합시키는 명령어
  - `--squash` : git merge에서 지정한 브랜치의 모든 커밋을 하나의 커밋으로 만듬.

```bash
git merge <branchname>
```

```bash
git merge --squash <branchname>
```

##### merge --abort

- git merge에서 conflict 발생 시, merge 이전 상태로 되돌아가게 하는 명령어

```bash
git merge --abort
```

### 기타

##### help

- Git 명령어의 공식 매뉴얼 내용을 출력하는 명령어

```bash
git help <command name>
```

