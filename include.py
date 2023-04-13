import random
book_array = ['📕','📗','📘','📙','📚']
smile_array = ['🤧','🤤','😌','🙃','☺','❤','😇','🙂','🤪']
accept_word = ['🟢Правильно🟢',"✅Верно✅","Браво✔","❤У тебя хорошо получается❤","Успех‍🔥","💚ЕГЭ по русскому на 100 баллов💚"]
unaccept_word = ['Не повезло❌',"Не верно🔴","На ЕГЭ всё будет🆘","Не отчаивайся✖","Нет🚫","🔻Попробуй ещё раз!🔻"]



def getAnswer(ac,un):
    all = ac+un
    win = ac*100/all
    if win==100:
        return "Браво"+getRand(smile_array)
    if(win>75):
        return "Хорошо"+getRand(book_array)
    if win>50:
        return "Тебе стоит потренироваться"+getRand(book_array)
    if(win>20):
        return "📕Тебе стоит зучить теорию!📚"
    else:
        return getRand(unaccept_word)


def getRand(arr):
    return arr[random.randint(0,len(arr))-1]

def beautify_text(text,maxsize = 100):
    text = text.split(" ")
    end = int(len(text)/2)

    if end>maxsize:
        end = maxsize
    for g in range(random.randint(5,end)):
        i = random.randint(0,len(text)-1)
        if i % 2 == 0 or i%4 == 0 or i%5 == 0:
            text[i]=text[i]+getRand(smile_array)
        else:
            text[i] = text[i]+getRand(book_array)
    return " ".join(text)



def randomUdarWord(word):
    w = word.lower()
    a = ["и","я","ё","о","а","э","ы","ю","у","е"]
    pie = getRand(a)
    if pie in list(w):
        w =  w.replace(pie,pie.upper(),1)
        if w == word:
            return randomUdarWord(word)
        else:
            return w
    else:
        return randomUdarWord(word)
