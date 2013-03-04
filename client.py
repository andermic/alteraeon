#! /usr/bin/python

import cmd
import multiprocessing
import signal
import socket


def kill_connection():
    print 'Terminating connection'
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()
    print 'Connection terminated'
    exit(0)

def sigintHandler(signum, frame):
    print 'Got a SIGINT'
    kill_connection()

def receiver(sock, agent):
    while True:
        try:
            msg = sock.recv(10000)
        except:
            exit(0)
        agent.act(msg) 
        print msg.replace('\xff\xf9','')


class Agent:
    is_running = False
    state = None

    def control(s, msg):
        if msg == ' run':
            print 'Running agent'
            s.is_running = True
        if msg == ' stop':
            print 'Stopping agent'
            s.is_running = False

    def act(s, msg):
        pass


class UserPrompt(cmd.Cmd):
    prompt = ''

    def do_agent(s, line):
        agent.control(line)

    def do_help(s, line):
        s.default('help ' + line)

    def do_quit(s, line):
        sock.send('quit\n')
        kill_connection()

    def emptyline(s):
        sock.send('\n')

    def default(s, line):
        sock.send(line + '\n')


if __name__ == '__main__':
    signal.signal(signal.SIGINT, sigintHandler)
    
    sock = socket.socket()
    sock.connect(('alteraeon.com', 3000))
    agent = Agent()
    user_prompt = UserPrompt()
    
    p = multiprocessing.Process(target=receiver, args=(sock, agent))
    p.start()

    user_prompt.cmdloop()
