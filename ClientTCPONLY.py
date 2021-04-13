from socket import *
import random
import threading
from tkinter import *
from tkinter.constants import LEFT, TOP, BOTTOM, BOTH,RIGHT, X, Y
import tkinter.messagebox
from tkinter import font
from PIL import ImageTk,Image
from time import sleep
import sys



FORMAT = "utf-8"
PORT = 5000
SERVER = "localhost"
ADDRESS= (SERVER, PORT) #localhost or 127.0.0.1 and 5000

print('Creating TCP for client')
s = socket(AF_INET, SOCK_STREAM)
#name = input("Enter your name:")
#s.settimeout()
try:
    s.connect(ADDRESS)
except error:
    print("Caught exception error, cannot connect")

images5 = ["1.gif", "2.gif", "3.gif", "4.gif", "5.gif", "6.gif"]
images6 = list(images5)
images6.append("7.gif")
images7= list(images6)
images7.append("8.gif")
images8= list(images7)
images8.append("9.gif")
images9= list(images7)
images9.append("10.gif")
images10= list(images7)
images10.append("11.gif")

class TCPGUI:
    def __init__(self):
        # HANGMAN window which is currently hidden
        self.client_close = False
        self.initial = True
        self.Window = Tk()
        self.Window.withdraw()

        # login window
        self.login = Toplevel()

        # set the title
        self.login.title("LOGIN")
        self.login.resizable(width = False, 
                             height = False)
        self.login.configure(width = 400,
                             height = 300)

        # Login to continue text
        self.pls = Label(self.login, 
                       text = "Enter name to start",
                       justify = CENTER, 
                       font = "Helvetica 14 bold")

        self.pls.place(relheight = 0.15,
                       relx = 0.2, 
                       rely = 0.05)
#______________________________________________________________________________
        # field for username
        self.labelName = Label(self.login,
                               text = "Name: ",
                               font = "Helvetica 12")

        self.labelName.place(relheight = 0.2,
                             relx = 0.1, 
                             rely = 0.2)

        # create a entry box for 
        # tyoing the message
        self.entryName = Entry(self.login, 
                             font = "Helvetica 14")

        self.entryName.place(relwidth = 0.4, 
                             relheight = 0.12,
                             relx = 0.35,
                             rely = 0.23)

        # set the focus of the curser
        self.entryName.focus()
