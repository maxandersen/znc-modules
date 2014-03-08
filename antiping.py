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

    def isAntiPing(self, message):
        raw = message.s
        # remove current nick to handle messages that mention me directly
        raw = raw.replace(self.GetNetwork().GetCurNick(),'')
        # remove common 'noop' characters
        raw = raw.replace(':','')
        raw = raw.replace('?','')
        raw = raw.replace('!','')
        raw = raw.replace(' ','')

        if self.directantiping.match(raw):
           return True
        else:
           return False

    def process(self, nick, channel, message):
        if self.isAntiPing(message):
           if channel is None:
              self.PutModule('Antiping from {0}: "{1}"'.format(nick.GetNick(),message.s))
              self.PutIRC('PRIVMSG {0} : (auto-antiping) Please do not just send an empty ping to me. Ask the question you have and I will reply ASAP. Thanks.'.format(nick.GetNick())) 
           else:       
              self.PutModule('Antiping from {0} in {1}: {2}'.format(nick.GetNick(),channel,message.s))
              self.PutIRC('PRIVMSG {0} : (auto-antiping) Please do not just send an empty ping in {1}. Ask the question you have and I will reply ASAP. Thanks.'.format(nick.GetNick(),channel)) 
              
