
# 파이썬으로 주식정보사이트 만들기.
명지전문대학 윤재락, 강태원, 김태진



## 필수 설치 요소   
anaconda 32bit 설치 > https://baessi.tistory.com/125   
maria DB 설치 > https://mariadb.org/download/ 10.5.9 version   
heildsql 설치 > 선택. sql 테이블을 관리할 수 있는 프로그램이라면 상관 없음.   
단, MySQL과 호환 가능한 툴이어야 합니다.(MariaDB 사용)

## 주의사항 
실행시 anaconda 로 32bit의 가상환경 세팅 후 runserver 할 것 -> kiwoom api를 사용하지 않았기 때문에 64bit도 상관없긴 하지만, 추후 사용을 위해서는 32bit로 진행하는 것 추천.   
포트번호는3306 혹은 3308 사용 -> 변경시 DBupdate -> 포트넘버 변경, setting 의 포트넘버 변경

----
*phpmyadmin*   
아이디 : ykk_stock   
비밀번호 :    
서버주소 :    
포트 : 3306   
데이터베이스 : ykk_stock   

* 기존 외부DB를 사용하였으나, git에 커밋한 내용은 내부 DB를 사용할 수 있도록 변경하였습니다.

---
```shell
pip install Django # 장고설치   
pip install jsonfield # json 설치   
pip install bs4 # beautifulSoup 설치   
pip install pandas # DataFrame 기본인 pandas 설치   
pip install pymysql # sql DB를 활용하기 위한 모듈   
pip install pykrx # 각종 주식 정보가 있는 pystock api 설치   
```
----
설치후 오류 예상
1. detail 부분 쿼리 오류 -> view의 날자 3,10,17,24 > 를 수치 조정하여 최근 업데이트 6/18 로 조정 ex) 오늘이 21일이면 3,10,17,24  22일이면 4,11,18,25   
2. news 부분 에러 -> 실행하는 컴퓨터에 config_secret 파일이 있어야 함. -> 네이버 API 를 다운받고 폴더안에 파일생성후 집어넣고 실행.
안될 시 문의   
jrakmom971106@gmail.com   
micro.kante@gmail.com
