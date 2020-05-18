# 在自己的腾讯云服务器安装git服务器

##### 确认版本

```
[root@VM_0_12_centos ~]# cat /etc/redhat-release
CentOS Linux release 7.8.2003 (Core)
```

##### 设置用户 git

```
[root@VM_0_12_centos ~]# adduser git
[root@VM_0_12_centos ~]# passwd git
```

##### 删除系统原来的git

```
[root@VM_0_12_centos ~]# git --version
git version 1.8.3.1
[root@VM_0_12_centos ~]# yum remove git -y
```
卸载掉系统中原有版本的git，下面要替换为最新版本的git

##### 下载最新版本的git并安装

```
[root@VM_0_12_centos ~]# wget https://mirrors.edge.kernel.org/pub/software/scm/git/git-2.26.2.tar.gz
[root@VM_0_12_centos ~]# tar zxvf git-2.26.2.tar.gz
[root@VM_0_12_centos ~]# cd git-2.26.2/
[root@VM_0_12_centos git-2.26.2]# ./configure --prefix=/usr/local/git
[root@VM_0_12_centos git-2.26.2]# make && make install
[root@VM_0_12_centos git-2.26.2]# ln -s /usr/local/git/bin/* /usr/bin/
[root@VM_0_12_centos git-2.26.2]# git --version
git version 2.26.2
```

##### 安装gitosis

```
[root@VM_0_12_centos ~]# yum install python python-setuptools
Loaded plugins: fastestmirror, langpacks
Loading mirror speeds from cached hostfile
Package python-2.7.5-88.el7.x86_64 already installed and latest version
Package python-setuptools-0.9.8-7.el7.noarch already installed and latest version
Nothing to do
[root@VM_0_12_centos ~]# git clone git://github.com/res0nat0r/gitosis.git
Cloning into 'gitosis'...
remote: Enumerating objects: 734, done.
remote: Total 734 (delta 0), reused 0 (delta 0), pack-reused 734
Receiving objects: 100% (734/734), 147.40 KiB | 23.00 KiB/s, done.
Resolving deltas: 100% (458/458), done.
[root@VM_0_12_centos ~]# cd gitosis/
[root@VM_0_12_centos gitosis]# python setup.py install

```
看到以下信息即安装成功
```
......
Using /usr/lib/python2.7/site-packages
Finished processing dependencies for gitosis==0.2
```

##### 设置公钥

切换到git用户
```
[root@VM_0_12_centos ~]# su git
[git@VM_0_12_centos root]$ cd
[git@VM_0_12_centos ~]$ pwd
/home/git
[git@VM_0_12_centos ~]$ ssh-keygen -t rsa
Generating public/private rsa key pair.
Enter file in which to save the key (/home/git/.ssh/id_rsa): 
Created directory '/home/git/.ssh'.
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in /home/git/.ssh/id_rsa.
Your public key has been saved in /home/git/.ssh/id_rsa.pub.
The key fingerprint is:
SHA256:IFI7UygKJ92E3yxG6f5fi3F4JOEZi8eJ8pnfIa6Ymj4 git@VM_0_12_centos
The key's randomart image is:
+---[RSA 2048]----+
| . +oo.          |
|o =.=o           |
|.+.==o. o        |
|.  .=+o* *       |
|   o..o S .      |
|    .o + +       |
|     .+ + =      |
|  E. o.o O o     |
| .+oo .o= o      |
+----[SHA256]-----+
[git@VM_0_12_centos ~]$ mv .ssh/id_rsa.pub /home/git
```

留意这里主机名有下划线，gitosis对这个主机名支持不好，需要更改，我更改为 mickcentos 了

```
[git@mickcentos ~]$ gitosis-init < ./id_rsa.pub
Initialized empty Git repository in /home/git/repositories/gitosis-admin.git/
Reinitialized existing Git repository in /home/git/repositories/gitosis-admin.git/
```

