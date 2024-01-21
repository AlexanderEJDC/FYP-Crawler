import asyncio
import itertools
import os
import sys
import vt

async def mainFileUpload(API_KEY, filePath):
    returnedValues = [] #Declare empty array for future use

#Section to upload hashes to VT
    async with vt.Client(API_KEY) as client: #Setup client
        with open(filePath, encoding="utf-8") as f: #Find the file, encode as utf8
            analysis = await client.scan_file_async(file=f) #Grab the analysis with the file scan
            print(f"File {filePath} uploaded.") #Show the file was uploaded to VT
            returnedValues.append((analysis, filePath)) #Append analysis to declared array and its path
        
        finAnalysis = await client.wait_for_analysis_completion(analysis)
        print(f"{filePath}: {finAnalysis.stats}")
        print(f"analysis id: {finAnalysis.id}")

async def mainURLScan(API_KEY, URL_link):
    #Send URL to scan
    async with vt.Client(API_KEY) as client:
        url_analysis = await client.scan_url_async(URL_link)
        finURL_Analysis = await client.wait_for_analysis_completion(url_analysis)
        print(f"{URL_link}: {finURL_Analysis.stats}")