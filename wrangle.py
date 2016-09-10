import urllib;
import re;
import csv;
import datetime
import os
import MC
def getStockData(x, stockCodes,sentimentList, BValue, TDebt, TAssets, NProfit, NProfit_Qtr):
    
    now = datetime.datetime.now();
    year = now.year;
    day = now.day;
    month = now.month;
    newYear = year-4;  
    fileNo = 0
    nameOfFile = 'analysis/stock_recommendations.csv';
    fp = open(nameOfFile, 'w');
    a = csv.writer(fp, delimiter=',',quoting=csv.QUOTE_ALL,lineterminator='\r') 
    for i in stockCodes:
        previousData = 'http://real-chart.finance.yahoo.com/table.csv?s='+i;
        cont = '.NS&amp;d='+str(month)+'&amp;e='+str(day)+'&amp;f='+str(year)+'&amp;g=d&amp;a=1&amp;b=1&amp;c='+str(newYear)+'&amp;ignore=.csv';
        stockUrl = previousData+cont;
        #print(stockUrl)
#        nameOfFile = 'analysis/'+i+'.csv';
#        print(nameOfFile)
#        fp = open(nameOfFile, 'w');
#        a = csv.writer(fp, delimiter=',',quoting=csv.QUOTE_ALL,lineterminator='\r')   
        file = urllib.request.urlopen(stockUrl);
        text = file.read();
        text = str(text)
        text=text.replace("b'", "");
        text=text.replace("'", "");
        text = text.split('\\n')
        col = 0;
        for itemToPrint in text:
            if col == 0 and fileNo != 0:
                col = col+1                
                continue;
            if fileNo == 0 and col == 0:
#                 print("Im in fileNo = 0 and col = 0")
                itemToPrint = 'Code,'+itemToPrint+',Quarters,Profits(In Cr.),Income(In Cr.), Income Range, Comparison Factors, Factors, Sentiment, Percentage';
            elif col == 1:
                itemToPrint = itemToPrint+','+str(NProfit_Qtr[fileNo][col-1])+','+str(NProfit[fileNo][col-1])+',Total Debt(In Cr.),'+str(TDebt[fileNo])+',Book Value,'+str(BValue[fileNo])+',BUY,'+str(sentimentList[fileNo][0])
            elif col == 2:
                itemToPrint = itemToPrint+','+str(NProfit_Qtr[fileNo][col-1])+','+str(NProfit[fileNo][col-1])+',Total Assets(In Cr.),'+str(TAssets[fileNo])+',Target Price,'+str(x[fileNo][1])+',SELL,'+str(sentimentList[fileNo][1])
            elif col == 3:
                itemToPrint = itemToPrint+','+str(NProfit_Qtr[fileNo][col-1])+','+str(NProfit[fileNo][col-1])+',,,Current Price,'+str(currentSharePrice[fileNo])+',,';
            elif col>3 and col<5:
                itemToPrint = itemToPrint+','+str(NProfit_Qtr[fileNo][col-1])+','+str(NProfit[fileNo][col-1]);
            
            if fileNo != 0 or col != 0:
                itemToPrint = i+','+itemToPrint
            a.writerow(itemToPrint.split(','))
            col = col+1
        
        # Logic to write other factors into the excel
#        fp.close()
        fileNo = fileNo+1
    fp.close()
    
       
def getStockSymbols(names):
    with open("EQUITY.csv", "r") as f:
        found = 0;
        stockCodes = []
#        isin = []

        for i in range(len(names)):
            f.seek(0)
            found = 0
            reader = csv.reader(f, delimiter=',', quotechar='|')
            code = str(names[i][0]).upper().split(' ')[0]
            #print('code = '+str(code))
            for row in reader:
                x = row[0].strip();
                xy = row[6].strip()
                if x == code:
                 #   print(str(x)+'----'+str(code))
                    stockCodes.append(code)
                    isin.append(xy);
                    found = 1;
                    break;
             
            if found == 0:
                #print("In here")
                f.seek(0)
                reader = csv.reader(f, delimiter=',', quotechar='|')
                code = str(names[i][0]).upper()
                #print('code = '+str(code))
                for row in reader:
                    x = row[1].strip().upper();
                    xy = row[6].strip()
                    if x.find(code) == -1:
                        continue;
                    else:
                        #print(str(x)+'----'+str(code))
                        stockCodes.append(row[0].strip())
                        isin.append(xy);
                        break;
            #key = key.upper();
                #x = row[0].strip().upper().split(' ')[0];
                 #print(x)
            #x = x.lower();
                #key = str(names[i][0])[:-1].upper()
               
#                    result.append(row[0].strip(), row[1].strip())     
#                    print(result)
#                    if(len(result) > 1):
#                        for j in result:
#                            if(str(names[i][0]).upper() == j[1]):
#                                stockCodes.append(j[0]) 
                
        
        
           
        
        #print(stockCodes)
        return stockCodes;
    
    
def getStockCodes(names, isin):
    i=0;j=0;
    for i in range(len(names)):
        for j in range(2):
          #names[i][j] = str(names[i][j]).replace(" ", "");
          names[i][j] = str(names[i][j]).replace("b'", "");
          names[i][j] = str(names[i][j]).replace("'", "");  
        #names[i][0] = str(names[i][0]).upper();
