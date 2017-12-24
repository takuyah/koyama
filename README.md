# Koyama Alert
This is a notification system for the Koyama Driving School reservation system.
Use at your own risk.

## 0. Prerequisites
You'll need either:
    * A channel on your LINE Developer account.
    * A channel and an access token on Pushbullet

## 1. Clone this repo.

## 2. Install dependencies:
```shp
cd (to this repo)
virtualenv . --python=python2.7
source bin/activate
pip2 install bs4 mechanize requests pushbullet.py
```

## 3. Set environment variables:
```sh
export KOYAMA_PUSH_MODE="line"  # line/pushbullet/both
export KOYAMA_LOC="shakujii"    # futakotamagawa/seijo/shakujii/akitsu/tsunashima
export KOYAMA_ID="(your ID)"
export KOYAMA_PW="(your password)"
export LINE_MY_ID="(your LINE developer user ID)"
export LINE_CHANNEL_TOKEN="(your LINE channel access token)"
export PUSHBULLET_TOKEN="(your Pushbullet access token)"
```

## 4. Go!
```sh
python2 koyama.py
```

## 5. (optional) Create a deployment package for AWS Lambda:

```sh
cd (to this repo)
source bin/activate
source package.sh
```