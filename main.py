# -*- coding: utf-8 -*-
import os
import random
from include import *
from com.antonsibgatulin.db import Database
import telebot
from telebot import types

import math

obj = {"tokenDebug":"",
       "tokenMain":""}
bot = telebot.TeleBot(obj['tokenMain'])


def startTest(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=1)
    btn1 = types.KeyboardButton("Начать тест"+book_array[random.randint(0,len(book_array))-1])
    btn2 = types.KeyboardButton("Теория" + book_array[random.randint(0, len(book_array)) - 1])

    markup.add(btn1,btn2)
    bot.send_message(message.from_user.id, beautify_text("Тысячи слов с ответами для подготовки к ЕГЭ–2023 по русскому языку. Система тестов для подготовки и самоподготовки к ЕГЭ.",5), reply_markup=markup)

def getButtonToStartTest(message):
    markup  =types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text="Корни",callback_data="t0")
    btn2 = types.InlineKeyboardButton(text="Приставки",callback_data="t1")
    btn3 = types.InlineKeyboardButton(text="Суффиксы",callback_data="t2")
    btn4 = types.InlineKeyboardButton(text="Ударения",callback_data="t3")
    btn5 = types.InlineKeyboardButton(text="Словосочетания",callback_data="t4")
    #btn6 = types.InlineKeyboardButton(text="Слитное написание слов",callback_data="t5")
    btn7 = types.InlineKeyboardButton(text="Правописание суффиксов и окончаний глагольных форм ",callback_data="t7")
    markup.add(btn1,btn2,btn3,btn4,btn5,btn7)
    bot.send_message(message.from_user.id,beautify_text("Привет! Я - тестер бота ЕГЭ по русскому языку с выбором заданий. Моя задача помочь Вам максимально эффективно использовать все возможности нашего портала и достичь наилучших результатов в подготовке к Единому Государственному экзамену.\n\nЯ готов помочь Вам с любыми вопросами, которые у Вас могут возникнуть. Чтобы начать работу со мной, просто напишите /start.\n\n" +"Я быстро отвечу на Ваши запросы и помогу с выбором нужных разделов для изучения. Например, Вы можете написать команду /theory, чтобы получить доступ к теоретическим материалам. Если же Вы захотите пройти моделирующий тест или проверочную работу, то напишите /tests.\n\nЕсли у Вас есть определенные вопросы по задачам или необходима помощь в их решении, Вы можете обратиться ко мне в чате. Я буду рад помочь Вам в процессе подготовки к экзамену.\n\nТакже, Вы можете найти полезную информацию по подготовке к ЕГЭ на страницах нашего сайта или обратиться к администратору для получения дополнительной консультации.\n\nНе откладывайте свою подготовку до последнего дня - начните уже сегодня! И не стесняйтесь обращаться ко мне за помощью и советом - я всегда готов Вам быстро ответить.\n\n",10),reply_markup=markup)


def getTheory(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text="Корни",callback_data="h0")
    btn2 = types.InlineKeyboardButton(text="Приставки",callback_data="h1")
    btn3 = types.InlineKeyboardButton(text="Суффиксы",callback_data="h2")
    btn4 = types.InlineKeyboardButton(text="Ударения",callback_data="h3")
    btn5 = types.InlineKeyboardButton(text="Правописание суффиксов и окончаний глагольных форм", callback_data="h7")
    markup.add(btn1,btn2,btn3,btn4,btn5)
    bot.send_message(message.from_user.id,"Выберите раздел теории"+getRand(book_array),reply_markup=markup)

def getCountWord(from_user):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Пуля - 30"+getRand(smile_array))
    btn2 = types.KeyboardButton("Блиц - 50"+getRand(smile_array))
    btn3 = types.KeyboardButton("Рапид - 100"+getRand(smile_array))
    btn4 = types.KeyboardButton("Классика - 150"+getRand(smile_array))
    btn5 = types.KeyboardButton("Шторм - 300"+getRand(smile_array))
    markup.add(btn1,btn2,btn3,btn4,btn5)
    bot.send_message(from_user.id,"Вабери кол-во слов!"+getRand(smile_array),reply_markup=markup)


def runWordId(message):
    user = Database.getUserByMessage(message)
    #if user.categoryId == 3:

    word,letter,fastanswer = Database.generateWord(user)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    if user.categoryId == 3:
        ran = None
        try:
            ran =randomUdarWord(fastanswer)
            #print(ran)
        except:
            runWordId(message)
            return
        arr = [fastanswer,ran]
        random.shuffle(arr)
        for x in arr:
            print(x)
            markup.add(types.KeyboardButton(x))
    else:
        for x in letter.upper():
            markup.add(types.KeyboardButton(x))
    bot.send_message(message.from_user.id,str(word).replace("x","...")+getRand(smile_array),reply_markup=markup)
    Database.updateNewWordFromUser(user)

