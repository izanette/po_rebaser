
class PoMsg:
    def __init__(self, msgid, msgstr, prevcontext):
        self.msgid = msgid
        self.msgstr = msgstr
        self.prevcontext = prevcontext

class PoMsgs:

    def __init__(self):
        self.array = []
        self.dict = {}
    def addPoMsg(self, pomsg):
        self.array.append(pomsg)
        self.dict[pomsg.msgid] = pomsg