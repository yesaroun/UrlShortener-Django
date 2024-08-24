# URL Shortener

## Tasks

- Front-end
  - 메인 랜딩 페이지
  - 로그인/회원가입 페이지
  - 비밀번호 찾기 페이지
  - 이메일 인증
  - URL 단축
  - 통계 페이지
  - 회원 개인 프로필 설정
  - 회사 설정
  - Vue.js

- Back-end
  - 정책 수립
  - DB 모델링
  - Rendering Views
  - API 만들기
  - Cache 사용

- 기타
  - 텔레그램 봇
  - Static File 관리
  - CICD 구성

## 정책

- 기본
  - User 당 50개 생성 가능
  - 리프레시 하지 않으면 60일 유효
  - 이메일 미인증시 사용 불가
  - 1초에 같은 IP에서 5회 이상 호출 불가
  - 기본통계 제공
  - 302 리텅

- 유료
  - 무제한 생성 가능
  - 삭제할때까지 삭제되지 않음
  - 이메일 미인증시 사용 불가
  - 1초에 같은 IP에서 20회 이상 호출 불가
  - 어드벤스드 통계 제공
  - 301 리턴

## 실행

gunicorn

```bash
gunicorn --bind 127.0.0.1:8000 UrlShortenerDjango.wsgi:application
```
