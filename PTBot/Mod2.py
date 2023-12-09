from telegram import Update
from telegram.ext import MessageHandler, filters, ApplicationBuilder, ContextTypes

import os

mainDirectory = "/home/alexander/FYP-Crawler GitRepo/FYP-Crawler/"

def checkIfExistent(titleOfRoom):
    if os.path.exists(mainDirectory+titleOfRoom):
        return True
    else:
        return False
    
def mkdir(titleOfRoom):
    os.mkdir(mainDirectory+titleOfRoom)
    open(mainDirectory+titleOfRoom+".txt", "x")
    newDir = mainDirectory+titleOfRoom+"/"+titleOfRoom+".txt"
    print(newDir)
    return newDir

def appendToFile(dir,message):
    file = open(dir,"a")
    file.write(message+"\n")
    file.close()

#Reads any messages in an update
async def ReadAllMsgs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update._effective_message.text
    roomTitle = update.effective_chat.title

    if checkIfExistent(roomTitle) == False:
        newDir = mkdir(roomTitle)
        appendToFile(newDir, message)
    elif checkIfExistent(roomTitle) == True:
        appendToFile(mainDirectory+roomTitle+"/"+roomTitle+".txt", message)

    else:
        print("Shits fucked!")
        print(message)
        print(roomTitle)

#Grabs a file from any update
async def GrabFile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #Assign the file to a new variable, await an update from any effective message
    incom_file = await update.effective_message.effective_attachment.get_file()
    await incom_file.download_to_drive('recieved_file')
    print("File recieved!") 

async def ExportHistory():
    print("History Exported!")

#Supply with token in main, build bot
async def BotSetup(API_TOKEN):
    PTBot = ApplicationBuilder().token(
        API_TOKEN
    ).build()

    file_handler = MessageHandler(filters.ATTACHMENT & (~filters.COMMAND), GrabFile)
    channel_handler = MessageHandler(filters.ALL & (~filters.COMMAND), ReadAllMsgs)

    PTBot.add_handler(file_handler)
    PTBot.add_handler(channel_handler)
    #return the built bot with handlers attached
    return PTBot

#Boilerplate to stop script running when imported
if __name__ == '__main__':
    #Application builder. On its own, doesn't do anything.
    application = ApplicationBuilder().token(
       '6460026166:AAFf7Wv93Cpa9YUFtsZ0E-AJfmFgKGDx_1s').build()
    
    #Command handles!
    file_handler = MessageHandler(filters.ATTACHMENT & (~filters.COMMAND), GrabFile)
    channel_handler = MessageHandler(filters.ALL & (~filters.COMMAND), ReadAllMsgs)

    application.add_handler(file_handler)
    application.add_handler(channel_handler)

    application.run_polling()  #Run until Cntrl-C! 