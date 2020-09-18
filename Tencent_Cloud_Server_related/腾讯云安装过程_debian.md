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

## 安装node.js
```shell
apt install nodejs npm
node -v
```


## 安装python3.8必须的库及软件：
```shell
apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev curl

wget https://www.sqlite.org/2020/sqlite-autoconf-3330000.tar.gz
tar xvf sqlite-autoconf-3330000.tar.gz
cd sqlite-autoconf-3330000
./configure --prefix=/usr/local/sqlite
make && make install
```

下载python 3.8.5
```shell
wget http://npm.taobao.org/mirrors/python/3.8.5/Python-3.8.5.tgz
tar xvf Python-3.8.5.tgz
cd Python-3.8.5
```

此时需修改setup.py
```shell
查找" sqlite_inc_paths" 新增
'/usr/local/sqlite/include'
'/usr/local/sqlite/include/sqlite3'
```

再安装python
```shell
./configure --enable-optimizations --enable-loadable-sqlite-extensions
make -j `grep processor /proc/cpuinfo | wc -l`
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

## 安装虚拟环境，进入虚拟环境
此时突然发现pip出问题了
```shell
No module named pip3
```

需要排除这个问题，强制重装pip3
注意这里要用“python3”
```shell
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
sudo python3 get-pip.py
```

```shell
sudo -H python -m pip3 install --upgrade pip
sudo -H python -m pip3 install --upgrade virtualenv
mkdir ~/myprojectdir
cd ~/myprojectdir
virtualenv myprojectenv
source myprojectenv/bin/active
python -m pip install pip --upgrade --use-feature=2020-resolver
```

## 安装并设置jupyterlab
```shell
python -m pip install jupyterlab

sha1:4de2eee9c661:dd597542536188fed6aa679ab6bc4203496d08d6

mkdir /home/mick/data/jupyter
mkdir /home/mick/data/jupyter/root
cd /home/mick/data/jupyter
python -c "import IPython; print(IPython.lib.passwd())"
输入自定义密码，生成sha1串: sha1:c70ff9706539:0deebacedca7300f8aa4bd541d6d2bea946eeea8
jupyter lab --generate-config --allow-root

vi /root/.jupyter/jupyter_notebook_config.py
	更改项目：
	c.NotebookApp.ip = '*'
	c.NotebookApp.allow_root = True
	c.NotebookApp.open_browser = False
	c.NotebookApp.port = 8347
	c.NotebookApp.password = u'sha1:c70ff9706539:0deebacedca7300f8aa4bd541d6d2bea946eeea8'
	c.ContentsManager.root_dir = '/home/mick/data/jupyter/root'
```

出现错误信息：
```shell
Command '('lsb_release', '-a')' returned non-zero exit status 1
```
```shell
sudo rm /usr/bin/lsb_release
```
