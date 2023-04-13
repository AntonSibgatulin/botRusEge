class TheoryModel:
    def __init__(self,text,type):
        self.text = text
        self.type = type
    def __str__(self):
        return "[THEORY]: "+str(self.type)