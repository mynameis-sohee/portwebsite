가상환경 설정해둬서 가상환경 안으로 들어가서 작업해야함
가상환경 들어가려면 PORTWEBSITE 디렉토리에서
source venv/portwebsite/bin/activate
명령어 입력
가상환경 나가기는 deactivate

서버 실행하고 싶으면 가상환경 들어가서 python manage.py runserver 0.0.0.0:8000 명령어 입력하면 서버 실행

https://www.mongodb.com/compatibility/mongodb-and-django
위의 링크에서 3번째 방법인 Djongo 사용하는 방법으로 데이터베이스랑 연결함

우리 기본 db이름은 portewbsite_db로 설정함

djongo Docs 링크: https://www.djongomapper.com/get-started/

PORTWEBSITE 디렉토리 바로 밑에 templates 폴더 만들어둬서 거기서 html작업
부트스트랩 5.0.2 버전으로 사전작업 다 끝내둠
각 페이지 마다 Nav 컴포넌트 박아둠
링크 참조: https://getbootstrap.com/docs/5.0/components/navbar/
