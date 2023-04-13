import mysql.connector
from com.antonsibgatulin.theory.Theory import TheoryModel
from com.antonsibgatulin.user.User import User
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="rus"
)



if conn:
    print ("Connected Successfully")
else:
    print ("Connection Not Established")
    exit()



def parseUser(data):
    return User(data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10])



def getUser(id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM `tguser` WHERE `userID` = "+str(id)+" LIMIT 1")
    for x in cursor:
        if x==None:
            cursor.close()
            return None
        else:
            cursor.close()
            return parseUser(x)

def getUserByMessage(message):
    user = getUser(message.from_user.id)
    if user == None:
        userId = message.from_user.id
        name = message.from_user.first_name
        username = message.from_user.username
        regUser(userId, name, username)
        return getUser(userId)
    else:
        return user

def getUserByMessageVk(user_id,vk_session):
    if(user_id<0):
        user_id = -user_id

    user = getUser(-user_id)
    if user == None:
        res = vk_session.method("users.get", {"user_ids": user_id,"fields":"domain"})[0]

        userId = -user_id
        name = res['first_name']
        username = res['domain']
        regUser(userId, name, username)
        return getUser(userId)
    else:
        return user
    pass

def regUser(id,name,username):
    user = getUser(id)
    if user != None:
        return
    cursor = conn.cursor()
    val = (name,username)
    cursor.execute("INSERT INTO `tguser`(`id`, `userID`, `name`, `username`, `wordId`, `categoryId`,`started`,`counts`,`index_w`,`ac`,`un`) VALUES (NULL,"+str(id)+",%s,%s,0,0,0,0,0,0,0)",val)
    conn.commit()
    cursor.close()


#print(getUser(2147483647))

def updateUserCategoryId(user,categoryId):
    cursor = conn.cursor()
    cursor.execute(f'UPDATE `tguser` SET `categoryId` = {categoryId} WHERE `userID` = {user}')

    conn.commit()
    cursor.close()



def generateWord(user):
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM `words` WHERE `type`= {user.categoryId} ORDER BY RAND() LIMIT 1')
    for i in cursor:
        user.wordId=i[0]
        user.index_w+=1
        user.started=1
        return i[1] ,i[4],i[6]


def updateUserCount(from_user, param):
    cursor = conn.cursor()
    cursor.execute(f'UPDATE `tguser` SET `counts` = {param} WHERE `userID` = {from_user.id}')
    print("dt")
    conn.commit()
    cursor.close()


def updateNewWordFromUser(user):
    cursor = conn.cursor()
    cursor.execute(f'UPDATE `tguser` SET `wordId` = {user.wordId} , `index_w` = {user.index_w},`started` = {user.started} WHERE `userID` = {user.id}')
    conn.commit()
    cursor.close()

def create_history_test(user):
    cursor = conn.cursor()
    cursor.execute(f'INSERT INTO `tgtest`(`id`, `userId`, `ac`, `un`, `categoryId`) VALUES (NULL,{user.id},{user.ac},{user.un},{user.categoryId})');
    conn.commit()
    cursor.close()

def create_word_dump(word,user,accept,youranswer):
    if accept:
        accept = 1
    else:
        accept = 0
    cursor = conn.cursor()
    cursor.execute(f'INSERT INTO `tgword`(`id`, `wordId`, `userId`, `fine`, `answer`,`youranswer`) VALUES (NULL,{user.wordId},{user.id},{accept},"{word}","{youranswer}")',);
    conn.commit()
    cursor.close()

def checkAnswer(user,text):
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM `words` WHERE `id` = {user.wordId} LIMIT 1')
    for x in cursor:
        if user.categoryId == 3:
            if text == x[6]:
                return True,x[2],x[5]
            else:
                return False,x[2],x[5]
        ans = x[6].upper()
        if x[3] == 4:
            if x[1] == x[2]:
                ans="Д".upper()
            else:
                ans="Н".upper()

        if ans==text.upper():
            cursor.close()
            return True,x[2],x[5]
        else:
            cursor.close()
            return False,x[2],x[5]


def updateAllUser(user):
    cursor = conn.cursor()
    cursor.execute(f'UPDATE `tguser` SET `ac` = {user.ac},`un` = {user.un}, `counts` = {user.counts},`categoryId` = {user.categoryId}, `wordId` = {user.wordId} , `index_w` = {user.index_w},`started` = {user.started} WHERE `userID` = {user.id}')
    conn.commit()
    cursor.close()

def getTheoryModel(type):
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM `theory` WHERE `type` = {type} LIMIT 1')
    for x in cursor:
        if x == None:
            return None
        return TheoryModel(x[1],x[2])