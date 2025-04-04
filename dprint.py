from config import config
from g_share import g_share
g_share.debug= config.debug

def dprint(*msg):
    if g_share.debug:
        print(*msg)


if __name__=='__main__':
    g_share.debug = True
    abc=122
    dprint('hello1', abc)
    g_share.debug =False
    dprint('hello2')
