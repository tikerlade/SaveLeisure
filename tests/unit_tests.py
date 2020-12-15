import os

import unittest
import telebot


TELEGRAM_TOKEN = str(os.getenv("TELEGRAM_TOKEN"))
TEST_USER = str(os.getenv("TEST_USER"))
bot = telebot.TeleBot(TELEGRAM_TOKEN)


class TestMessageFirst(unittest.TestCase):
    def test_start(self):
        message = '\start'

        def handle(message):
            if (message == '\start'):
                bot.send_message(TEST_USER, "I'm a SaveLeisure :robot:, please talk to me :speech_balloon:!\n"
        "Currently I'm able only to echo your messages :hear_no_evil:")
                return(True)
        self.assertTrue(handle(message))


    def test_help(self):
        message = '\help'

        def handle(message):
            if (message == '\help'):
                bot.send_message(TEST_USER, "This is a bot :robot_face: for automation your basic routine of sending staff that you want to"
            " read :SOON_arrow: to your *Saved Messages* which will "
            "shortly become a mess :woozy_face: where you can't find anything.\n\n"
            "`Forwarding` - forward article that you like to bot and save it\n\n"
            "`/start` - start a conversation with this bot\n"
            "`/help` - here you are\n"
            "`/new` - add new item to your list\n"
            "`/get` - get items from your added items\n"
            "`/unread` - mark listed items as unread\n"
            "`/stats` - will give you general statistics\n"
            "`/end` - end current conversation\n\n"
            "`/new` & `/get` will give you options :gear_selector: to set everything as you need.\n\n"
            ":warning_selector: Developing is still in progress :warning_selector:")
                return (True)

        self.assertTrue(handle(message))

    def test_new_item(self):
        message = "/new_item"

        def handle(message):
            if message == '/new_item':
                bot.send_message(TEST_USER, "Okay :fire:, Tell me what is your item you want to add is about")
                return True
        self.assertTrue(handle(message))
