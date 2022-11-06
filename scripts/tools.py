'''
Kyle Tennison
November 4, 2022

Misc tools for Math Modeling challenge
'''


from constants import *
from datetime import datetime
from subprocess import Popen
import os

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def setup() -> None:
    '''
    Miscellaneous setup for program. Expected to run at start of program.
    Pre: 
        None
    Pose:
        Changes os environment path
    '''
    # Change directory to current file
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    # Purge log & output folder
    resetLog()
    purgeFolder(dname)

def bold(text:str) -> str:
    ''' Returns text with bold encoding.'''
    return bcolors.BOLD + text + bcolors.ENDC

def red(text:str) -> str:
    '''Returns text with red encoding.'''
    return bcolors.FAIL + text + bcolors.ENDC

def green(text:str) -> str:
    ''' Returns text with green encoding'''
    return bcolors.OKGREEN + text + bcolors.ENDC

def warn(text:str) -> str:
    '''Returns text with yellow encoding'''
    return bcolors.WARNING + text + bcolors.ENDC

def resetLog() -> None:
    ''' Purge LOGFILE to make room for new program'''
    with open(LOGFILE, 'w') as f: 
        f.write('')

def purgeFolder(cwd: str) -> None: 
    ''' Purge WRITEDIR files for the updated ones'''

    # Delete directory
    path = f"{cwd}/{WRITEDIR}/"
    Popen(["rm", "-r", path])

    # Make new directory
    Popen(["mkdir", "-p", path])


def log(text:str, end:str='\n', hasHeader:bool=True) -> None:
    '''
    Log a message to the console. Saves output in LOGFILE
    Pre:
      text (str)        - Text to print to the console
      end (str)         - Ending character for line (default = \n)
      hasHeader (bool)  - Show timestamp in print?
    Post:
      Prints to console.
      Modifies LOGFILE
      No return
    '''

    # Get rid of color headers from string
    for color in [i for i in bcolors.__dict__.values() if isinstance(i, str)]:
        if color in text:
            text = text.replace(color, '')

    # Log text
    if hasHeader: print(datetime.now(), end=' ')
    print(text, end=end, flush=True)
    with open(LOGFILE, 'a') as f:
        f.write(f"\n{datetime.now()} > {text}")

    