#__________________________________________________________________________________
        # field for password
        # self.passName = Label(self.login,
        #                     text = "Password: ",
        #                     font = "Helvetica 12")

        # self.passName.place(relheight = 0.2,
        #                     relx = 0.1,
        #                     rely = 0.35)

        # self.entryPass = Entry(self.login,
        #                     font = "Helvetica 14", show="*")

        # self.entryPass.place(relwidth = 0.4,
        #                     relheight = 0.12,
        #                     relx = 0.35,
        #                     rely = 0.4)

        # create a Continue Button 
        # along with action
        self.go = Button(self.login,
                         text = "Start", 
                         font = "Helvetica 14 bold", 
                         command = lambda: self.goAhead(self.entryName.get()))

        self.go.place(relx = 0.4,
                      rely = 0.55)

        #Sydney ADDED_______________________
        self.inputValue = StringVar()
        self.serverText = StringVar()
        self.serverguessed = StringVar()
        self.displaySentence = StringVar()
        self.count = StringVar()
        self.inputValue.trace('w', self.limitLetter) #sydney
        #________________________________________
        self.Window.mainloop()

    def goAhead(self, name):
        self.login.destroy()
        self.layout(name)
        #CODE GOES HERE SYDNEY!!!!!!!!!
        #MAYBE
        # the thread to receive messages
        rcv = threading.Thread(target=self.receive)
        rcv.start()

    def limitLetter(self, *args):
        value = self.inputValue.get()
        if len(value) > 1: self.inputValue.set(value[:1])

    def layout(self,name):
        self.name = name
        self.currentImages = []
        self.count.set("Guesses Left:")
        self.numCount = 0
        self.imagesDict = {"5": images5, "6": images6, "7": images7, "8": images8, "9": images9, "10": images10}
        #self.serverguessed.set("Guessed -> ")
        # to show chat window
        self.Window.deiconify()
        self.Window.title("HANGMAN")
        self.Window.resizable(width = False,
                              height = False)
        self.Window.configure(width = 470,
                              height = 550,
                              bg = "#FFFFFF")

        self.img = PhotoImage(file="gallows.gif") 
        self.panel = Label(self.Window, image=self.img, width = 200, bg = "#FFFFFF",
                             height = 250,)
        self.panel.pack(side="bottom", fill="both", expand="yes")
        self.panel.place( relx=0.05,
                            rely = 0.2)
       # self.Window.create_image(20, 20, anchor=NW, image=self.img) 

        #WHERE SERVER INFO WILL GO
        self.textCons = Label(self.Window,
                             width = 20,
                             height = 2,
                             bg = "#17202A",
                             fg = "#EAECEE",
                             font = "Impact 14",
                             padx = 5,
                             pady = 5, textvariable=self.serverText)

        self.textCons.place(relheight = 0.15,
                            relwidth = 1)

    #SYDNEY________________________________________________
        self.guessedLetters = Label(self.Window,
                        width = 5,
                        height = 3,
                        bg = "#000000",
                        fg = "#EAECEE",
                        font = "Helvetica 12",
                        padx = 5,
                        pady = 5, textvariable=self.serverguessed, anchor="nw", justify=LEFT, wraplength=180)

        self.guessedLetters.place(relheight = 0.20, #SYDNEY,
                        relwidth = 0.40,
                        rely = 0.25, relx = 0.55)

        self.guessCountField = Label(self.Window, height=1, width=2, bg = "#FFFFFF",
                             font = "Helvetica 9", textvariable=self.count)

        self.guessCountField.place(relwidth = 0.2, 
                             relheight = 0.05,
                             relx = 0.65,
                             rely = 0.20)

        self.display = Label(self.Window,
                        width = 20,
                        height = 1,
                        bg = "#000000",
                        fg = "#FFFFFF",
                        font = "Helvetica 14", 
                        padx = 5,
                        pady = 5, textvariable=self.displaySentence)

        self.display.place(relheight = 0.09, #SYDNEY,
                        relwidth = 1,
                        rely = 0.75, relx = 0)
    #___________________________________

        self.labelBottom = Label(self.Window,
                                 bg = "#ABB2B9",
                                 height = 45)

        self.labelBottom.place(relwidth = 1,
                               rely = 0.825)

        self.entryMsg = Entry(self.labelBottom,
                              bg = "#2C3E50",
                              fg = "#EAECEE",
                              font = "Helvetica 20", textvariable=self.inputValue, justify='center')

        # place the given widget
        # into the gui window
        self.entryMsg.place(relwidth = 0.20,
                            relheight = 0.06,
                            rely = 0.008,
                            relx = 0.35)

        self.entryMsg.focus()

        # create a Send Button
        self.buttonMsg = Button(self.labelBottom,
                                text = "Guess Letter",
                                font = "Helvetica 10 bold", 
                                width = 20,
                                bg = "#ABB2B9",
                                command = lambda : self.sendButton(self.entryMsg.get()))

        self.buttonMsg.place(relx = 0.60,
                             rely = 0.008,
                             relheight = 0.06, 
                             relwidth = 0.22)
        #SYDNEY_________________________________________________________
        self.guessPhrase = Entry(self.labelBottom,
                                bg = "#2C3E50",
                                fg = "#EAECEE",
                                font = "Helvetica 13")

        # place the given widget
        # into the gui window
        self.guessPhrase.place(relwidth = 0.74,
                                relheight = 0.06,
                                rely = 0.075,
                                relx = 0.011)

            # create a full guess Button
        self.phraseBTN = Button(self.labelBottom,
                                text = "Guess Phrase",
                                font = "Helvetica 10 bold", 
                                width = 20,
                                bg = "#ABB2B9",
                                command = lambda : self.sendButton(self.guessPhrase.get()))

        self.phraseBTN.place(relx = 0.77,
                                rely = 0.075,
                                relheight = 0.06,
                                relwidth = 0.22)
        #____________________________________________________________________
        self.quit = Button(self.Window,
                                text = "Quit",
                                font = "Helvetica 10 bold", 
                                width = 3,
                                bg = "#FF0000",
                                command = lambda : self.sendButton('exit'))

        self.quit.place( relheight = 0.06,relwidth = 0.15,
                        rely = 0, relx = 0.83)

        self.textCons.config(cursor = "arrow")
        self.guessedLetters.config(cursor="arrow")

    def sendButton(self, msg):
        self.msg=msg
        self.entryMsg.delete(0, END)
        self.sendMessage()
        # snd= threading.Thread(target = self.sendMessage)
        # snd.start()

    def sendMessage(self):
        while True:
            #message = self.msg
            s.send(self.msg.encode(FORMAT))
            break

    def receive(self):
        while True:
            try:
                message = s.recv(1024).decode(FORMAT)

                #print("MESSSAGE: "+ message)
                # if the messages from the server is NAME send the client's name
                if message == 'NAME':
                    s.send(self.name.encode(FORMAT))
                elif message == 'CLOSE':
                    self.quit.configure(state='disabled')
                    s.close()
                    self.client_close = True
                    break
                elif message.isnumeric():
                    self.updateCount(message)
                elif '[' in message:
                    self.messageParse(message)
                elif "{'" in message:
                     self.serverguessed.set(message[9:])
                else:
                    self.serverText.set(message)
                    if 'You got it' in message or 'You LOST' in message:
                        self.disableBTNs()

            except Exception as e:
                print(e)
                #s.close()
                #break
        if self.client_close:
            sleep(3)
            self.Window.destroy()
            sys.exit(0)
    def messageParse(self, message):
        # splite takes an extra paramter to limit the # of splits
        if 'You got it' in message or 'You LOST' in message:
            a = message.split("[",1)
            #print(a)
            #print(a[0])
            self.serverText.set(a[0])
            self.displaySentence.set(a[1][:-1])
            self.disableBTNs()
        else:
            x = message.split("]",1)[1] #get second half of split info
            y = message.split("]",1) #entire array of split objects, only split once cause of param 1
            self.displaySentence.set(y[0][1:])
            #print(x)
            #print(y)
            if x.isnumeric():
                self.updateCount(x)
            elif 'Guessed' in x:
                self.serverguessed.set(x[9:])

    def disableBTNs(self):
        self.entryMsg.configure(state='disabled')
        self.guessPhrase.configure(state='disabled')
        self.phraseBTN.configure(state='disabled')
        self.buttonMsg.configure(state='disabled')

    def updateCount(self, num):
        if self.initial:
            self.count.set("Guesses Left: " + num)
            self.currentImages = list(self.imagesDict[num]) #get correct list of images from dict
            self.numCount = num
            self.initial = False
        elif(self.numCount != num): #which means that you did NOT GUESS it correct
                    getimg = self.currentImages[0]
                    img2 = PhotoImage(file=getimg)
                    self.panel.configure(image=img2)
                    self.panel.image = img2
                    self.currentImages.pop(0)
                    self.serverText.set("Nope, Guess again!")
        else: #guessed correctly
            self.serverText.set("Nice! Keep Guessin'")

        self.count.set("Guesses Left: " + num)
        self.numCount = num

g = TCPGUI()


