Vagrant.configure("2") do |config|
  config.vm.box = "hashicorp/bionic64"

  config.vm.provision "shell", privileged: false, inline: <<-SHELL

  sudo apt-get update

  # TODO: Install pyenv prerequisites 

  echo Y | sudo apt-get install make build-essential libssl-dev zlib1g-dev \
  libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm \
  libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

  echo Y | sudo apt install libedit-dev

  # TODO: Install pyenv

  git clone https://github.com/pyenv/pyenv.git ~/.pyenv
  cd ~/.pyenv && src/configure && make -C src
  
  echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.profile
  echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.profile
  echo 'eval "$(pyenv init --path)"' >>~/.profile
  
  echo 'eval "$(pyenv init -)"' >> ~/.bashrc
  . ~/.profile
  pyenv install 3.8.5
  pyenv global 3.8.5

  curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

  SHELL

  config.vm.network "forwarded_port", guest: 5000, host: 5000

  config.trigger.after :up do |trigger|
    trigger.name = "Launching App"
    trigger.info = "Running the TODO app setup script" 
    trigger.run_remote = {privileged: false, inline: "
    # Install dependencies and launch
      cd /vagrant
      poetry install
      nohup poetry run flask run --host=0.0.0.0 > logs.txt 2>&1 &
    "}
  end
  
end
