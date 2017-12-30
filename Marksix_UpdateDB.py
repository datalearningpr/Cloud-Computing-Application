import time
import os
import re
import sys
from selenium import webdriver
from bs4 import BeautifulSoup  
from datetime import datetime
from sqlalchemy.sql import func
from app import db, Result
s = db.session()



# this function helps process the webscrape data
def ProcessResultTable(ResultTable):

    if len(ResultTable)% 4 != 0:
        raise Exception('Wrong ResultTable input, row number not correct.')

    ProcessedList=[]

    for i in range(len(ResultTable)//4):
        
        RowDict={}

        col1=i*4
        col2=i*4+1
        col3=i*4+2
        col4=i*4+3

        RowDict['DrawNumber'] = ResultTable[col1].get_text(strip=True)
        RowDict['DrawDate']   = datetime.strptime(ResultTable[col2].get_text(strip=True), '%d/%m/%Y').date()
        
        
        # there is bug in the website data
        if (RowDict['DrawNumber'] =='93/092') & (RowDict['DrawDate'] == datetime(year=1993, month=11, day=30).date()):
            RowDict['DrawNumber'] ='93/093' 

        RowDict['DrawName']   = ResultTable[col3].get_text(strip=True)

        srcList=[x['src'] for x in ResultTable[col4].findAll('img',{'src': re.compile('.*_[0-9][0-9]_.*')})]

        numList=list(map(lambda x: int(re.compile('_[0-9][0-9]_').findall(x)[0][1:3]),
            srcList))

        RowDict['Number1']=numList[0]
        RowDict['Number2']=numList[1]
        RowDict['Number3']=numList[2]
        RowDict['Number4']=numList[3]
        RowDict['Number5']=numList[4]
        RowDict['Number6']=numList[5]

        RowDict['NumberSpecial']=numList[6]

        ProcessedList.append(RowDict)

    return ProcessedList




# this function will update the marksix database
def updateDB():
  
    # use headless explorer
    driver = webdriver.PhantomJS()

    driver.get("http://bet.hkjc.com/marksix/Results.aspx?lang=en")
    time.sleep(0.5)

    driver.find_element_by_id("radioDrawDate").click()
    driver.execute_script("SetHiddenValue('hiddenSelectDrawFromMonth', '01');\
                         SetHiddenValue('hiddenSelectDrawFromYear', '1993');\
                         OnSearchSubmit();")
    time.sleep(1)
    flag=True
    
    maxDate = s.query(func.max(Result.drawdate).label('max_date')).scalar() 
    if maxDate is None:
        maxDate = "1993-01-05"   # first episode date
    else:
        maxDate = maxDate.strftime('%Y-%m-%d')
    toFind=datetime.strptime(maxDate, "%Y-%m-%d").strftime('%d/%m/%Y')+'.*'


    result = ""
    pagenum=0
    while(flag):

        html = driver.page_source
        bs = BeautifulSoup(html, 'html.parser')

        if bs.find(text=re.compile(toFind)) is not None:
            flag = False

        resulttable = bs.find("table",{"id":"_ctl0_ContentPlaceHolder1_resultsMarkSix_markSixResultTable"})
        resultset = bs.findAll("td",{"class":{"tableResult1","tableResult2"}})

        ProcessedResult=ProcessResultTable(resultset)

        if len(ProcessedResult)!=0:

            for count, i in enumerate(ProcessedResult):            
                new_record = Result(i)

                if pagenum == 0 and count == 0:
                    result = new_record.drawdate.strftime('%Y-%m-%d')

                check = Result.query.filter_by(drawnumber = new_record.drawnumber).first()
                if not check:
                    s.add(new_record)
            
            s.commit()

        driver.find_elements_by_xpath("//*[contains(text(), 'Next>>')]")[0].click()
        pagenum+=1
        
        time.sleep(0.2)

    driver.quit()  
    return result


