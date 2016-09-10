# -*- coding: utf-8 -*-
"""
Created on Fri Apr 29 18:17:08 2016

@author: Adi
"""
import urllib;
import re;

def getMCData(currentSharePrice, sentimentList, BValue, TDebt, TAssets, NProfit, NProfit_Qtr, tempUrl):
    
    j=0;
    for i in tempUrl:
        
        i = str(i).replace("b'","")
        i = str(i).replace("'","")
        i = str(i).replace("[","")
        i = str(i).replace("]","")
        print(i)
        file = urllib.request.urlopen(i);
        text = file.read();
        
        regex = b'<span class="pl_txt wrd" style="width:(\d+)';
        pattern_SL =  re.compile(regex);  
        x=re.findall(pattern_SL, text) 
        sentimentList.append([])
        if(x == []) :
            regex = b'<span class="pl_txt wrd rtxt" style="width:(\d+)';
            pattern_SL =  re.compile(regex);
            x=re.findall(pattern_SL, text) 
            if x == []:
                sentimentList[j].append(int(0))
                sentimentList[j].append(int(0))
            else:
                sentimentList[j].append(100-int(x[0]))  
                sentimentList[j].append(int(x[0]))
        else:
            sentimentList[j].append(int(x[0]))       
            sentimentList[j].append(100-int(x[0]))  
        
        # Current share price data from Money Control
        regex = b'id="Nse_Prc_tick"><strong>(\d+(\.)?(\d+)?)'
        pattern_SPrice = re.compile(regex);
        currentSharePrice.append((re.findall(pattern_SPrice, text))[0][0])
        
        # Book Value data from Money Control
        regex = b'BOOK [^.]*">(\d+\.\d+)'
        pattern_BValue = re.compile(regex);
        BValue.append((re.findall(pattern_BValue, text))[0])

        #Total debt expressions
        regex = b'Total Debt[^.]*">(\d+(\,)?(\d+)?(\.)?(\d+)?)'
        pattern_TAssets = re.compile(regex); 
        TDebt.append((re.findall(pattern_TAssets, text))[0][0])
        
        #Total Assets expressions
        regex = b'Total Assets[^.]*">(\d+(\,)?(\d+)?(\.)?(\d+)?)'
        pattern_TAssets = re.compile(regex); 
        TAssets.append((re.findall(pattern_TAssets, text))[0][0])

        regex = b'gD_12" >Net Profit([^.]*">((-)?\d+(\,)?(\d+)?(\.)?(\d+)?))([^.]*">((-)?\d+(\,)?(\d+)?(\.)?(\d+)))([^.]*">((-)?\d+(\,)?(\d+)?(\.)?(\d+)))([^.]*">((-)?\d+(\,)?(\d+)?(\.)?(\d+)))'
        
        regex_month = b'gL_10 tar">((\w+)\'(\d+))';
        pattern_Month = re.compile(regex_month);
        z = re.findall(pattern_Month, text)
        
        regex_month = b'"PR20">((\w+)\'(\d+))';
        pattern_Month = re.compile(regex_month); 
        z1 = re.findall(pattern_Month, text)
#        print(z)
        pattern_TB = re.compile(regex);
        x = re.findall(pattern_TB, text)
        NProfit.append([])  
        NProfit_Qtr.append([])
        c=0;
        for i in (1,8,15,22):
            if c==3:
                NProfit_Qtr[j].append(z1[0][0])  
            else:
                NProfit_Qtr[j].append(z[c][0])    
            NProfit[j].append(x[0][i])
            c=c+1
        j=j+1;
#        print(NProfit_Qtr)
#    print(NProfit)
#    print(NProfit_Qtr)
#    return   sentimentList;  
    
def getMCUrls(x, z):
    tempUrl = []
    j=0
    for i in x:
#        print(i)
#        j=j+1;
        name = "";
        name = i
        name = str(name).replace(" ", "");
        url = 'http://www.moneycontrol.com/mccode/common/autosuggesion.php?query='+name+'&type=1&format=json&callback=suggest1';
        file = urllib.request.urlopen(url);
        text = file.read();
        if 'javascript:void(0)' in str(text) != True:
            name = z[j]
            name = str(name).replace(" ", ""); 
#            print("ISIN FAILED -------------------")
            url = 'http://www.moneycontrol.com/mccode/common/autosuggesion.php?query='+name+'&type=1&format=json&callback=suggest1';
            file = urllib.request.urlopen(url);
            text = file.read();    

        regex = b'link_src":"(.+?)"';
        pattern = re.compile(regex);
        
#        print(re.findall(pattern, text))
        tempUrl.append(re.findall(pattern, text)[0])
#        print(tempUrl)
#        tempUrl[j] = str(tempUrl[j]).replace("b'", ""); 
#        tempUrl[j] = str(tempUrl[j]).replace("'", ""); 
#        linkUrl.append(tempUrl)
#        print("Here")        
#        print(tempUrl)
        j=j+1
#    print(linkUrl)
    return(tempUrl)

def funcMC(currentSharePrice, sentimentList, BValue, TDebt, TAssets, NProfit, NProfit_Qtr, x, z):    
    print("IN MC ----------------------------------------")
    print(x)
    tempUrl = getMCUrls(x, z)
    #    print(tempUrl)
    getMCData(currentSharePrice, sentimentList, BValue, TDebt, TAssets, NProfit, NProfit_Qtr, tempUrl)
#    writeOtherData(sentimentList, BValue, TDebt, TAssets, NProfit, NProfit_Qtr)
#print(tempUrl)

