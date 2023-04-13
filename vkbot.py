# -*- coding: utf-8 -*-
import vk_api
from com.antonsibgatulin.db import Database

from vk_api.longpoll import VkLongPoll,VkEventType

from include import *
from vk_api.keyboard import VkKeyboard,VkKeyboardColor
token = ""
vk_session = vk_api.VkApi(token=token)
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

def send_message(user_id,text,keyboard=None,attachment = None):
    post = {"user_id":user_id,"message":text,"random_id":0}
    if keyboard != None:
        post['keyboard'] = keyboard.get_keyboard()
    if attachment !=None:
        post['attachment'] = attachment

    vk_session.method("messages.send",post)




def getButtonToStartTest(message):
    keyword = VkKeyboard(False,False)
    keyword.add_button("Корни"+getRand(book_array),VkKeyboardColor.PRIMARY)
    keyword.add_line()
    keyword.add_button("Приставки"+getRand(book_array),VkKeyboardColor.PRIMARY)
    keyword.add_line()
    keyword.add_button("Суффиксы"+getRand(book_array),VkKeyboardColor.PRIMARY)
    keyword.add_line()
    keyword.add_button("Ударения"+getRand(book_array),VkKeyboardColor.PRIMARY)
    keyword.add_line()
    keyword.add_button("Словосочетания"+getRand(book_array),VkKeyboardColor.PRIMARY)
    keyword.add_line()
    keyword.add_button("Cуффиксы и окончания глагольных форм"+getRand(book_array),VkKeyboardColor.PRIMARY)

    send_message(message.user_id,beautify_text("Привет! Я - тестер бота ЕГЭ по русскому языку с выбором заданий. Моя задача помочь Вам максимально эффективно использовать все возможности нашего портала и достичь наилучших результатов в подготовке к Единому Государственному экзамену.\n\nЯ готов помочь Вам с любыми вопросами, которые у Вас могут возникнуть. Чтобы начать работу со мной, просто напишите /start.\n\n" +"Я быстро отвечу на Ваши запросы и помогу с выбором нужных разделов для изучения. Например, Вы можете написать команду /theory, чтобы получить доступ к теоретическим материалам. Если же Вы захотите пройти моделирующий тест или проверочную работу, то напишите /tests.\n\nЕсли у Вас есть определенные вопросы по задачам или необходима помощь в их решении, Вы можете обратиться ко мне в чате. Я буду рад помочь Вам в процессе подготовки к экзамену.\n\nТакже, Вы можете найти полезную информацию по подготовке к ЕГЭ на страницах нашего сайта или обратиться к администратору для получения дополнительной консультации.\n\nНе откладывайте свою подготовку до последнего дня - начните уже сегодня! И не стесняйтесь обращаться ко мне за помощью и советом - я всегда готов Вам быстро ответить.\n\n",10),keyboard=keyword)




def getTheory(message):
    keyword = VkKeyboard(False,False)
    keyword.add_button("Теория - Корни"+getRand(book_array),VkKeyboardColor.PRIMARY)
    keyword.add_button("Теория - Приставки"+getRand(book_array),VkKeyboardColor.PRIMARY)
    keyword.add_line()
    keyword.add_button("Теория - Суффиксы"+getRand(smile_array),VkKeyboardColor.PRIMARY)
    keyword.add_button("Теория - Ударения"+getRand(book_array),VkKeyboardColor.PRIMARY)
    keyword.add_line()
    #keyword.add_button("Теория - Словосочетания"+getRand(book_array),VkKeyboardColor.PRIMARY)
    #keyword.add_line()
    keyword.add_button("Теория - Cуффиксы и окончания"+getRand(book_array),VkKeyboardColor.PRIMARY)
    keyword.add_button("Начать тест" + getRand(smile_array), VkKeyboardColor.PRIMARY)

    send_message(message.user_id,"Выберите раздел теории"+getRand(book_array),keyboard=keyword)



def getCountWord(from_user):
    keyword = VkKeyboard(True,False)
    keyword.add_button("Пуля - 30"+getRand(smile_array),VkKeyboardColor.SECONDARY)
    keyword.add_button("Блиц - 50" + getRand(smile_array), VkKeyboardColor.SECONDARY)
    keyword.add_line()
    keyword.add_button("Рапид - 100" + getRand(smile_array), VkKeyboardColor.SECONDARY)
    keyword.add_button("Классика - 150" + getRand(smile_array), VkKeyboardColor.SECONDARY)
    keyword.add_line()
    keyword.add_button("Шторм - 300" + getRand(smile_array), VkKeyboardColor.SECONDARY)

    send_message(from_user.user_id,"Вабери кол-во слов!"+getRand(smile_array),keyboard=keyword)



