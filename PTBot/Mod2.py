from telegram import Update
from telegram.ext import MessageHandler, filters, ApplicationBuilder, ContextTypes

#Reads any messages in an update
async def ReadAllMsgs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update._effective_message.text
    print(message)


#Grabs a file from any update
async def GrabFile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    #Assign the file to a new variable, await an update from any effective message
    incom_file = await update.effective_message.effective_attachment.get_file()
    await incom_file.download_to_drive('recieved_file')
    print("File recieved!") 

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