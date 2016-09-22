#!/usr/bin/python
import datetime

import telebot

bot = telebot.TeleBot("241532263:AAG6OidLQs6sCUPT8et_O5SZXKHz0-Du3K8")

def check_str(*args):
  def mycheck_str(message):
    for i in args:
      if message.text == i:
         return True
    return False 
  return mycheck_str

@bot.message_handler(commands = ['start', 'help'])
def send_welcome(message):
  bot.reply_to(message, "hello, have a nice day!")

@bot.message_handler(check_str('t', 'time'))
def show_time(message):
  d = datetime.datetime.now()
  bot.reply_to(message, repr(d))

@bot.message_handler(func=lambda m: True)
def echo_all(message):
  bot.reply_to(message, message.text)


bot.polling()
