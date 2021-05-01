from socket import *
import threading
from tkinter import *
import tkinter
from tkinter.constants import LEFT, TOP, BOTTOM, BOTH,RIGHT, X, Y
from time import sleep
import sys
import random

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

images5 = ["./images/1.gif", "./images/2.gif", "./images/3.gif", "./images/4.gif", "./images/5.gif", "./images/6.gif"]
images6 = list(images5)
images6.append("./images/7.gif")
images7= list(images6)
images7.append("./images/8.gif")
images8= list(images7)
images8.append("./images/9.gif")
images9= list(images7)
images9.append("./images/10.gif")
images10= list(images7)
images10.append("./images/11.gif")

#Hand images :
rockHandPhoto = "./images/Rock_1.gif"
paperHandPhoto = "./images/Paper_1.gif"
scissorHandPhoto = "./images/Scissor_1.gif"


#Decision image :
decisionPhoto = "./images/Decision_Final.gif"

#Result images :
winPhoto = "./images/G_WIN.gif"
losePhoto = "./images/G_LOST.gif"
tiePhoto = "./images/G_DRAW.gif"

rockHandButton = " "
paperHandButton = " "
scissorHandButton = " "
computerName = " "
playerName = " "
click = True

class TCPGUI:
    def __init__(self):
        # HANGMAN window which is currently hidden
        self.client_close = False
        self.initial = True
        self.played = False
        self.Window = Tk()
        self.Window.withdraw()

        # login window
        self.login = Toplevel()
        # self.root = Toplevel()

        #rockpaperscissor
        self.gameWon = 0  #default is false
        # self.rockHandButton = " "
        # self.paperHandButton = " "
        # self.scissorHandButton = " "
        # self.computerName = " "
        # self.playerName = " "

        # set the title
        self.login.title("LOGIN")
        self.login.resizable(width = False, 
                             height = False)
        self.login.configure(width = 400,
                             height = 300)
        self.inputName = StringVar()
        self.inputName.trace('w', self.limitLength) 

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
                             font = "Helvetica 14", textvariable=self.inputName)

        self.entryName.place(relwidth = 0.4, 
                             relheight = 0.12,
                             relx = 0.35,
                             rely = 0.23)

        # set the focus of the curser
        self.entryName.focus()

        self.go = Button(self.login,
                         text = "Start", 
                         font = "Helvetica 14 bold", 
                         command = lambda: self.goAhead(self.entryName.get()))

        self.go.place(relx = 0.4,
                      rely = 0.55)

        self.inputValue = StringVar()
        self.serverText = StringVar()
        self.serverguessed = StringVar()
        self.displaySentence = StringVar()
        self.count = StringVar()
        self.inputValue.trace('w', self.limitLetter)
        self.computerText = StringVar()
        self.playerText = StringVar()
        #________________________________________
        self.Window.mainloop()

    def goAhead(self, name):
        self.login.destroy()
        self.layout(name)
        # the thread to receive messages
        rcv = threading.Thread(target=self.receive)
        rcv.start()

    def limitLetter(self, *args):
        value = self.inputValue.get()
        if len(value) > 1: self.inputValue.set(value[:1])

    def limitLength(self, *args):
        value = self.inputName.get()
        if len(value) > 15: self.inputName.set(value[:15])

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

        self.img = PhotoImage(file="./images/gallows.gif") 
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

        self.guessedLetters = Label(self.Window,
                        width = 5,
                        height = 3,
                        bg = "#000000",
                        fg = "#EAECEE",
                        font = "Helvetica 12",
                        padx = 5,
                        pady = 5, textvariable=self.serverguessed, anchor="nw", justify=LEFT, wraplength=180)

        self.guessedLetters.place(relheight = 0.20,
                        relwidth = 0.40,
                        rely = 0.25, relx = 0.55)

        self.rockPS = Button(self.Window,
                         text = "Wanna play a game?", 
                         font = "Helvetica 10 bold",
                         command = lambda: self.rockpaperscissor())

        self.rockPS.place(relx = 0.55,
                      rely = 0.55)
        self.rockPS.configure(state='disabled')
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

        self.display.place(relheight = 0.09,
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
        #________________________________________________________
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
            sleep(2.5)
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
        self.rockPS.configure(state='disabled')

    def enableBTNs(self):
        self.entryMsg.configure(state='normal')
        self.guessPhrase.configure(state='normal')
        self.phraseBTN.configure(state='normal')
        self.buttonMsg.configure(state='normal')

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

        if(int(self.numCount) <= 5 and self.played == False):
             self.rockPS.configure(state='normal')
             self.played = True

        self.count.set("Guesses Left: " + num)
        self.numCount = num

    def rockpaperscissor(self):
        self.root = tkinter.Toplevel(self.Window)
        self.root.configure(bg="#000000")
        self.root.geometry('+0+0')
        # self.root.iconbitmap("Game.ico")
        self.root.title("Rock-Paper-Scissor")
        self.root.resizable(width=False,height=False)
        self.disableBTNs()

        self.rpsImagesDict = {"Rock": PhotoImage(file=rockHandPhoto), "Paper": PhotoImage(file=paperHandPhoto), "Scissor": PhotoImage(file=scissorHandPhoto),
        "RockRock": [PhotoImage(file=tiePhoto), "again"],
        "RockPaper": [PhotoImage(file=losePhoto), "lose"],
        "RockScissor": [PhotoImage(file=winPhoto), "win"],
        "PaperRock": [PhotoImage(file=winPhoto), "win"],
        "PaperPaper": [PhotoImage(file=tiePhoto), "again"],
        "PaperScissor": [PhotoImage(file=losePhoto), "lose"],
        "ScissorRock": [PhotoImage(file=losePhoto), "lose"],
        "ScissorPaper": [PhotoImage(file=winPhoto), "win"],
        "ScissorScissor": [PhotoImage(file=tiePhoto), "again"]}

        self.decision = PhotoImage(file=decisionPhoto)
        self.resultButton = Label(self.root,image=self.decision)

        # self.resultButton.configure
        self.click = True
        self.computerText.set("")
        self.playerText.set("Choose: ")

        global rockHandButton,paperHandButton,scissorHandButton, playerName, computerName

        #Set images and commands for buttons :
        rockHandButton = Button(self.root,image = self.rpsImagesDict["Rock"], command=lambda:self.youPick("Rock"))
        paperHandButton = Button(self.root,image = self.rpsImagesDict["Paper"], command=lambda:self.youPick("Paper"))
        scissorHandButton = Button(self.root,image = self.rpsImagesDict["Scissor"], command=lambda:self.youPick("Scissor"))

        playerName = Label(self.root, textvariable=self.playerText , font = "Helvetica 12", bg="#000000", fg="#FFFFFF")
        playerName.grid(row=0, column=0)

        computerName = Label(self.root, textvariable=self.computerText, font = "Helvetica 12", bg="#000000", fg="#FFFFFF")
        computerName.grid(row=0, column=1)
        #Place the buttons on window :
        rockHandButton.grid(row=1,column=0)
        paperHandButton.grid(row=1,column=1)
        scissorHandButton.grid(row=1,column=2)

        #Add space :
        self.root.grid_rowconfigure(2, minsize=50)

        #Place result button on window :
        self.resultButton.grid(row=3,column=0,columnspan=5) 
        self.draw = Button(self.root,
                         text = "Play Again", state="disabled",
                         font = "Helvetica 13 bold", command = lambda: self.resetGame())

        self.draw.place(relx = 0.55,
                      rely = 0.48)

        self.winLose = Button(self.root,
                         text = "Move On", state="disabled",
                         font = "Helvetica 13 bold", command = lambda: self.winlostGame())

        self.winLose.place(relx = 0.20,
                    rely = 0.48)


    def computerPick(self):
        choice = random.choice(["Rock","Paper","Scissor"])
        return choice

    def handleCompPick(self, playerPick, compPick):
            paperHandButton.configure(image=self.rpsImagesDict[compPick])
            self.gameWon = self.rpsImagesDict[playerPick+compPick][1]
            self.resultButton.configure(image=self.rpsImagesDict[playerPick+compPick][0])
            scissorHandButton.grid_forget()

    def youPick(self, yourChoice):
        global click

        compPick = self.computerPick()
        self.playerText.set("Player Choice:")
        self.computerText.set("Computer Choice:")

        if click==True:

            if yourChoice == "Rock":
                rockHandButton.configure(image=self.rpsImagesDict[yourChoice])
                self.handleCompPick(yourChoice, compPick)
                click=False

            elif yourChoice == "Paper":
                rockHandButton.configure(image=self.rpsImagesDict[yourChoice])
                self.handleCompPick(yourChoice, compPick)
                click=False

            elif yourChoice=="Scissor":
                rockHandButton.configure(image=self.rpsImagesDict[yourChoice])
                self.handleCompPick(yourChoice, compPick)
                click=False

        if(self.gameWon == "again"):
            self.draw.configure(state='normal')
            click=True

        elif(self.gameWon == "win" or self.gameWon == "lose"):
            self.winLose.configure(state='normal')

    def resetGame(self):
        rockHandButton.configure(image=self.rpsImagesDict["Rock"])
        paperHandButton.configure(image=self.rpsImagesDict["Paper"])
        scissorHandButton.configure(image=self.rpsImagesDict["Scissor"])
        self.resultButton.configure(image=self.decision)

        #Get back the deleted buttons :
        scissorHandButton.grid(row=1,column=2)
        self.draw.configure(state='disabled')
        self.computerText.set("")

    def winlostGame(self):
        self.enableBTNs()
        self.sendButton(self.gameWon)
        self.root.destroy()


g = TCPGUI()


