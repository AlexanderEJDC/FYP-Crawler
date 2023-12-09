#Master Control File 

#Setup relevant imports from other API interfaces that will be required. 
from telegram import Update
from telegram.ext import MessageHandler, filters, ApplicationBuilder, ContextTypes

import asyncio
import os 

#Import the two other API interfaces
from PTBot import Mod2
#from VTBot import whoops

#Main function
async def main():
    #Setup the bot, supply it with the desired token
    PTBot = await Mod2.BotSetup('6460026166:AAFf7Wv93Cpa9YUFtsZ0E-AJfmFgKGDx_1s')
    PTBot
    


#Execute main
if __name__ == "__main__":
    asyncio.run(main())