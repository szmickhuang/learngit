# 安装好debian 10.2

## 安装debian后常规处理
```shell
useradd -m mick -g root -s /bin/bash -d /home/mick
passwd mick
```

更新系统：
```shell
# 需要用到git
apt install git
apt update
apt upgrade
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

## 安装node.js

通过curl命令向系统添加NodeSource存储库，再安装nodejs 14.x及npm
```shell
# nodejs 可以自动带入虚拟环境
curl -sL https://deb.nodesource.com/setup_14.x | sudo bash -
apt install nodejs

## Run `apt install -y nodejs` to install Node.js 14.x and npm
## You may also need development tools to build native addons:
     apt install gcc g++ make
## To install the Yarn package manager, run:
     curl -sL https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -
     echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list
     apt update && sudo apt install yarn

nodejs --version

apt install python3-pip

rm /usr/bin/python
ln -s /usr/bin/python3 /usr/bin/python
ln -s /usr/bin/pip3 /usr/bin/pip
```

更改pip源为国内源，此时改用mick登录（非root）
```shell
mkdir ~/.pip
cd ~/.pip
sudo cp /root/.pip/pip.conf .
sudo chown mick pip.conf
```

## 安装虚拟环境，进入虚拟环境
```shell
sudo -H python -m pip install --upgrade pip
sudo -H python -m pip install --upgrade virtualenv

virtualenv myprojectenv
source myprojectenv/bin/active
python -m pip install pip --upgrade
```

## 安装ta-lib
```shell
# 先下载安装talib
mkdir /home/mick/temp
cd /home/mick/temp
wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
tar -xvf ta-lib-0.4.0-src.tar.gz
cd ta-lib
./configure --prefix=/home/mick/myprojectenv
make
make install

# 再安装python版本的talib
cd /home/mick
# 这里因为连接github速度太慢，改为用github的镜像 github.com.cnpmjs.org
git clone https://github.com.cnpmjs.org/mrjbq7/ta-lib.git
cd ta-lib
python setup.py install

# reboot后才能生效
reboot
```

## 安装并设置jupyterlab，已进入myprojectenv虚拟环境
```shell
python -m pip install jupyterlab
mkdir /home/mick/data
mkdir /home/mick/data/jupyter
mkdir /home/mick/data/jupyter/root
cd /home/mick/data/jupyter/root
python -c "import IPython; print(IPython.lib.passwd())"
输入自定义密码，生成sha1串: sha1:1345c2bf86f4:01f2100fd4e0ee7e1944d2a9595c7ea937227689

jupyter lab --generate-config --allow-root

vi /home/mick/.jupyter/jupyter_notebook_config.py
	更改项目：
	c.ServerApp.ip = '*'
	c.ServerApp.allow_root = True
	c.ServerApp.open_browser = False
	c.ServerApp.port = 8347
	c.ServerApp.password = u'sha1:1345c2bf86f4:01f2100fd4e0ee7e1944d2a9595c7ea937227689'
	c.ServerApp.root_dir = '/home/mick/data/jupyter/root'
```

```shell
jupyter lab build --dev-build=False --minimize=False

# 启动时要加上 --no-browser 参数
nohup jupyter lab --no-browser &
```