def checkCheckCountOfWords(message):
    text = str(message.text)
    send = False
    if text.startswith("Пуля - 30"):
        send = True
        Database.updateUserCount(message.from_user, 30)
    if text.startswith("Блиц - 50"):
        send = True
        Database.updateUserCount(message.from_user,50)
    if text.startswith("Рапид - 100"):
        send = True
        Database.updateUserCount(message.from_user,100)
    if text.startswith("Шторм - 300"):
        send = True
        Database.updateUserCount(message.from_user,300)

    if send:
        runWordId(message)


def endUserTest(message,user, ac, un):
    if ac + un == 0:
        return
    bot.send_message(user.id,getAnswer(ac,un)+ " "+str(ac)+"/"+str(un)+"/"+str(ac+un)+" - "+str(ac/(ac+un)*100)+"%")
    startTest(message)

def restartUser(message,user):
    Database.create_history_test(user)
    user.index_w = 0
    user.counts = 0
    user.categoryId = -1
    user.wordId = 0
    user.started = 2

    ac = user.ac
    un = user.un

    user.ac = 0
    user.un = 0
    Database.updateAllUser(user)
    endUserTest(message, user, ac, un)

def nextWord(message,user):
    if user.index_w>=user.counts:
        restartUser(message,user)
    else:
        runWordId(message)



def checkLetter(message):
    h = list("АБВГДЕЁЖЗИКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ")
    #user = Database.getUserByMessage(message)
    text = str(message.text)
    user = Database.getUserByMessage(message)
    if user.wordId == None or user.wordId == 0 or user.counts == 0:
        return

    if text in h:


        answer,accept,someWord = Database.checkAnswer(user,text)
        if answer:
            bot.send_message(message.from_user.id,""+getRand(accept_word))
            user.ac+=1
        else:

            user.un+=1
            if user.categoryId == 4:
                user.un+=3
            bot.send_message(message.from_user.id, "" + getRand(unaccept_word)+" ("+accept+")")
        Database.create_word_dump(someWord,user,answer,text[0])
        Database.updateAllUser(user)
        nextWord(message,user)
    elif user.categoryId == 3:
        answer, accept, someWord = Database.checkAnswer(user, text)
        if answer:
            bot.send_message(message.from_user.id, "" + getRand(accept_word))
            user.ac += 1
        else:
            user.un += 1
            bot.send_message(message.from_user.id, "" + getRand(unaccept_word) + " (" + accept + ")")
        Database.create_word_dump(someWord, user, answer, text[0])
        Database.updateAllUser(user)
        nextWord(message, user)




@bot.message_handler(commands=['start'])
def start(message):
    Database.getUserByMessage(message)
    startTest(message)

@bot.message_handler(commands=['restart'])
def start(message):
    user = Database.getUserByMessage(message)
    restartUser(message,user)
    startTest(message)

@bot.message_handler(commands=['starttest'])
def start(message):
    user = Database.getUserByMessage(message)
    restartUser(message,user)
    getButtonToStartTest(message)



@bot.message_handler(commands=['testend'])
def start(message):
    user = Database.getUserByMessage(message)
    restartUser(message, user)


@bot.message_handler(commands=['theory'])
def start(message):
    getTheory(message)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    #print(message)
    if str(message.text).startswith("Начать тест"):
        getButtonToStartTest(message)

    if str(message.text).startswith("Теория"):
        getTheory(message)

    try:
        checkCheckCountOfWords(message)
        checkLetter(message)
    except:
        pass

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    data = call.data
    if str(data).startswith("t"):
        user = (Database.getUserByMessage(call))
        if(user == None or user.id == None):
            return

        Database.updateUserCategoryId(user.id, int(data[1]))
        getCountWord(call.from_user)

    if str(data).startswith("h"):
        theoryModel = Database.getTheoryModel(int(data[1]))
        if theoryModel == None:
            return
        text = theoryModel.text
        text = beautify_text(text)
        if len(text) > 4096:
            for x in range(int(len(text)/4096)+1):
                pie = text[x*4096:x*4096+4096]
                #print(pie)
                bot.send_message(call.from_user.id, pie)
        else:
            bot.send_message(call.from_user.id,theoryModel.text)

bot.polling(none_stop=True, interval=0) #обязательная для работы бота часть