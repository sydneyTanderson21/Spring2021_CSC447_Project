#Import the required libraries :
from tkinter import *
import random
import tkinter

root = Tk()
root.configure(bg="#000000")
root.geometry('+0+0')
root.iconbitmap("Game.ico")
root.title("Rock-Paper-Scissor")
root.resizable(width=False,height=False)

#Hand images :
rockHandPhoto = PhotoImage(file="Rock_1.png")
paperHandPhoto = PhotoImage(file="Paper_1.png")
scissorHandPhoto = PhotoImage(file="Scissor_1.png")


#Decision image :
decisionPhoto = PhotoImage(file="Decision_Final.png")

#Result images :
winPhoto = PhotoImage(file="G_WIN.png")
losePhoto = PhotoImage(file="G_LOST.png")
tiePhoto = PhotoImage(file="G_DRAW.png")



#Initialize the button variables :
rockHandButton = " "
paperHandButton = " "
scissorHandButton = " "
computerName = " "
playerName = " "

imagesDict = {"Rock": rockHandPhoto, "Paper": paperHandPhoto, "Scissor": scissorHandPhoto,
"RockRock": tiePhoto,
"RockPaper": losePhoto,
"RockScissor": winPhoto,
"PaperRock": winPhoto,
"PaperPaper": tiePhoto,
"PaperScissor": losePhoto,
"ScissorRock": losePhoto,
"ScissorPaper": winPhoto,
"ScissorScissor": tiePhoto}

#Create the result button :
resultButton = Label(root,image=decisionPhoto) #SYDNEY... Change size?

#Set the variable to True
click = True
computerText = tkinter.StringVar()
playerText = tkinter.StringVar()

computerText.set("")
playerText.set("Choose: ")

def play():
    global rockHandButton,paperHandButton,scissorHandButton, playerName, computerName
    
    #Set images and commands for buttons :
    rockHandButton = Button(root,image = rockHandPhoto, command=lambda:youPick("Rock"))
    paperHandButton = Button(root,image = paperHandPhoto, command=lambda:youPick("Paper"))
    scissorHandButton = Button(root,image = scissorHandPhoto, command=lambda:youPick("Scissor"))
    
    playerName = Label(root, textvariable=playerText , font = "Helvetica 12", bg="#000000", fg="#FFFFFF")
    playerName.grid(row=0, column=0)

    computerName = Label(root, textvariable=computerText, font = "Helvetica 12", bg="#000000", fg="#FFFFFF")
    computerName.grid(row=0, column=1)
    #Place the buttons on window :
    rockHandButton.grid(row=1,column=0)
    paperHandButton.grid(row=1,column=1)
    scissorHandButton.grid(row=1,column=2)

    #Add space :
    root.grid_rowconfigure(2, minsize=50) #Sydney... change size? 

    #Place result button on window :
    resultButton.grid(row=3,column=0,columnspan=5) #Sydney.. chnge size?
    

    # labelName.place(relheight = 0.2,
    #                          relx = 0.1, 
    #                          rely = 0.2)


def computerPick():
    choice = random.choice(["Rock","Paper","Scissor"])
    return choice

def handleCompPick(playerPick, compPick):
        paperHandButton.configure(image=imagesDict[compPick])
        resultButton.configure(image=imagesDict[playerPick+compPick])
        scissorHandButton.grid_forget()

def youPick(yourChoice):
    global click

    compPick = computerPick()
    playerText.set("Player Choice:")
    computerText.set("Computer Choice:")

    if click==True:

        if yourChoice == "Rock":

            rockHandButton.configure(image=imagesDict[yourChoice])
            handleCompPick(yourChoice, compPick)
            click = False

        elif yourChoice == "Paper":
            rockHandButton.configure(image=imagesDict[yourChoice])
            handleCompPick(yourChoice, compPick)
            click = False

        elif yourChoice=="Scissor":
            rockHandButton.configure(image=imagesDict[yourChoice])
            handleCompPick(yourChoice, compPick)
            click = False

    else:
        #To reset the game :
        if yourChoice=="Rock" or yourChoice=="Paper" or yourChoice=="Scissor":
            rockHandButton.configure(image=rockHandPhoto)
            paperHandButton.configure(image=paperHandPhoto)
            scissorHandButton.configure(image=scissorHandPhoto)
            resultButton.configure(image=decisionPhoto)

            #Get back the deleted buttons :
            scissorHandButton.grid(row=1,column=2)

            #Set click = True :
            click=True


#Calling the play function :
play()

#Enter the main loop :
root.mainloop()