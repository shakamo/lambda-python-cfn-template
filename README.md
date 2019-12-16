# lambda-python-cfn-template


```
$ brew tap versent/homebrew-taps
$ brew tap aws/tap
$ brew install aws-sam-cli
$ brew install saml2aws
$ brew install python3

$ brew list --versions
aws-sam-cli 0.31.0
saml2aws 2.19.0
python 3.7.5
```


```
$ pip install autopep8
$ pip install flake8

$ pip list --version
autopep8 1.4.4
flake8 3.7.9
```

```
$ brew install docker
$ brew cask install docker

$ docker -v
Docker version 19.03.4, build 9013bf5
```


Visual Studio Code で以下の Extension をインストールします。

- AWS Toolkit for Visual Studio Code
- Python

saml2aws をセットアップします。

```
$ saml2aws configure
```


saml2aws を使用して AWS にログインします。

```
$ saml2aws login -a default
```


Visual Studio Code を起動します。  
Settings の aws.samcli.location に sam のパスを設定します。

```
$ which sam
/usr/local/bin/sam
```


必要に応じて以下を追加   ~/.aws/config
```
[saml]
region = ap-northeast-1
output = json
```
