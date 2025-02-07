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

安装curl
```shell
apt install curl
```

## 安装ta-lib
```shell
sudo apt install build-essential
sudo apt install python3-dev
sudo apt install pip
```

从ta-lib官网下载最新版的deb文件（官网链接： https://ta-lib.org/install/）
```shell
sudo dpkg -i ta-lib_0.6.4_amd64.deb
```

修改 .bashrc
增加两行：
```shell
export PYTHONPATH=/usr/local/lib/python3.11/dist-packages
export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
```

python -m pip install TA-Lib --break-system-packages

如果安装成功，测试一下：
python
```python
import talib
print(talib.get_functions())
```

如果运行没报错，应该安装成功了。

## 安装node.js

通过curl命令向系统添加NodeSource存储库，再安装nodejs 20.x及npm
```shell
# nodejs 可以自动带入虚拟环境
curl -sL https://deb.nodesource.com/setup_20.x | sudo bash -
sudo apt install nodejs

## Run `apt install -y nodejs` to install Node.js 14.x and npm
## You may also need development tools to build native addons:
     apt install gcc g++ make
## To install the Yarn package manager, run:
     curl -sL https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
     echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
     sudo apt update && sudo apt install yarn

# 这里可能需要做一个nodejs的link，link to node
# node位于/usr/bin
# ln -s /usr/bin/node /usr/bin/nodejs

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
# 设置清华源
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
sudo cp /root/.pip/pip.conf .
sudo chown mick pip.conf

# 先下载安装talib
mkdir /home/mick/temp
cd /home/mick/temp
wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz
tar -xvf ta-lib-0.4.0-src.tar.gz
cd ta-lib
./configure --prefix=/usr
make
sudo make install

# 再安装python版本的talib
cd /home/mick
mkdir /home/mick/talib_temp
cd /home/mick/talib_temp

# 这里因为连接github速度太慢，改为用github的镜像 github.com.cnpmjs.org
git clone https://github.com.cnpmjs.org/mrjbq7/ta-lib.git
cd ta-lib
sudo python setup.py install

# reboot后才能生效
reboot

# 至此，已经把talib库装入系统，但虚拟环境还需重新弄一遍
```


## 安装虚拟环境，进入虚拟环境
```shell
sudo -H python -m pip install --upgrade pip
sudo -H python -m pip install --upgrade virtualenv

virtualenv myprojectenv
source myprojectenv/bin/active
python -m pip install pip --upgrade
```

## 在虚拟环境重安装一遍ta-lib
```shell
python -m pip3 install ta-lib
# 至此，虚拟环境的python也把talib库安装好了
```

## 安装并设置jupyterlab，已进入myprojectenv虚拟环境
```shell
python -m pip install jupyterlab
mkdir /home/mick/data
mkdir /home/mick/data/jupyter
mkdir /home/mick/data/jupyter/root
cd /home/mick/data/jupyter/root
python -c "import jupyter_server.auth; print(jupyter_server.auth.passwd())"
输入自定义密码，生成sha1串: argon2:$argon2id$v=19$m=10240,t=10,p=8$inpSJvyVORFtPb4pQtty0Q$yl2A3OV/s/u8ISZR3JKQJzmA4Y4+vyw3BxMqVveW7FY

jupyter lab --generate-config --allow-root

vi /home/mick/.jupyter/jupyter_notebook_config.py
	更改项目：
	c.ServerApp.ip = '*'
	c.ServerApp.allow_root = True
	c.ServerApp.open_browser = False
	c.ServerApp.port = 8347
	c.ServerApp.password = u'argon2:$argon2id$v=19$m=10240,t=10,p=8$inpSJvyVORFtPb4pQtty0Q$yl2A3OV/s/u8ISZR3JKQJzmA4Y4+vyw3BxMqVveW7FY'
	c.ServerApp.root_dir = '/home/mick/data/jupyter/root'
```

如果是在aws或ucloud的云服务器上安装，记得把安全组策略的入站规则，加入8347端口

```shell
jupyter lab build --dev-build=False --minimize=False

# 启动时要加上 --no-browser 参数
nohup jupyter lab --no-browser &
```



## 安装完如果import pandas出现lzma出错
```shell
apt install -y liblzma-dev
python -m pip install backports.lzma
```
然后得修改 /usr/local/lib/python3.9/lzma.py
```shell
vi /usr/local/lib/python3.9/lzma.py
```
_lzma那两句import得修改如下：
```shell
try:
    from _lzma import *
    from _lzma import _encode_filter_properties, _decode_filter_properties
except ImportError:
    from backports.lzma import *
    from backports.lzma import _encode_filter_properties, _decode_filter_properties
```

# 注意：安装kite插件总是出错，暂时不建议安装
## 给 jupyter lab 安装 kite 插件（自动补全代码）
```shell
# 先从 kite 官网下载并安装 kite
bash -c "$(wget -q -O - https://linux.kite.com/dls/linux/current)"

# 安装好 kite 以后，如果无 error
python -m pip install jupyter-kite
jupyter labextension install @kiteco/jupyterlab-kite --dev-build=False --minimize=False
```

---
# windows10安装ta-lib
```shell
# 从 https://www.lfd.uci.edu/~gohlke/pythonlibs 下载 TA_Lib-0.4.24-cp310-cp310-win_amd64.whl
# 把 TA_Lib-0.4.24-cp310-cp310-win_amd64.whl 放到 c:\windows\system32
cd c:\windows\system32
python -m pip install TA_Lib-0.4.24-cp310-cp310-win_amd64.whl
```