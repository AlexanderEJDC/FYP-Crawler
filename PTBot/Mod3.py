from telegram import Update
from telegram.ext import MessageHandler, filters, ApplicationBuilder, ContextTypes

import os
import re
import vt

mainDirectory = "/home/alexander/FYP-Crawler GitRepo/FYP-Crawler/Data"
VT_API_KEY = "4206453d8d313a93b6660e2287494cef879cf7348d2af8b3b8884a260d1f7b8e"

#VirusTotal Functions

async def mainFileUpload(API_KEY, filePath):
#Section to upload hashes to VT
    async with vt.Client(API_KEY) as client: #Setup client
        with open(filePath) as f: #Find the file, encode as utf8
            analysis = await client.scan_file_async(file=f) #Grab the analysis with the file scan
            print(f"File {filePath} uploaded.") #Show the file was uploaded to VT
        
        #Wait to get the analysis, then print the stats
        finAnalysis = await client.wait_for_analysis_completion(analysis)
        print(f"{filePath}: {finAnalysis.stats}")
        print(f"analysis id: {finAnalysis.id}")

async def mainURLScan(API_KEY, URL_link):
    #Send URL to scan
    async with vt.Client(API_KEY) as client:
        url_analysis = await client.scan_url_async(URL_link)
        finURL_Analysis = await client.wait_for_analysis_completion(url_analysis)
        print(f"{URL_link}: {finURL_Analysis.stats}")

#Series of functions to create the relevant files in the data folder. 

def appendTxt(titleOfRoom, message):
    file = open(mainDirectory+"/"+titleOfRoom+"-Messages.txt", 'a')
    file.write(message + "\n")
    file.close() 

def makeTxt(titleOfRoom):
    file = open(mainDirectory+"/"+titleOfRoom+"-Messages.txt", 'x')
    file.close() 

def checkFileExsits(titleOfRoom): #Check if the txt already exists
    status = os.path.exists(mainDirectory+"/"+titleOfRoom+"-Messages.txt")
    if status == True:    
        return True
    elif status == False: 
        return False
    else:
        print("checkDirExists Broke! Assume False!")
        return False

    #What gets passed to the main program - uses all of the above.    
def fileCheckConditional(roomTitle, message):
    if checkFileExsits(roomTitle) == True:
        appendTxt(roomTitle, message)
    elif checkFileExsits(roomTitle) == False:
        makeTxt(roomTitle)
        appendTxt(roomTitle, message)
"""
    Now for URLS! 
    Could this be more efficient and be merged? Yes.
    Do I give a fuck? No. 
"""
def appendURLTxt(titleOfRoom, message):
    file = open(mainDirectory+"/"+titleOfRoom+"-URLs.txt", 'a')
    file.write(message + "\n")
    file.close() 

def makeURLTxt(titleOfRoom):
    file = open(mainDirectory+"/"+titleOfRoom+"-URLs.txt", 'x')
    file.close() 

def checkURLFileExsits(titleOfRoom): #Check if the URL txt already exists
    status = os.path.exists(mainDirectory+"/"+titleOfRoom+"-URLs.txt")
    if status == True:    
        return True
    elif status == False: 
        return False
    else:
        print("checkDirExists Broke! Assume False!")
        return False

    #Uses above for URLs specifically. 
def URLCheckConditional(roomTitle, message):
    if checkURLFileExsits(roomTitle) == True:
        appendURLTxt(roomTitle, message)
    elif checkURLFileExsits(roomTitle) == False:
        makeURLTxt(roomTitle)
        appendURLTxt(roomTitle, message)

#Checks to see if a DM or other form of chat, as DM's don't have titles. 
def checkUpdateType(update):
    if update.effective_chat.type == "private":
        return update.effective_chat.first_name
    else: 
        return update.effective_chat.title 
    
#Scan for a URL in a message
def URLScanMessage(message):
    URLs = re.findall(r'(https?://[^\s]+)',message)
    if URLs: #If there was a URL in the message
        return True, URLs #Return true and the list
    else: #Else assume no URLs, return false and the empty list
        return False, URLs


"""
    TODO: 
    Check if a DM or a group/channel update! CHECK
    Check for URL in messages! CHECK
    Grab entire chat history! NOT POSSIBLE - BOTS DON'T HAVE ACCESS
    Finish VTScripts! CHECK
    Add report storage for VT hashes
"""

#Reads any messages in an update
async def ReadAllMsgs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update)
    message = update._effective_message.text
    print(message)
    roomTitle = checkUpdateType(update)
    print(roomTitle)
    fileCheckConditional(roomTitle,message)
    bool, urlList = URLScanMessage(message)
    if bool == True:
        for item in urlList: 
            URLCheckConditional(roomTitle,item)
            print("URL added to list")
            await mainURLScan(VT_API_KEY, item)
    else: #Assume bool is false, dead end.
        return 0

#Grabs a file from any update
async def GrabFile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    fileHeader = checkUpdateType(update) #Get the channel name where its from
    incom_file = await update.effective_message.effective_attachment.get_file() 
    pathToFile = '/home/alexander/FYP-Crawler GitRepo/FYP-Crawler/Data/Files/'+fileHeader+"_"+incom_file.file_id
    await incom_file.download_to_drive(custom_path=f'{pathToFile}')
    print("File recieved!")

    await mainFileUpload(VT_API_KEY, pathToFile)
    print("Sent to VT") 

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