def startTest(event):
    user = Database.getUserByMessageVk(event.user_id,vk_session)
    keyboard = VkKeyboard()
    keyboard.add_button("Начать тест"+book_array[random.randint(0,len(book_array))-1],VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button("Теория",VkKeyboardColor.PRIMARY)
    send_message(event.user_id, beautify_text("Тысячи слов с ответами для подготовки к ЕГЭ–2023 по русскому языку. Система тестов для подготовки и самоподготовки к ЕГЭ.",5), keyboard=keyboard)


def setTaskVk(event,id):
    user = (Database.getUserByMessageVk(event.user_id,vk_session))
    if (user == None or user.id == None):
        return

    Database.updateUserCategoryId(user.id, int(id))
    getCountWord(event)




def runWordId(message):
    user = Database.getUserByMessageVk(message.user_id,vk_session)
    #if user.categoryId == 3:

    word,letter,fastanswer = Database.generateWord(user)
    keyboard = VkKeyboard(False,False)
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
            keyboard.add_button(x,VkKeyboardColor.PRIMARY)
            #keyboard.add_line()
    else:
        for x in letter.upper():
            keyboard.add_button(str(x), VkKeyboardColor.PRIMARY)
            #keyboard.add_line()

    send_message(message.user_id,str(word).replace("x","...")+getRand(smile_array),keyboard=keyboard)
    Database.updateNewWordFromUser(user)


def checkCheckCountOfWords(message):
    text = str(message.text)
    user = Database.getUserByMessageVk(message.user_id,vk_session)
    send = False
    user_id=-message.user_id
    if text.startswith("Пуля - 30"):
        send = True
        Database.updateUserCount(user, 30)
    if text.startswith("Блиц - 50"):
        send = True
        Database.updateUserCount(user,50)
    if text.startswith("Рапид - 100"):
        send = True
        Database.updateUserCount(user,100)
    if text.startswith("Шторм - 300"):
        send = True
        Database.updateUserCount(user,300)

    if send:
        runWordId(message)




def endUserTest(message,user, ac, un):
    if ac + un == 0:
        return
    send_message(abs(user.id),getAnswer(ac,un)+ " "+str(ac)+"/"+str(un)+"/"+str(ac+un)+" - "+str(ac/(ac+un)*100)+"%")
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
    user = Database.getUserByMessageVk(message.user_id,vk_session)
    if user.wordId == None or user.wordId == 0 or user.counts == 0:
        return

    if text in h:


        answer,accept,someWord = Database.checkAnswer(user,text)
        if answer:
            send_message(message.user_id,""+getRand(accept_word))
            user.ac+=1
        else:

            user.un+=1
            if user.categoryId == 4:
                user.un+=3
            send_message(message.user_id, "" + getRand(unaccept_word)+" ("+accept+")")
        Database.create_word_dump(someWord,user,answer,text[0])
        Database.updateAllUser(user)
        nextWord(message,user)
    elif user.categoryId == 3:
        answer, accept, someWord = Database.checkAnswer(user, text)
        if answer:
            send_message(message.user_id, "" + getRand(accept_word))
            user.ac += 1
        else:
            user.un += 1
            send_message(message.user_id, "" + getRand(unaccept_word) + " (" + accept + ")")
        Database.create_word_dump(someWord, user, answer, text[0])
        Database.updateAllUser(user)
        nextWord(message, user)


def getTheoryMessage(event,id):
    theoryModel = Database.getTheoryModel(int(id))
    if theoryModel == None:
        return
    text = theoryModel.text
    text = beautify_text(text)
    if len(text) > 4096:
        for x in range(int(len(text) / 4096) + 1):
            pie = text[x * 4096:x * 4096 + 4096]
            # print(pie)
            send_message(event.user_id, pie)
    else:
        send_message(event.user_id, theoryModel.text)

def get_text_messages(event):
    #print(message)
    if str(event.text).startswith("Начать тест"):
        getButtonToStartTest(event)
        pass

    try:
        checkCheckCountOfWords(event)
        checkLetter(event)
    except:
        pass

    if str(event.text)==("Теория"):
        getTheory(event)

    #check task
    if str(event.text).startswith("Корни"):
        setTaskVk(event, 0)
        pass
    if str(event.text).startswith("Приставки"):
        setTaskVk(event, 1)
        pass
    if str(event.text).startswith("Суффиксы"):
        setTaskVk(event, 2)
        pass
    if str(event.text).startswith("Ударения"):
        setTaskVk(event, 3)
        pass
    if str(event.text).startswith("Словосочетания"):
        setTaskVk(event, 4)
        pass
    if str(event.text).startswith("Cуффиксы и окончания глагольных форм"):
        setTaskVk(event, 7)
        pass





    if str(event.text).startswith("Теория - Корни"):
        getTheoryMessage(event,0)
        pass
    if str(event.text).startswith("Теория - Приставки"):
        getTheoryMessage(event,1)
        pass
    if str(event.text).startswith("Теория - Суффиксы"):
        getTheoryMessage(event,2)
        pass
    if str(event.text).startswith("Теория - Ударения"):
        getTheoryMessage(event,3)
        pass
    #if str(event.text).startswith("Теория - Словосочетания"):
    #    setTaskVk(event,4)
    #    pass
    if str(event.text).startswith("Теория - Cуффиксы и окончания"):
        getTheoryMessage(event,7)
        pass

def startCommandListener(event):
    msg = event.text.replace("/","",1)
    if msg == "start" or msg == "Начать":
        Database.getUserByMessageVk(event.user_id,vk_session)
        startTest(event)
        pass
    if msg == "theory":
        getTheory(event)
        pass

    if msg == "testend":
        user = Database.getUserByMessageVk(event.user_id,vk_session)
        restartUser(event, user)

    if msg == "starttest":
        user = Database.getUserByMessageVk(event.user_id,vk_session)
        restartUser(event, user)
        getButtonToStartTest(event)

    if msg == "restart":
        user = Database.getUserByMessageVk(event.user_id,vk_session)
        restartUser(event, user)
        startTest(event)

    pass


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        if event.to_me:
            msg = event.text
            user_id = event.user_id
            if event.from_user:

                rand = random.randint(0,300)
                if rand == 1:
                    send_message(event.user_id,"",attachment="wall-219474215_6")

                if str(msg).startswith("/") or msg=="Начать":
                    startCommandListener(event)
                else:
                    get_text_messages(event)





