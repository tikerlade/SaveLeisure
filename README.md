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

## Конструирование ПО
**Определение проблемы**

В мессенджере Telegram все нужные сообщения можно сохранять в отдельный диалог *Saved Messages*. Также туда можно загрузить неограниченное количество файлов, то есть мессенджер предоставляет бесконечное облако. 

Многие люди пользуются этой функцией, пересылая сообщения в этот диалог, чтобы в будущем снова к ним обратиться. Зачастую, на поиск нужного сообщения в диалоге уходит очень много времени.  

Решить эту проблему поможет Telegram бот, который расширяет функционал диалога *Saved Messages*. Мы можем отправить/переслать боту сообщение (это может быть название книги, ссылка на статью, фильм и так далее), а он спросит нас, к какой категории относится это сообщение, и сохранит данные. Когда нам снова захочется обратиться к данным, мы можем запросить их у бота, выбрав категорию и количество пересланных сообщений.

**Выработка требований**
TODO: mattopewd

**Разработка архитектуры и детальное проектирование**
Вам нужно будет реализовать для вашего проекта первые две диаграммы из подхода https://c4model.com/
TODO: mattopewd

**Кодирование и отладка**
Весь код написан на языке Python. Использовались следующие технологии:
TODO: tikerlade

**Unit тестирование**
TODO: rmnshv

**Интеграционное тестирование**
TODO: rmnshv

**Сборка**
Чтобы запустить бота локально, придется немного попотеть :smile:.
1. Склонировать репозиторий.
2. Обеспечить виртуально окружение и установить необходимые средства.
3. Инициализировать базы данных.
4. Запустить бота с параметром --local.
```shell script
git clone https://github.com/tikerlade/SaveLeisure.git
cd SaveLeisure
python -m venv env
source env/bin/activate
pip install -r requirements.txt
// Here initialize database
python bot/main.py --local
```
Чтобы не ломать себе жизнь, можете просто открыть бота по ссылке:
> Bot :robot: is available by the following [link](http://t.me/SaveLeisureBot)

**Участники проекта**
| Имя | Telegram | 
| --- | --- |
| Кузнецов Иван |[@kuznetsof_ivan](http://t.me/kuznetsof_ivan)|
| Чучин Дмитрий  | [@CapitanJamesFlint](http://t.me/CapitanJamesFlint) |
| Шевелев Роман | [@rmnshv](http://t.me/rmnshv) | 
| Егоров Матвей | [@mattopewd](http://t.me/mattopewd) | 


