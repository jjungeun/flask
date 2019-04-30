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

