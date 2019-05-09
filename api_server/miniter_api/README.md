FLASK_ENV는 Flask가 실행되는 개발 스테이지를 뜻한다.  development로 하면 debug 모드가 실행된다.

```
$ FLASK_ENV=development FKAS_APP=app.py flask run
```



dictionary의 setdefault함수 : 두개의 인자(키값, 값)를 전달한다. 키 값이 있다면 해당 키의 값을 반환하고 없다면 키를 생성하고 두번째 인자로 받은 값을 키의 값으로 설정한다.

```
user.setdefault('follow',set()).add(follow_id)
```

만약 user 딕셔너리에 follow키값이 있다면 값(set)에 follow_id를 추가하고, 없다면 'follow ' : {}를 딕셔너리에 추가한 후, follow_id를 follow 값(set)에 추가한다.

팔로우/언팔로우 엔드포인트 구성 시 list가 아닌 set을 사용하는 이유는 중복되어 요청이 들어와도 한번만 저장하기 위해서이다. 그런데 json모듈은 set을 JSON으로 변경하지 못한다.(리스트는 할 수 있음) 따라서  JSON인코더를 커스텀하여 기존의 JSON인코더대신 사용해야 한다. 커스텀 인코더가 할 일은 set을 list로 변환하는 일이다.

```
class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj,set):
            return list(obj)
        
        return JSONEncoder.default(self,obj)

app.json_encoder = CustomJSONEncoder
```

언팔로우 시, set에서 remove대신 discard를 하는 이유는 remove는 해당하는 값이 없으면 오류가 일어나지만 discard는 값이 없으면 무시하기 때문이다. set에 unfollow_id가 있는지 확인하지 않아도 된다.

```
user.setdefault('follow',set()).discard(unfollow_id)
```



# 인증

유저를 인증하기 위해 유저의 비밀번호를 단방향 해쉬암호를 사용하여 저장한다. bcrypt를 사용하면 단방향 암호 알고리즘을 더 안전하게 사용할 수 있다. HTTP통신은 stateless이므로 통신 전에 인증 절차를 거쳤는지 알 수 없기 때문에 access token을 통해 인증된 사용자인지 판별한다.

access token을 생성하는 방법 중 JWT(Json Web Token)을 사용해보았다.  user_id와 토큰 생성시간을 토큰을 만들었다. 여기서 중요한 점은 JWT를 생성 할 때 사용자의 개인정보는 포함시키면 안된다.



### flask 글로벌 객체 g

애플리케이션 전반에서 공유해야 할 데이터를 저장하고 사용하는데 효율적이다. 

miniter에서는 인증과정에서 user id를 저장하는데 사용하였다.

하지만 다수의 동시접근이 이뤄지면 문제가 생길수도 있다는 것을 염두에두어야한다.



### 데코레이터(decorator)

대상 함수를 wrap하고 함수 전에 먼저 시행되는 함수를 데코레이터함수라고 한다. 예를들어 인증절차이다. 함수마다 access token을 확인하는 코드가 있다면 중복이 매우 많아진다. 따라서 이런 경우 토큰을 확인하는 데코레이터 함수를 생성하고 인증이 필요한 함수에 데코레이터 선언만 해주면 된다.

혹은 특정 함수 다음에 꼭 시행되어야  하는 경우도 데코레이터를 이용할 수 있다.

데코레이터를 class로 사용하려면 \_\_call\_\_함수로 정의하면 된다.

