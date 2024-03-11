
class PoMsg:
    def __init__(self, msgid, msgstr, prevcontext):
        self.msgid = msgid
        self.msgstr = msgstr
        self.prevcontext = prevcontext

    def join_lines(self, lines):
        result = ""
        for idx, msg in enumerate(lines):
            start = msg.find('"')+1
            end = msg.rfind('"')
            result += msg[start:end]
            if idx < len(lines)-1:
                result += ' '

        return result #.strip()

    def char_only(self, msg):
        result = ""
        for i in range(len(msg)):
            c = msg[i]
            if ('0' <= c <= '9') or ('a' <= c <= 'z') or ('A' <= c <= 'Z'):
                result += c.lower()

        return result

    def get_key(self):
        #return self.join_lines(self.msgid)
        return self.char_only(self.join_lines(self.msgid))

    def __str__(self):
        key = self.get_key()
        msgstr = self.join_lines(self.msgstr)
        return f'key: {key[0:50]}, str: {msgstr[0:50]}'

class PoMsgs:

    def __init__(self):
        self.array = []
        self.dict = {}

    def addPoMsg(self, pomsg):
        self.array.append(pomsg)
        self.dict[pomsg.get_key()] = pomsg


