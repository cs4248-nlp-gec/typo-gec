# typo-gec

This repository contains the code for CS4248 Project.

## Setup guide

Please install gector from the offical repository. The model has been tested on python3.7.

```bash
sudo apt install software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.7

git clone https://github.com/grammarly/gector
cd gector

# create a virtual venv
python3 -m venv venv
source venv/bin/activate # on linux machine

# install the requirements
python -m pip install -r requirements.txt
```

If you experienced any errors during the installation process, feel free to reach out.