#    print(names)   
    stockCodes = getStockSymbols(names);
#    print(names)    
    print(stockCodes)
    return stockCodes
    #stockPrices = "https://in.finance.yahoo.com/q/hp?s="+str(names[4][0])+".NS";
    #print(stockPrices);
    

def formatData(currentSharePrice, sentimentList, BValue, TDebt, TAssets, NProfit, NProfit_Qtr):
    for i in NProfit_Qtr:
        for j in range(0,4):
            i[j] = str(i[j]).replace("b\"","")
            i[j] = str(i[j]).replace("\"","")
            i[j] = str(i[j]).replace("[","")
            i[j] = str(i[j]).replace("]","")

    for i in NProfit:
        for j in range(0,4):
            i[j] = str(i[j]).replace("b'","")
            i[j] = str(i[j]).replace(",","")
            i[j] = str(i[j]).replace("'","")
            i[j] = str(i[j]).replace("[","")
            i[j] = str(i[j]).replace("]","")
    
    for i,a in enumerate(BValue):
            
            BValue[i] = str(a).replace("b'","")
            BValue[i] = str(BValue[i]).replace("'","")
            BValue[i] = str(BValue[i]).replace(",","")
    for i,a in enumerate(TDebt):
            
            TDebt[i] = str(a).replace("b'","")
            TDebt[i] = str(TDebt[i]).replace("'","")
            TDebt[i] = str(TDebt[i]).replace(",","")
    for i,a in enumerate(TAssets):
            
            TAssets[i] = str(a).replace("b'","")
            TAssets[i] = str(TAssets[i]).replace("'","")
            TAssets[i] = str(TAssets[i]).replace(",","")
            
    for i,a in enumerate(currentSharePrice):
            
            currentSharePrice[i] = str(a).replace("b'","")
            currentSharePrice[i] = str(currentSharePrice[i]).replace("'","")
            currentSharePrice[i] = str(currentSharePrice[i]).replace(",","")
#    print(BValue)   
#    for i in TDebt:
#        for j in range(0,4):
#            i[j] = str(i[j]).replace("b'","")
#            i[j] = str(i[j]).replace("'","")
#        
#    for i in TAssets:
#        for j in range(0,4):
#            i[j] = str(i[j]).replace("b'","")
#            i[j] = str(i[j]).replace("'","")
#    

#url = "http://economictimes.indiatimes.com/markets/stocks/recos";
#url = "http://economictimes.indiatimes.com/markets/stocks/recos/articlelist/msid-3053611,page-1.cms"
#url = "http://economictimes.indiatimes.com/lazyloadlistnew.cms?msid=3053611&curpg=1&img=0"
url = 'http://economictimes.indiatimes.com/lazyloadlistnew.cms?msid=3053611&curpg=1&img=0'
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
#stockPrices = "https://in.finance.yahoo.com/q/hp?s=PCJEWELLER.NS";
#text = '<a href="/markets/stocks/recos/buy-reliance-capital-with-a-target-of-rs-410-mitesh-panchal/articleshow/51907461.cms">Buy Reliance Capital with a target of Rs 410: Mitesh Panchal</a>';
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
text = urllib.request.urlopen(req).read()
#file = urllib.request.urlopen(url);
#file = urllib2.urlopen(url,headers=hdr);
#text = file.read();
#print(text)
#regex = 'markets/stocks/recos/(.+?)cms$';
#regex = b'<a href="/markets/stocks/recos/buy-(.+?)</a>';
#regex = b'cms">Sell (.+?)with a target of Rs (.+?):';
#regex = b'cms">Buy (.+?)with an intra-day target of Rs (.+?):';
#regex = b'cms">Buy (.+?) with [^.]* Rs \d+: ';
regex = b'cms">Buy (.+?) (with|at) [^.]* Rs (\d+(\,)?(\d+)?): ';
#regex = b'cms">Buy (.+?)with [^.]* Rs (\d+(\,)?(\d+)?):';
#regex = b'<a href="/markets/stocks/recos/buy-(.+?)cms';
pattern = re.compile(regex);
price = re.findall(pattern, text);
#print(price)
x = []
j=0;
for i in price:
    x.append([])
    x[j].append(i[0])
    x[j].append(i[2])
    j=j+1;
#x = list(map(list, price))
#map(lambda x:x.strip('b'),x)
#print(str(x).strip("b'"))
#print(newPrice)
i=0;
#x = filter(None, x)
list(filter(None,x))
isin = []
#print(x)
stockCodes = getStockCodes(x,isin)
print(stockCodes)
sentimentList = []
BValue=[]
TDebt = []
TAssets = []
NProfit = []
NProfit_Qtr = []
currentSharePrice = []

MC.funcMC(currentSharePrice, sentimentList, BValue, TDebt, TAssets, NProfit, NProfit_Qtr, isin, stockCodes)
formatData(currentSharePrice, sentimentList, BValue, TDebt, TAssets, NProfit, NProfit_Qtr)
#print(BValue)
#print(TDebt)
#print(TAssets)
#print(NProfit)
#print(NProfit_Qtr)
print(x)
getStockData(x, stockCodes, sentimentList, BValue, TDebt, TAssets, NProfit, NProfit_Qtr)

#print(isin)
#getDataFromMC(x)
#print(x);
#a = price[0].split(',')