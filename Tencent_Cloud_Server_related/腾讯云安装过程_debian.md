# 安装好debian 10.2

## 安装debian后常规处理
```shell
su
useradd -m mick -g root -s /bin/bash -d /home/mick
passwd mick
```

需要让mick账户可通过sudo安装软件
```shell
apt install sudo
vi /etc/sudoers
```
在root后面添加mick
```shell
# User privilege specification
root ALL=(ALL) ALL
mick ALL=(ALL) ALL
```

更新系统：
```shell
apt update
apt upgrade
```

安装python3.8必须的库及软件：
```shell
apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev curl
```

下载python 3.8.5
```shell
wget http://npm.taobao.org/mirrors/python/3.8.5/Python-3.8.5.tgz
tar xvf Python-3.8.5.tgz
cd Python-3.8.5
./configure --enable-optimizations
make
make install
```

更改pip源为国内源，此时改用mick登录（非root）
```shell
mkdir ~/.pip
cd ~/.pip
touch pip.conf
vi pip.conf
```
pip.conf的内容：
```shell
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple

[install]
use-mirrors = true
mirrors = https://pypi.tuna.tsinghua.edu.cn/simple
trusted-host = pypi.tuna.tsinghua.edu.cn
```

安装虚拟环境，进入虚拟环境
```shell
sudo -H pip3 install --upgrade pip
sudo -H pip3 install --upgrade virtualenv
mkdir ~/myprojectdir
cd ~/myprojectdir
virtualenv myprojectenv
source myprojectenv/bin/active
pip install pip --upgrade --use-feature=2020-resolver
```

安装jupyterlab
```shell
pip install jupyterlab
```

把原有的debian 9升级到debian 10
```shell
sed -i 's/stretch/buster/g' /etc/apt/sources.list
apt-get update && apt-get upgrade
apt-get dist-upgrade
reboot
```

查看是否已升级为10（buster）了
```shell
lsb_release -a
```


安装python3和pip标头
```shell
sudo apt install python3-pip python3-dev
```

为jupyter创建python虚拟环境
```shell
sudo -H pip3 install --upgrade pip
sudo -H pip3 install virtualenv

mkdir ~/myprojectdir
cd ~/myprojectdir

virtualenv myprojectenv

source myprojectenv/bin/activate
```

