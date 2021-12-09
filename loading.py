#! usr/bin/python3
import time
try:
    for i in range(10):
        print("Loading" + "."*i, end="\r")
        time.sleep(.5)
        #how to make this start over again?
except:
    KeyboardInterrupt
    print("\nExiting")