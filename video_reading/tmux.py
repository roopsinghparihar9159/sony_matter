import time
import sys
import os
import subprocess

class Tmux(object):

    WAIT_SECS = 5

    def __init__(self, session_name, param):
        self.name = session_name
#       os.system('tmux new -s %s &' % session_name)
        # subprocess.Popen(['C:\\cygwin64\\Cygwin', '-c', 'tmux new -s %s' % session_name], shell=True)
        subprocess.Popen(['C:\\cygwin64\\Cygwin','tmux', 'new', '-d', '-s', session_name],shell=True)
#       subprocess.check_call('tmux new -s %s' % session_name, shell=True, close_fds=True)
# ======NOT return here, unless exit from tmux==========

    def execute(self, cmd, wait_secs=WAIT_SECS):
        time.sleep(wait_secs)
        subprocess('tmux send-keys -t %s ls Enter' % self.name)

    # def horizontal_split(self):
    #     time.sleep(1)
    #     subprocess('tmux split-window -v -t %s' % self.name)


if __name__ == '__main__':
    print('tmux test............')
    tmux = Tmux("tmux-test", 999)
    tmux.horizontal_split()
    tmux.execute('ls')


# from subprocess import Popen, CREATE_NEW_CONSOLE

# Popen('cmd', creationflags=CREATE_NEW_CONSOLE)

# input('Enter to exit from Python script...')


