# -*- coding: utf-8 -*-

#Imports:
import bs4 as bs
import urllib.request
import pickle
import requests
import os
import pandas as pd

def open_share_hist(ticker):
  """
  queries shares outstanding from sharesoutstandinghistory.com 
  for a given ticker

  Parameters ---------- 
  ticker : stock ticker

  Returns -------------
  DataFrame with 'Date' and 'SharesOut'

  """
  
  #make sure ticker is lower case
  ticker = ticker.lower()
  
  #if rerunning on stock, load the pickle
  if os.path.exists('SharesOutstanding_{}.pickle'.format(ticker)):
    with open('SharesOutstanding_{}.pickle'.format(ticker), "rb") as f:
            sh_os = pickle.load(f)
  
  #if first run on stock, scrape it, then save the pickle
  if not os.path.exists('SharesOutstanding_{}.pickle'.format(ticker)):
    resp = requests.get('https://www.sharesoutstandinghistory.com/{}/'.format(ticker))
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'class': 'infotable'})

    sh_os = pd.DataFrame(data=[],columns=["Date","SharesOut"])
    for row in table.findAll('tr')[3:]:
        sh_date = row.findAll('td')[0].text
        sh_out = row.findAll('td')[1].text
        sh_os = sh_os.append({'Date': sh_date, 'SharesOut': sh_out}, ignore_index=True)
       
    with open('SharesOutstanding_{}.pickle'.format(ticker),"wb") as f:
        pickle.dump(sh_os,f)
    
  sh_os['SharesOut'] = pd.to_numeric(sh_os['SharesOut'].replace(mapping, regex=True))
    
  return(sh_os)
