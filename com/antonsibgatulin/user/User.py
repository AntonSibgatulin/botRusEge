class User:
    def __init__(self,id,name,username,wordId=None,categoryId=None,started=None,counts=None,index_w=None,ac=None,un=None):
        self.id = id
        self.name = name
        self.username = username
        self.wordId=wordId
        self.categoryId = categoryId
        self.started = started
        self.counts = counts
        self.index_w = index_w
        self.ac = ac
        self.un = un

    def __str__(self):
        return "[USER]: "+str(self.id)+" "+self.name+" @"+self.username