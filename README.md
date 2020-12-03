# [SaveLeisure](http://t.me/SaveLeisureBot) :robot:
[![Build Status](https://travis-ci.com/tikerlade/SaveLeisure.svg?token=QXtXzRqKNghyH5soGYoY&branch=main)](https://travis-ci.com/tikerlade/SaveLeisure)
[![codecov](https://codecov.io/gh/tikerlade/SaveLeisure/branch/main/graph/badge.svg?token=I8T7ALFRTX)](https://codecov.io/gh/tikerlade/SaveLeisure)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


Telegram bot that will save interesting information that you send to it and which you want to read / watch later. Such information as a blogpost :page_with_curl:, film :movie_camera: or book :books:.

<img src="https://github.com/tikerlade/SaveLeisure/blob/main/pics/adding_item.gif" width="243" height="500">

## Current stage :watch:
This is a bot :robot: for automation your basic routine of sending staff that you want to read :soon: to your **Saved Messages** which will shortly become a mess :dizzy_face: where you can't find anything.

All functions listed below except `Forwarding` are reachable from inline keyboads after `/start` command or texting to bot.

* `Forwarding` - forward article that you like to bot and save it with appropriate category
* `/start` - start a conversation with this bot\n"
* `/help` - here you are\n"
* `/new` - add new item to your list\n"
* `/get` - get items from your added items\n"
* `/unread` - mark listed items as unread\n"
* `/stats` - will give you general statistics\n"
* `/end` - end current conversation\n\n"
* `/new` & `/get` will give you options :gear_selector: to set everything as you need.\n\n"

":warning: Developing is still in progress :warning:"

## Running locally :computer:
To run this bot locally you need to

```shell script
git clone https://github.com/tikerlade/SaveLeisure.git
cd SaveLeisure
python -m venv env
source env/bin/activate
pip install -r requirements.txt
// Here initialize database
python bot/main.py --local
```

1. Clone this repository
2. Enable virtual environment & install requirements
3. :warning: Initialize database
4. :warning: Run bot with local parameter


> Bot :robot: is available by the following [link](http://t.me/SaveLeisureBot)
