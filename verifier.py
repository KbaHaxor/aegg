import commands
import logging
from pwn import *

l = logging.getLogger("aegg.verifier")


class Verifier(object):
    CMDS = ['uname -a', 'id', 'whoami']

    def __init__(self, binary):
        self.binary = binary
        self.delay = 0.5

    def _verify(self, payload, cmd):
        l.info('Verifying by cmd: %s ...' % cmd)
        s = process(self.binary)

        s.sendline(payload)
        s.recvrepeat(self.delay)
        s.sendline(cmd)
        recv = s.recvrepeat(self.delay)
        s.close()

        uname = commands.getoutput(cmd)
        if uname in recv:
            l.info('... succeeded!')
            return True
        l.info('... failed!')
        return False

    def verify(self, payload):
        for cmd in Verifier.CMDS:
            try:
                if self._verify(payload, cmd):
                    return True
            except Exception, e:
                l.warning('Pwnlib Error: %s %s' % (Exception, e))
        return False
