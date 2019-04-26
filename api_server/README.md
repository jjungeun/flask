# First Flask

##### 이 레포지터리에는 flask를 이용한 api server를 구현한 코드가 있습니다.

환경은 ubuntu, zsh(oh my zsh)shell, conda가상환경에서 진행하였습니다.

### +추가


mininoda를 install한 후에 zsh쉘 환경설정하고 가상환경을 다루는 과정에서 좀 헤매서 해결과정을 정리하겠습니다.

``` bash
sudo apt install zsh
```

chsh로 쉘을 변경해도 되지만 바로 적용하기 위해 exec한다.

```bash
exec zsh
```
echo $SHELL로 확인한다. 그리고 zsh 설정관리툴인 oh my zsh를 설치한다.

```zsh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
```

~/.zshrc 파일에 쉘 설정을 한다. 꼭 들어가야 하는 정보는 conda의 경로를 설정하는 것이다.

```~/.zshrc
export PATH="/usr/jungeun/miniconda3/bin:$PATH"
```



이제 환경설정은 다 끝났으니 가상환경을 만들고 활성화시킨다.

```zsh
conda create --name <name>
conda activate <name>
```



다 잘 되었으면 마지막으로 flask를 설치한다.

**여기서 중요한건 가상환경에서만 install하려면 apt install이 아닌 conda install을 해야한다.**

 ```zsh
conda install flask
 ```

