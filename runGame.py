from time import sleep
import sys
from subprocess import call
import threading

from subprocess import call
def thread_second():
    call([sys.executable, "ServerTCPONLY.py"])

processThread = threading.Thread(target=thread_second)  # <- note extra ','
processThread.start()

sleep(3)

c = call([sys.executable, 'ClientTCPONLY.py'])
                                    # stdout=PIPE,
                                    # stderr=STDOUT