
### Getting Started

Download and install [Raspbian Jessie Lite](https://www.raspberrypi.org/downloads/raspbian/) onto an SD Card

Start up Raspbian

```
cd ~
mkdir .venvs
sudo apt-get update
sudo apt-get install python-dev virtualenv
# this should install Python 3.4
python3 --version # for verification
cd ~/.venvs
virtualenv -p python3 pi
. pi/bin/activate

cd /home/pi/apps/louver_project/pi
pip install -r requirements.txt
```
