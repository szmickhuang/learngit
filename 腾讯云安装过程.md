# 安装python3.8.5
- yum install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gcc make libffi-devel
- yum groupinstall "Development Tools"
- yum install python-devel
- yum update
- wget http://npm.taobao.org/mirrors/python/3.8.5/Python-3.8.5.tgz
- tar xvf Python3.8.5.tgz
- cd Python3.8.5
- ./configure
- make
- make install
- ln -s /usr/local/bin/python3 /usr/bin/python3
- ln -s /usr/local/bin/pip3 /usr/bin/pip3
- 修改两个文件
vi /usr/bin/yum
	#!/usr/bin/python 改为 #!/usr/bin/python2.7
vi /usr/libexec/urlgrabber-ext-down
	#! /usr/bin/python 改为 #! /usr/bin/python2.7
- rm -f /usr/bin/python
- ln -s /usr/bin/python3 /usr/bin/python
- ln -s /usr/bin/pip3 /usr/bin/pip
- python -m pip install --upgrade pip
- python -m pip install --upgrade setuptools

# 安装node.js
- cd /usr/local
- wget https://nodejs.org/dist/v114.8.0/node-v14.8.0.1-linux-x64.tar.xz
- tar xvf node-v14.8.0-linux-x64.tar.xz
- ln -s /usr/local/node-v14.8.0-linux-x64/bin/npm .
- ln -s /usr/local/node-v14.8.0-linux-x64/bin/node .

# 安装akshare、baostock以及virtualenv
- python -m pip install akshre
- python -m pip install baostock
- python -m pip install virtualenv

# 安装jupyterlab
- pip install jupyterlab
- mkdir /data/jupyter
- mkdir /data/jupyter/root
- cd /data/jupyter
- python -c "import IPython; print(IPython.lib.passwd())"
输入自定义密码，生成sha1串: sha1:c70ff9706539:0deebacedca7300f8aa4bd541d6d2bea946eeea8
- jupyter lab --generate-config --allow-root
- jupyter lab --generate-config --allow-root
- vi /root/.jupyter/jupyter_notebook_config.py
	更改项目：
	c.NotebookApp.ip = '*'
	c.NotebookApp.allow_root = True
	c.NotebookApp.open_browser = False
	c.NotebookApp.port = 8347
	c.NotebookApp.password = u'sha1:c70ff9706539:0deebacedca7300f8aa4bd541d6d2bea946eeea8'
	c.ContentsManager.root_dir = '/data/jupyter/root'

# 解决导入pandas提示:Could not import the lzma modle的问题
- yum install xz-devel
- yum install python-backports-lzma
- pip install backports.lzma
- vi /usr/local/lib/python3.8/lzma.py
	把第27行
		from _lzma import *
		from _lzma import _encode_filter_properties, _decode_filter_properties
	改为：
		try:
			from _lzma import *
			from _lzma import _encode_filter_properties, _decode_filter_properties
		except:
			from backports.lzma import *
			from backports.lzma import _encode_filter_properties, _decode_filter_properties

# python -m pip install --upgrade xxx 需要更改参数
- python -m pip install --upgrade --use-feature=2020-resolver xxx

# 启动jupyterlab
- jupyter lab build
- nohup jupyter lab &

# jupyter lab build fail 的出错信息

[LabBuildApp] Building jupyterlab assets (build:prod:minimize)
Build failed.
Troubleshooting: If the build failed due to an out-of-memory error, you
may be able to fix it by disabling the `dev_build` and/or `minimize` options.

If you are building via the `jupyter lab build` command, you can disable
these options like so:

jupyter lab build --dev-build=False --minimize=False

You can also disable these options for all JupyterLab builds by adding these
lines to a Jupyter config file named `jupyter_config.py`:

c.LabBuildApp.minimize = False
c.LabBuildApp.dev_build = False

If you don't already have a `jupyter_config.py` file, you can create one by
adding a blank file of that name to any of the Jupyter config directories.
The config directories can be listed by running:

jupyter --paths

Explanation:

- `dev-build`: This option controls whether a `dev` or a more streamlined
`production` build is used. This option will default to `False` (ie the
`production` build) for most users. However, if you have any labextensions
installed from local files, this option will instead default to `True`.
Explicitly setting `dev-build` to `False` will ensure that the `production`
build is used in all circumstances.

- `minimize`: This option controls whether your JS bundle is minified
during the Webpack build, which helps to improve JupyterLab's overall
performance. However, the minifier plugin used by Webpack is very memory
intensive, so turning it off may help the build finish successfully in
low-memory environments.

An error occured.
RuntimeError: JupyterLab failed to build
See the log file for details:  /tmp/jupyterlab-debug-50si0k_u.log