import znc
import re

class antiping(znc.Module):
    description = "If someone writes you an empty ping this will ask them to provide more context."

    directantiping = re.compile('ping\Z',re.IGNORECASE)

    def OnChanMsg(self, nick, channel, message):
        self.process(nick, channel, message)
        return znc.CONTINUE

    def OnPrivMsg(self, nick, message):
        self.process(nick, None, message)
        return znc.CONTINUE

    def removeNoop(self, text):
       chars = ":.!? "
       for c in chars:
         if c in text:
            text = text.replace(c, "")
       return text

    def isPrivAntiPing(self, message):
        raw = message.s
        # remove current nick to handle messages that mention me directly
        raw = raw.replace(self.GetNetwork().GetCurNick(),'')

        raw = self.removeNoop(raw)

        if self.directantiping.match(raw):
           return True
        else:
           return False

    def isChannelAntiPing(self,message):
        return self.GetNetwork().GetCurNick() in message.s and self.isPrivAntiPing(message)

    def process(self, nick, channel, message):
        if channel is None:
           if self.isPrivAntiPing(message):
              self.PutModule('Antiping from {0}: "{1}"'.format(nick.GetNick(),message.s))
              self.PutIRC('PRIVMSG {0} : (auto-antiping) Thanks for pinging me, but please just ask the question you have and I will reply ASAP. Thanks.'.format(nick.GetNick()))
        else:
           if self.isChannelAntiPing(message):
              self.PutModule('Antiping from {0} in {1}: {2}'.format(nick.GetNick(),channel,message.s))
              self.PutIRC('PRIVMSG {0} : (auto-antiping) Please do not just send an empty ping in {1}. Ask the question you have and I will reply ASAP. Thanks.'.format(nick.GetNick(),channel))
              
