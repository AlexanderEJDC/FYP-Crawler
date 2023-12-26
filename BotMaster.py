#Master Control File 
#6460026166:AAFf7Wv93Cpa9YUFtsZ0E-AJfmFgKGDx_1s
#Setup relevant imports from other API interfaces that will be required. 
from telegram import Update
from telegram.ext import MessageHandler, filters, ApplicationBuilder, ContextTypes

import asyncio
import os 

#Import the two other API interfaces
from PTBot import Mod3
#from VTBot import whoops

API_TOKEN = "6460026166:AAFf7Wv93Cpa9YUFtsZ0E-AJfmFgKGDx_1s"


"""
#Execute main
if __name__ == "__main__":
    asyncio.run(main())
"""