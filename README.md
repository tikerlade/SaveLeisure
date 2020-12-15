

# [SaveLeisure](http://t.me/SaveLeisureBot) :robot:

[comment]: <> ([![codecov]&#40;https://codecov.io/gh/tikerlade/SaveLeisure/branch/main/graph/badge.svg?token=I8T7ALFRTX&#41;]&#40;https://codecov.io/gh/tikerlade/SaveLeisure&#41;)
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

Пользовательские истории:

 1. Я как пользователь Telegram, узнав об интересном фильме/книге или узнав полезную информацию, хочу сохранить название или сделать заметку соответственно, чтобы в нужный момент легко найти фильм/книгу или интересующую запись.
 2. Как пользователь Telegram, которому написали название фильма/книги, заинтересовав при этом описанием, я хочу сохранить название, переслав сообщение в диалог с ботом SaveLeisure, чтобы после быстро найти интересующий фильм или книгу, не вспоминая слова, по которым можно отыскать это в диалоге с человеком.

**Разработка архитектуры и детальное проектирование**

 1. System Context diagram
<img src="https://i.imgur.com/FbwfdM5.png" width="161" height="471">

 2. Container diagram
 <img src="https://i.imgur.com/tPhWYWU.png" width="681" height="726">



**Кодирование и отладка**

Весь код написан на языке Python. Использовались следующие технологии:
* [python-telegram-bot](https://python-telegram-bot.readthedocs.io/en/stable/index.html) - библиотека для написания бота от Telegram
* [heroku](https://dashboard.heroku.com/apps) - хостинг, для работы бота
* [PostgreSQL](https://www.postgresql.org/) - база данных



**Тестирование**
Некоторые Unit и Integration тесты находятся в директории tests. Их можно собрать и запустить как и любой .py файл.
Тестовые сценарии, которые использовались при мануальном тестировании:
| # | Action |  Expected result | Status
| --- | --- | --- | --- |
| 1 |Открыть бота в первый раз| Бот присылает приветственное сообщение | Passed :heavy_check_mark:
| 2 | Отправить боту команду /start | Бот присылает содержимое команды /help - полезную информацию | Passed :heavy_check_mark:
| 3 | Отправить боту команду /new или нажать на кнопку Add new item | Бот присылает сообщение, в котором просит выбрать категорию информации, которую мы хотим сохранить | Passed :heavy_check_mark:
| 4 | Выбрать категорию |  Бот просит отправить ему информацию | Passed :heavy_check_mark:
| 5 | Отправить боту сообщение | Бот отправляет сообщение о том, что информация сохранена и предлагает дальнейшие действия | Passed :heavy_check_mark:
| 6 | В главном меню бота выбрать Get my items | Бот предлагает выбрать категорию информации для вывода | Passed :heavy_check_mark:
| 7 | Выбрать категорию | Бот предлагает ввести количество сообщений, который он должен переслать | Passed :heavy_check_mark:
| 8 | Ввести количество | Бот пересылает нужное количество сообщений | Passed :heavy_check_mark:
| 9 | Ввести /unread | Бот не удаляет пересланные сообщения из БД | Passed :heavy_check_mark:
| 10 | Выйти из бота | Бот присылает сообщение bye-bye | Passed
| 11 | Переслать боту сообщение из другого диалога | Бот предлагает выбрать категорию, к которой относится выбранное сообщение | Passed :heavy_check_mark:
| 12 | Выбрать категорию | Бот сохраняет данные | Passed :heavy_check_mark:
| 13 | Нажать на кнопку Information или ввести /info | Бот сохраняет данные | Passed :heavy_check_mark:

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
| Чучин Дмитрий  | [@CapitanJamesFlint](http://t.me/CapitanJamesFlint)|
| Шевелев Роман | [@rmnshv](http://t.me/rmnshv)| 
| Егоров Матвей | [@mattopewd](http://t.me/mattopewd)| 
