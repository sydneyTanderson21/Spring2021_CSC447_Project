from socket import *
import random
import threading
import sys
from time import *
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP
from base64 import b64decode, b64encode

udpPorts = []   # for list of UDP ports, in order to prevent collision

FORMAT = "utf-8"
PORT = 5000
SERVER = "localhost"
ADDRESS = (SERVER, PORT)
stop_server = False

# Lists that will contains
# all the clients connected to 
# the server and their names.
clients, names = [], []

fullword = False

print('Creating TCP socket')
s = socket(AF_INET, SOCK_STREAM)
s.bind(ADDRESS)

def new_client(c, addr, command, full):
    # inst = "This is hangman You will guess one letter at a time. If the letter is in the hidden word the '-' will be\n" \
    #        "replaced by the correct letter Guessing multiple letters at a time will be considered as guessing the entire\n" \
    #        "word (which will result in either a win or loss automatically - win if correct, loss if incorrect).You win\n" \
    #        "if you either guess all of the correct letters or guess the word correctly. You lose if you run out of\n" \
    #        "attempts. Attempts will be decremented in the case of an incorrect or repeated letter guess.\n" \
    #        "Enter 'Start' or 'Exit' when you're asked 'Are you Ready?' " \
    #        "In the game you must enter 'guess <char>' to guess or 'end' to end the game\n"

    inst = "This is hangman You will guess one letter at a time. if you either guess all of the correct letters or guess the word correctly."
    guessedLetters = set()
    words = []
    display = []
    count = 4
    # reads from the file, decrypts and makes a list of words
    for line in decryptData(open("encryptedWords.txt", "r").read()).splitlines():
        line = line.strip()
        words.append(line)

    random.shuffle(words)                                       # shuffle the list and take the first

    if command == '-r':
        word = list(words[0])

    #print('Hidden word: ', word) #make it a list

    for i in range(len(word)):
        display.append('_')

    display = list(display)
    #print('The game is on,guess')
    # print(str(display) + str((len(word)+1) - count))
    c.send((str(display)).encode(FORMAT))           # 3 send display
    c.send((str((len(word)+1) - count)).encode(FORMAT))   # sendcount

    while True:

        char = c.recv(1024).decode(FORMAT)                                          # char is either a letter or a word or the full phrase

        while True and count < len(word)+1 and char and char != "": #logic makes sense, count = # of guesses
            #print("Received: " + char)
            char = char.lower()
            count += 1 #guesses increase
            if char == 'exit':
                c.send(("GOODBYE!").encode(FORMAT))
                break
            elif len(char) > 1:   # it means you are trying to guess the entire word
                if fun(word, char):
                    c.send(str((len(word)+1) - count).encode(FORMAT))
                    c.send(("You got it!!! Bulls eye! The word was " + str(char)).encode(FORMAT))
                    full = True
                    break
                else:
                    c.send(str((len(word)+1) - count).encode(FORMAT))
                    c.send(("You LOST! Better Luck Next Time!").encode(FORMAT))
                    break
            elif len(char) == 1: #guessed a letter
                display = list(display)
                guessedLetters.add(char)
                for i in range(len(word)):
                    if word[i] == char:
                        display[i] = char
                if char in word:
                    count -= 1
                    #print("CHAR IN WORD")
                if display == word:
                    c.send(str((len(word)+1) - count).encode(FORMAT))
                    c.send(("You got it!!! Bulls eye!" + str(display)).encode(FORMAT))
                    break
                else:
                    # c.send(str((len(word)+1) - count).encode(FORMAT))    # 5 send count
                    #print('Sending display ', display)
                    c.send((str(display) + str((len(word)+1) - count)).encode(FORMAT))                 # 6 send the word
                #guessedLetters = list(guessedLetters)
                c.send(("Guessed: " + str(guessedLetters)).encode(FORMAT))

            char= c.recv(1024).decode(FORMAT)                                         # 7 Receive char again

        if(char == "exit"):
            c.send("CLOSE".encode(FORMAT))              # 10 send end message
            break
        elif display != word and count >= len(word)+1 and full == False:
            #c.send(str((len(word)+1) - count).encode(FORMAT))
            c.send(("You LOST! Better Luck Next Time!").encode(FORMAT))
            c.send("CLOSE".encode(FORMAT))
            # sleep(3)
            break
    c.close()
    stop_server = True


def Server(command):

    print('TCP is on ' + SERVER)

    s.listen()

    while True:

        con, addr = s.accept()

        con.send("NAME".encode(FORMAT))

        name = con.recv(1024).decode(FORMAT)
        names.append(name)
        clients.append(con)


        r = "Hello, " + name
        con.send(r.encode(FORMAT))                     # accept
        #print("Huston, we have a connection" + str(addr))               # print the address we're connecting to
        thread = threading.Thread(target=new_client, args=(con, addr, command, fullword))
        thread.start()     # start a new thread
        if stop_server:
            sys.exit(0)

    #con.close()                                                           # Close the TCP connection


def fun(word, string):              # first is the current word we are guessing, second is received guess string
    string = list(string)           # this function checks if a user makes a whole word guess
    for i in range(len(word)):
        if word[i] != string[i]:
            return False
    return True

def decryptData(data):
    private_key = RSA.import_key(open("private_key.pem").read())
    rsa_private = PKCS1_OAEP.new(private_key)
    text = b64decode(data)
    return rsa_private.decrypt(text).decode()


Server("-r")
