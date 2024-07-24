import re
import os
import time
import requests

def getPageNum(bookID, chapterID):
    u = f"https://m.ikbook8.com/book/{bookID}/{chapterID}.html"
    r = requests.get(u)
    raw = r.content.decode("gbk",errors="ignore")
    pageNum = re.findall(r'共(.*?)页', raw, re.M | re.I)
    return pageNum[0]

def getChapterName(bookID, chapterID):
    u = f"https://m.ikbook8.com/book/{bookID}/{chapterID}.html"
    r = requests.get(u)
    raw = r.content.decode("gbk",errors="ignore")
    pageName = re.findall(r'<title>(.*?)</title>', raw, re.M | re.I)
    return pageName[0]

def getPageContent(bookID, chapterID, pageNum):
    try:
        u = f"https://m.ikbook8.com/book/{bookID}/{chapterID}_{pageNum+1}.html"
        r = requests.get(u)
        raw = r.content.decode("gbk",errors="ignore")
        pageContentRaw = re.findall(r'<div class="content">(.*?)</div>', raw, re.M | re.I | re.DOTALL)
        pageContent = ""
        for sentence in pageContentRaw[1].split('<br />'):
            if "&nbsp;&nbsp;&nbsp;&nbsp;" in sentence and "<br/>" not in sentence:
                pageContent += sentence.replace('&nbsp;&nbsp;&nbsp;&nbsp;', '')
        return pageContent
    except:
        logINFO("ERROR", f"Func:getPageContent, bookID:{bookID},chapterID:{chapterID},pageNum:{pageNum}")

def getChapterNum(bookID):
    u = f"https://m.ikbook8.com/book/{bookID}.html"
    r = requests.get(u)
    raw = r.content.decode("gbk",errors="ignore")
    chapterNum = re.findall(r'共(.*?)页', raw, re.M | re.I)
    return int(chapterNum[0])

def getChapterDetail(bookID, chapterNum):
    try:
        chapterDetail = []
        for i in range(chapterNum):
            u = f"https://m.ikbook8.com/book/{bookID}/{i+1}/"
            r = requests.get(u)
            raw = r.content.decode("gbk",errors="ignore")
            chapterNumRaw = re.findall(r'<a href="(.*?)class="cp_1">', raw, re.M | re.I)
            for raw in chapterNumRaw:
                chapterUrl = re.findall(r'https://m.ikbook8.com/(.*?)html', raw, re.M | re.I)
                chapterDetail.append(chapterUrl[0].split('/')[-1][:-1])
            time.sleep(SLEEP_SECONDS)
        return chapterDetail
    except:
        logINFO("ERROR", f"Func:getChapterDetail, bookID:{bookID}, chapterNum:{chapterNum}")

def getBookName(bookID):
    try:
        u = f"https://m.ikbook8.com/book/{bookID}.html"
        r = requests.get(u)
        raw = r.content.decode("gbk",errors="ignore")
        bookName = re.findall(r'<meta property="og:title" content="(.*?)"/>', raw, re.M | re.I)
        return bookName[0]
    except:
        logINFO("ERROR", f"Func:getBookName, bookID:{bookID}")

def logINFO(logType, logMessage):
    print(f"[{logType}]:{logMessage}")

DEBUG_MODE = False
SLEEP_SECONDS = 1

if not DEBUG_MODE:
    #bookID = "225805058"
    print(f"Sample:https://m.ikbook8.com/book/bookID.html")
    bookID = input("请输入bookID：")
    bookName = getBookName(bookID)
    curPath = os.getcwd()
    with open(f"{curPath}/{bookName}.txt", "w") as f:
        logINFO("INFO",f"下载文档为{curPath}/{bookName}.txt")
        logINFO("WARN", f"当前单页下载间隔为{SLEEP_SECONDS}秒")
        chapterNum = getChapterNum(bookID)
        chapterDetail = getChapterDetail(bookID, chapterNum)
        chapterNumLog = 0
        for chapterID in chapterDetail:
            pageNum = getPageNum(bookID, chapterID)
            chapterName = getChapterName(bookID, chapterID)
            chapterContent = ""
            for page in range(int(pageNum)):
                chapterContent += getPageContent(bookID, chapterID, page)
                chapterContent += "\n"
                logINFO("INFO",f"下载完毕：{chapterName}[第{page+1}页/共{pageNum}页]")
                time.sleep(SLEEP_SECONDS)
            f.write(chapterContent)
            chapterNumLog += 1
            logINFO("INFO", f"下载完毕：chapterID:{chapterID}[第{chapterNumLog}章/共{len(chapterDetail)}章]")
            time.sleep(SLEEP_SECONDS)
    f.close()
    logINFO("INFO", f"下载文档为{curPath}/{bookName}.txt")
    input("键入任意字符结束……")
else:
    bookID = "225805058"
    chapterID = "32620226"
    pageNum = getPageNum(bookID, chapterID)
    print(pageNum)

