# Debian 11上安装Python 3.10，并切换系统默认Python版本
## 更新程序包并安装变异依赖环境
```shell
sudo apt update && sudo apt upgrade
sudo apt install wget build-essential libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev
```
## 开始正式安装
### 1. 下载Python源码包
可以前往Python官网获取最新源码
```shell
cd ~
wget https://www.python.org/ftp/python/3.10.5/Python-3.10.5.tgz
```

### 2. 解压Python源码
将下载好的源码包进行解压，默认放在当前文件夹下的压缩包同名文件夹内
```shell
tar xzf Python-3.10.4.tgz
```

### 3. 编译Python源码
进入解压后的文件夹内，进行选项配置
```shell
cd Python-3.10.4
./configure --enable-optimizations

#--enable-optimizations为优化性能选项，其余类似的还有 --prefix=PATH 指定安装目录……，可根据需要进行选择。
#默认安装路径为 /usr/local/bin
```

### 4. 安装Python 3.10
```shell
make altinstall

#altinstall用于防止编译器覆盖默认Python版本
```

### 5. 验证安装
```shell
root@raspberrypi:~ # python3.10
Python 3.10.4 (default, Dec  5 2021, 22:46:09) [GCC 10.2.1 20210110] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

至此，已完成Python3.10的安装
接下来可以根据需要选择是否需要更改默认Python为Python3.10

## 切换Python版本
可以使用以下两个命令 whereis或which 确定已安装python的版本和路径：

```shell
# whereis：适用于查看目前已安装的所有Python版本及路径
root@raspberrypi:~ # whereis python
python: /usr/bin/python2.7-config /usr/bin/python /usr/bin/python3.9 /usr/bin/python2.7 /usr/bin/python3.9-config /usr/lib/python3.9 /usr/lib/python2.7 /etc/python3.9 /etc/python2.7 /usr/local/bin/python3.10-config /usr/local/bin/python3.10 /usr/local/lib/python3.9 /usr/local/lib/python2.7 /usr/local/lib/python3.10 /usr/include/python3.9m /usr/include/python3.9 /usr/include/python2.7 /usr/share/man/man1/python.1.gz
```
```shell
#which：适用于查看具体某个python版本的安装路径
root@raspberrypi:~ # which python3.10
/usr/local/bin/python3.10
```

## 为单个用户切换Python版本
只需要在该用户home目录下的 .bashrc 文件下新增 Alias 即可
```shell
alias python='/usr/local/bin/python3.10'
#python具体版本和路径可根据个人需要确定
```

修改完毕后，使用source ~/.bashrc命令，重新加载 .bashrc 文件，使其生效

## 系统级切换Python版本
使用update-alternatives --list python命令，为整个系统更改Python版本

### 1. 列出所有可用Python替代版本
```shell
root@raspberrypi:~ # update-alternatives --list python
/usr/bin/python2.7
/usr/bin/python3.9
/usr/local/bin/python3.10
```

### 2. 添加替代版本列表
如果运行后出现错误信息：update-alternatives: error:no alternatives for python
则为没有更新替代版本列表，使用以下命令添加：
```shell
#注意：update-alternatives --install <link> <name> <path> <priority>
#1.<link>一般情况下，直接使用 /usr/bin/python 即可
#2.<name>即为需要更换的python
#3.<path>为需要添加的python版本的安装路径，可以在上文中确定
#4.<priorit>为优先级。数字越大，优先级越高

root@raspberrypi:~ # update-alternatives --install /usr/bin/python python /usr/bin/python2.7 1
update-alternatives: 使用 /usr/bin/python2.7 来在自动模式中提供 /usr/bin/python (python)
root@raspberrypi:~ # update-alternatives --install /usr/bin/python python /usr/bin/python3.9 2
update-alternatives: 使用 /usr/bin/python3.9 来在自动模式中提供 /usr/bin/python (python)
root@raspberrypi:~ # update-alternatives --install /usr/bin/python python /usr/local/bin/python3.10 3
update-alternatives: 使用 /usr/local/bin/python3.10 来在自动模式中提供 /usr/bin/python (python)
```

至此，系统已默认Python版本为3.10，验证如下：
```shell
root@raspberrypi:~ # python
Python 3.10.0 (default, Dec  5 2021, 22:46:09) [GCC 10.2.1 20210110] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

### 3. 进行版本切换#
使用update-alternatives --config python命令即可
```shell
root@raspberrypi:~ # update-alternatives --config python
有 3 个候选项可用于替换 python (提供 /usr/bin/python)。

  选择       路径                     优先级  状态
------------------------------------------------------------
* 0            /usr/local/bin/python3.10   3         自动模式
  1            /usr/bin/python2.7          1         手动模式
  2            /usr/bin/python3.9          2         手动模式
  3            /usr/local/bin/python3.10   3         手动模式

要维持当前值[*]请按<回车键>，或者键入选择的编号：2
update-alternatives: 使用 /usr/bin/python3.9 来在手动模式中提供 /usr/bin/python (python)
root@raspberrypi:~ # python
Python 3.9.2 (default, Feb 28 2021, 17:03:44) 
[GCC 10.2.1 20210110] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> 
```

## 参考链接：
月灯依旧：[怎样在Debian 10上安装Python 3.9](https://bynss.com/linux/455663.html#)
weixin_39634876：[python升级命令debian_如何将 Debian Linux 中的默认的 Python 版本切换为替代版本](https://blog.csdn.net/weixin_39634876/article/details/110689901)
YanniZhang的博客：[linux 查看python安装路径,版本号](https://blog.csdn.net/jenyzhang/article/details/49646641)
