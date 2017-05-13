#MLA Generator
#David Ma

import sys
import webbrowser
from tkinter import *
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import quote
from tkinter.messagebox import *
from urllib.request import urlopen

def asciiCheck(content):
    out=''
    for i in content:
        try:
            i.encode('ascii')
        except Exception:
            out=out+quote(i)
        else:
            out=out+i
    return out

def checkUpdate():
    version='1.2.5'
    url='https://raw.githubusercontent.com/davidmaamoaix/MLA-Generator/master/Version'
    try:
        html=urlopen(url)
    except Exception:
        alert('Error: Internet is not available')
    bsObj=BeautifulSoup(html,'lxml')
    text=bsObj.find('body')
    x=[]
    if text.text.split('\n')[0]!=version:
        x.append(True)
        x.append(text.text.split('\n')[1])
    else:
        x.append(False)
        x.append(text.text.split('\n')[1])
    return x

def runUpdate():
    global x
    webbrowser.open(x[1])

def checkForLicense():
    url='https://raw.githubusercontent.com/davidmaamoaix/MLA-Generator/master/GeneratorLicense'
    try:
        html=urlopen(url)
    except Exception:
        alert('Error: Internet is not available')
    bsObj=BeautifulSoup(html,'lxml')
    text=bsObj.find('body')
    if text.text.split('\n')[0]=='Enabled':
        return True
    else:
        return text.text.split('\n')[0]

def alert(content,title='Error',exitAfter=True):
    showinfo(title,content)
    if exitAfter:
        sys.exit(0)
        exit()

def run():
    global urlEntry
    url=urlEntry.get()
    try:
        html=urlopen(asciiCheck(url))
    except Exception:
        alert('Error: URL cannot be reached')
    bsObj=BeautifulSoup(html,'lxml')

    #License Check
    licenseText=checkForLicense()
    print(licenseText)
    if licenseText!=True:
        alert(licenseText)
    
    #Article Title
    articleTitle=bsObj.find('h1').text
    if articleTitle==None:
        articleTitle=bsObj.find('title').text
    articleTitle='"'+articleTitle+'.'+'" '

    #Website Title
    try:
        titlePage=urlopen(url.split('//')[0]+'//'+url.split('//')[1].split('/')[0])
    except Exception:
        alert('Error: URL cannot be reached')
    titleBsObj=BeautifulSoup(titlePage,"lxml")
    websiteTitle=titleBsObj.find('title').text
    if ',' in websiteTitle:
        websiteTitle=websiteTitle.split(',')[0]
    elif '_' in websiteTitle:
        websiteTitle=websiteTitle.split('_')[0]
    elif '-' in websiteTitle:
        websiteTitle=websiteTitle.split(' - ')[0]
    websiteTitle=websiteTitle+', '

    #Sponsor
    if 'wikipedia' in url:
        sponsor='Wikimedia Foundation, '
    else:
        sponsor=''

    #Created Date
    createdDate=''
    try:
        if 'wikipedia.org' in url:
            href=bsObj.find('a',{'accesskey':'h'})
            historyPage=urlopen(url.split('//')[0]+'//'+url.split('//')[1].split('/')[0]+href.attrs['href'])
            historyObj=BeautifulSoup(historyPage,'lxml')
            createdDate=historyObj.find('a',{'class':'mw-changeslist-date'}).text.split(', ')[1]+', '
    except Exception:
        createdDate=''

    #Accessed Date
    month=['January','Febuary','March','April','May','June','July','August','September','October','November','December']
    accessedDate=str(datetime.now().day)+' '+str(month[datetime.now().month-1])+' '+str(datetime.now().year)

    #Generate New URL
    url=url.split('//')[1].replace('www.','')
    
    alert(articleTitle+websiteTitle+sponsor+createdDate+url+'. Accessed '+accessedDate,'Program Finished')

window=Tk()
window.wm_title("MLA Generator")
title=Label(window,text='MLA Generator by David')
title.pack()
x=checkUpdate()
if x[0]:
    title=Label(window,text='\nAn Update is Found',fg='red')
    title.pack()
    update=Button(window,text='Update',command=runUpdate)
    update.pack()
    space=Label(window,text='\n')
    space.pack()
else:
    spacing=Label(window,text='\n\n\n')
    spacing.pack()
instruction=Label(window,text='Enter the URL:')
instruction.pack()
urlEntry=Entry(window)
urlEntry.pack()
generate=Button(window,text='Generate',command=run)
generate.pack()
window.mainloop()
