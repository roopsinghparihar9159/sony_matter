import sys
import os
import shlex
import pprint
from subprocess import *


def cmd(inp):
    """ Run a shell command
    inp -- (string) command to run including all arguments
    returns list((string) command output,(int) return code)
    """
    command = shlex.split(inp)
    com = Popen(command, shell=False, stdout=PIPE, stderr=PIPE)
    out = ''.join(com.communicate()).strip()
    return out, com.returncode


def tmuxSessions(kill = False):

    tm = cmd('tmux ls');

    sess = [];

    sess.append("Create New Session");

    s = tm[0].split("\n")

    if len(s)==0:
        return createNewSession()

    for i, v in enumerate(s):
        index = i+1
        sess.append(v)

    for i, v in enumerate(sess):
        if kill and i==0:
            continue;
        out = "{0}) {1}".format(i,v)
        print(out)

    ask = "Select a Session #: \n"

    if kill:
        ask = "Select a Session # To Kill: \n"

    inp = input(ask);

    return inp,sess;



def restoreSession(sess):

    s = sess.split(":")

    command = "tmux attach -t '{0}'".format(s[0])

    cmd(command)

    exit(0)



def createNewSession():
    # ask user for new session name
    name = input("Name you new session: \n")

    command = "tmux new-session -s '{0}'".format(name)

    res = cmd(command)

    exit(0)


def killSession(sess):

    s = sess.split(":")

    command = "tmux kill-session -t '{0}'".format(s[0]);

    res = cmd(command);

    exit(0);


def askCreate():

    inp = tmuxSessions();

    while inp[0].isdigit() == False or int(inp[0])<0 or int(inp[0])>(len(inp[1])-1):
        inp = tmuxSessions()

    index = int(inp[0]);

    if index ==0:
        return createNewSession()
   # session = inp[1][int(inp[0])]

    return restoreSession(inp[1][index])



def askKill():

    inp = tmuxSessions(True);

    while inp[0].isdigit() == False or int(inp[0])<=0 or int(inp[0])>len(inp[1]):
        inp = tmuxSession(True);

    sess = inp[1][int(inp[0])]

    killSession(sess);

    exit(0);

print('###########################')
print('## TMUX SESSIONS ##########')
print('###########################')


try:
    if len(sys.argv)>1 and sys.argv[1] == '-k':
        askKill()
    else: 
        askCreate()
except KeyboardInterrupt:
    print("\n Canceled......")
    exit(0)
except NameError:
    print("Exiting....")
    exit(0);