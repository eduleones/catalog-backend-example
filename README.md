# catalog-backend-example
 Simple Example of a Catalog Backend
 
 ### Install in Ubuntu 18.04
 
 ##### Python 3.7.3 with Pyenv and Pyenv-virtualenv
 
 ```
sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev \
libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
xz-utils tk-dev libffi-dev liblzma-dev python-openssl git
```
```
curl https://pyenv.run | bash
git clone https://github.com/pyenv/pyenv-virtualenv.git $(pyenv root)/plugins/pyenv-virtualenv
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bash_profile
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bash_profile
$SHELL
```

```
pyenv install 3.7.3
pyenv virtualenv 3.7.3 catalog-backend
```

#### Up virtualenv
```
pyenv activate catalog-backend
```
