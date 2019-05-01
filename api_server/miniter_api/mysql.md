### mysql의 root계정에 비밀번호로 접근하려면

처음엔 root계정의 plugin이 auth_socket으로 되어있다.

```
SELECT user,plugin from mysql.user;
```



다음의 명령어로 root 사용자의 인증 모드를 비밀번호를 사용해서 인증하는 모드로 변경한다.

```
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '비밀번호';
FLUSH PRIVILEGES;
```



그럼 이제 config파일에 mysql user정보를 설정하고 코드로 db에 접근할 수 있다.