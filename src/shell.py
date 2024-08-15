#!/usr/bin/env python3

from sys import argv
import subprocess
import os
from time import time
import threading
from concurrent.futures import ThreadPoolExecutor
from local_builtins import *
from local_utils import *
from local_network import *

print_local = False

class threadObject(threading.Thread):

    def __init__(self, arguments):
        threading.Thread.__init__(self)
        self.id = os.getpid()
        self.arguments = arguments
        self.data = ""

    def run(self, *args):
        self.data = callback(self.arguments)



class fshell(object): 

    def __init__(self):

        self.filedescriptors = list()
        self.builtins = {}
        self.clients = list()
        self.executor = ThreadPoolExecutor()
    
    def __exit__(self):
        pass


def callback(*args):
    print("Thread at: ", threading.get_ident())
    data = subprocess.run(args[0], shell=True, capture_output = True).stdout.decode("utf-8")
    return data

"""
Handle external command
"""
def handle_external(**kwargs):
    arguments = kwargs["arguments"]
    data = ""
    try:
        t = threadObject(arguments)
        t.start()
        t.join()
        data = t.data
    except Exception as e:
        return ""
    return data

"""
Handle internal command
"""
def handle_internal(**kwargs):

    shell = kwargs["shell"]
    cmd = kwargs["command"]
    arguments = kwargs["arguments"]
    data = shell.builtins[cmd](shell, arguments)
    return data

"""
Lookup command
"""
def lookupcmd(**kwargs):

    if kwargs["command"] not in kwargs["shell"].builtins.keys():
        return False
    else:
        return True

"""
Handler
"""
def command_handler(**kwargs):
    shell = kwargs["shell"]
    arguments = kwargs["arguments"]
    command = arguments[0]
    data = ""
    if lookupcmd(shell=shell, command=command) is False:
        data = handle_external(shell=shell, command=command, arguments=arguments)
    else:
        data = handle_internal(shell=shell, command=command, arguments=arguments)

    if print_local is True:
        print(data)
        
    return data

"""
Insert commands
"""
def insert_builtins(**kwargs):

    shell = kwargs["shell"]
    if isinstance(shell, fshell) is False:
        return False

    shell.builtins["help"] = helpfunction
    shell.builtins["greet"] = greet
    shell.builtins["exit"] = goodbye

    return True

"""
Input loop
"""
def inputloop(**kwargs):
    shell = kwargs["shell"]
    while True:
        data = get_input()
        if(len(data) == 0):
            continue
        command_handler(shell=shell, arguments=splitdata(data))

"""
Main
"""
def main(args):
    global print_local
    print("Main thread at: ", threading.get_ident())
    shell = fshell()
    insert_builtins(shell=shell, arguments=args[0])
    create_server(shell=shell, ip="127.0.0.1", port=5555)

    """
    if len(args) == 1:
        print_local = True
        inputloop(shell=shell)
    elif len(args) == 3 and args[1] == "listen":
        print("Starting server!")
        create_server(shell=shell, ip="127.0.0.1", port=5555)
    """
    
if __name__ == "__main__":
    main(argv)

