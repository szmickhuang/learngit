# 安装好debian 10.2

## 安装debian后常规处理
```shell
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

通过curl命令向系统添加NodeSource存储库，再安装nodejs 12.x及npm
```shell
curl -sL https://deb.nodesource.com/setup_12.x | sudo bash -
apt install nodejs

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
python -m pip install pip --upgrade --use-feature=2020-resolver
```

## 安装并设置jupyterlab，已进入myprojectenv虚拟环境
```shell
python -m pip install jupyterlab
mkdir /home/mick/data
mkdir /home/mick/data/jupyter
mkdir /home/mick/data/jupyter/root
cd /home/mick/data/jupyter
python -c "import IPython; print(IPython.lib.passwd())"
输入自定义密码，生成sha1串: sha1:57e7657408d7:ee7a0271842fc98a4ad3314ea596ec27e277d00b

jupyter lab --generate-config --allow-root

vi /home/mick/.jupyter/jupyter_notebook_config.py
	更改项目：
	c.ServerApp.ip = '*'
	c.ServerApp.allow_root = True
	c.ServerApp.open_browser = False
	c.ServerApp.port = 8347
	c.ServerApp.password = u'sha1:57e7657408d7:ee7a0271842fc98a4ad3314ea596ec27e277d00b'
	c.ServerApp.root_dir = '/home/mick/data/jupyter/root'
```

```shell
jupyter lab build --dev-build=False --minimize=False
```

安装ta-lib