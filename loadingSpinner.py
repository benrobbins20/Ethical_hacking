import itertools, sys, time
from itertools import cycle
import threading
class fc:
    pv = '\033[38;5;206;48;5;57m'
    end = '\033[0m'
def spinner(run):
    spinnerChars = ['-', '/', '|', '\\']
    if run == 1: # pass int 1 to turn on spinner 
        for char in cycle(spinnerChars):
            print(f'{fc.pv}{char}{fc.end}',end='\r')
            time.sleep(.2)
    elif run == 0: #pass int 0 to turn off spinner
        sys.exit()

