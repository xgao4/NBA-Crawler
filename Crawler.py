import urllib
import re
import pandas as pd
import datetime
import time
import pymysql
from sqlalchemy import create_engine

#initialize pandas
pd_games_det = pd.DataFrame(columns=['Type','Team','Host','Player','Starting','Min',\
                                     'FGP','FGM','FGA','TPP','TPM','TPA',\
                                     'FTP','FTM','FTA','REB','OREB','DREB',\
                                     'AST','STL','BLK','TOV','PF','PTS','DATE'\
                                     ])

#get the whole page info
def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html
    

def getTeamName(html):
    reg = r'\<a\ href\=\"\/team.*\<\/a\>'
    team_re = re.compile(reg)
    team_list = re.findall(team_re,html)
    return team_list


def getPlayerName(html):
    reg = r'href\=\"\/player\/.*\<\/a\>'
    name_re = re.compile(reg)
    name_list = re.findall(name_re,html)
    return name_list
    
def getType(html):
    reg = r'style\=margin\-top\:10px\;\>([\d\D]*?)\<\/div\>'
    name_re = re.compile(reg)
    name_list = re.findall(name_re,html)
    return name_list
    
def getStarting(html):
    reg = r'class=\"current\ gs.*\<\/td\>'
    com_re = re.compile(reg)
    re_list = re.findall(com_re,html)
    return re_list
 
def getMin(html):
    reg = r'class=\"normal\ mp.*\<\/td\>'
    com_re = re.compile(reg)
    re_list = re.findall(com_re,html)
    return re_list

def getFGP(html):
    reg = r'class=\"normal\ fgper.*\<\/td\>'
    com_re = re.compile(reg)
    re_list = re.findall(com_re,html)
    return re_list

def getFG(html):
    reg = r'class=\"normal\ fg.*col4.*\<\/td\>'
    com_re = re.compile(reg)
    re_list = re.findall(com_re,html)
    return re_list

def getFGA(html):
    reg = r'class=\"normal\ fga.*\<\/td\>'
    com_re = re.compile(reg)
    re_list = re.findall(com_re,html)
    return re_list

def getTPP(html):
    reg = r'class=\"normal\ threepper.*\<\/td\>'
    com_re = re.compile(reg)
    re_list = re.findall(com_re,html)
    return re_list    

def getTPM(html):
    reg = r'class=\"normal\ threep.*col7.*\<\/td\>'
    com_re = re.compile(reg)
    re_list = re.findall(com_re,html)
    return re_list     
 
def getTPA(html):
    reg = r'class=\"normal\ threepa.*\<\/td\>'
    com_re = re.compile(reg)
    re_list = re.findall(com_re,html)
    return re_list 
    
def getFTP(html):
    reg = r'class=\"normal\ ftper.*\<\/td\>'
    com_re = re.compile(reg)
    re_list = re.findall(com_re,html)
    return re_list  

def getFTM(html):
    reg = r'class=\"normal\ ft.*col10.*\<\/td\>'
    com_re = re.compile(reg)
    re_list = re.findall(com_re,html)
    return re_list  

def getFTA(html):
    reg = r'class=\"normal\ fta.*\<\/td\>'
    com_re = re.compile(reg)
    re_list = re.findall(com_re,html)
    return re_list 

def getREB(html):
    reg = r'class=\"normal\ trb.*\<\/td\>'
    com_re = re.compile(reg)
    re_list = re.findall(com_re,html)
    return re_list 

def getOREB(html):
    reg = r'class=\"normal\ orb.*\<\/td\>'
    com_re = re.compile(reg)
    re_list = re.findall(com_re,html)
    return re_list
    
def getDREB(html):
    reg = r'class=\"normal\ drb.*\<\/td\>'
    com_re = re.compile(reg)
    re_list = re.findall(com_re,html)
    return re_list
    
def getAST(html):
    reg = r'class=\"normal\ ast.*\<\/td\>'
    com_re = re.compile(reg)
    re_list = re.findall(com_re,html)
    return re_list
 
def getSTL(html):
    reg = r'class=\"normal\ stl.*\<\/td\>'
    com_re = re.compile(reg)
    re_list = re.findall(com_re,html)
    return re_list
 
def getBLK(html):
    reg = r'class=\"normal\ blk.*\<\/td\>'
    com_re = re.compile(reg)
    re_list = re.findall(com_re,html)
    return re_list
    
def getTOV(html):
    reg = r'class=\"normal\ tov.*\<\/td\>'
    com_re = re.compile(reg)
    re_list = re.findall(com_re,html)
    return re_list   
    
def getPF(html):
    reg = r'class=\"normal\ pf.*\<\/td\>'
    com_re = re.compile(reg)
    re_list = re.findall(com_re,html)
    return re_list  
def getPTS(html):
    reg = r'class=\"normal\ pts.*\<\/td\>'
    com_re = re.compile(reg)
    re_list = re.findall(com_re,html)
    return re_list
    
def getDate(html):
    reg = r'\<div\ style\=([\d\D]*?)<div class="basic">'
    com_re = re.compile(reg)
    re_list = re.findall(com_re,html)
    return re_list
    
  
def get_team_player(html):
    reg = r'\<div\ class\=\"title\"([\d\D]*?)\<tr\ class\=\"team\_all\_tr\"\>'
    player_re = re.compile(reg)
    player_list = re.findall(player_re,html)
    
    gameDate = re.split('>|<',getDate(player_list[0])[0])[1]
    
    Type = re.split('\n',getType(player_list[0])[0])[2]
    
    visit_team = re.split('>|<',getTeamName(player_list[0])[2])[2]
   
    host_team = re.split('>|<',getTeamName(player_list[1])[0])[2]
    
    v_player_num = len(getPlayerName(player_list[0]))
    h_player_num = len(getPlayerName(player_list[1]))
    
    v_index = pd_games_det['Team'].count()
    h_index = pd_games_det['Team'].count() + v_player_num
    for i in range(0,v_player_num):
      v_player = re.split('>|<',getPlayerName(player_list[0])[i])[1]
      v_starting = re.split('>|<',    getStarting(player_list[0])[i])[1]
      v_min = re.split('>|<',    getMin(player_list[0])[i])[1]
      v_fgp = re.split('>|<',    getFGP(player_list[0])[i])[1]
      v_fg = re.split('>|<',    getFG(player_list[0])[i])[1]
      v_fga = re.split('>|<',    getFGA(player_list[0])[i])[1]
      v_tpp = re.split('>|<',    getTPP(player_list[0])[i])[1]
      v_tpm = re.split('>|<',    getTPM(player_list[0])[i])[1]
      v_tpa = re.split('>|<',    getTPA(player_list[0])[i])[1]
      v_ftp = re.split('>|<',    getFTP(player_list[0])[i])[1]                     
      v_ftm = re.split('>|<',    getFTM(player_list[0])[i])[1] 
      v_fta = re.split('>|<',    getFTA(player_list[0])[i])[1] 
      v_reb = re.split('>|<',    getREB(player_list[0])[i])[1] 
      v_oreb = re.split('>|<',    getOREB(player_list[0])[i])[1] 
      v_dreb = re.split('>|<',    getDREB(player_list[0])[i])[1] 
      v_ast = re.split('>|<',    getAST(player_list[0])[i])[1] 
      v_stl = re.split('>|<',    getSTL(player_list[0])[i])[1] 
      v_blk = re.split('>|<',    getBLK(player_list[0])[i])[1] 
      v_tov = re.split('>|<',    getTOV(player_list[0])[i])[1] 
      v_pf = re.split('>|<',    getPF(player_list[0])[i])[1] 
      v_pts = re.split('>|<',    getPTS(player_list[0])[i])[1] 
      pd_games_det.loc[v_index+i] = {'Type':Type,'Team':visit_team,'Host':0,'Player':v_player,\
      'Starting':v_starting,'Min':v_min,'FGP':v_fgp,'FGM':v_fg,'FGA':v_fga,'TPP':v_tpp,\
      'TPM':v_tpm,'TPA':v_tpa,'FTP':v_ftp,'FTM':v_ftm,'FTA':v_fta,'REB':v_reb,\
      'OREB':v_oreb,'DREB':v_dreb,'AST':v_ast,'STL':v_stl,'BLK':v_blk,'TOV':v_tov,\
      'PF':v_pf,'PTS':v_pts,'DATE':gameDate}
    for i in range(0,h_player_num):
       h_player = re.split('>|<',getPlayerName(player_list[1])[i])[1]
       h_starting = re.split('>|<',    getStarting(player_list[1])[i])[1]
       h_min = re.split('>|<',    getMin(player_list[1])[i])[1]
       h_fgp = re.split('>|<',    getFGP(player_list[1])[i])[1]
       h_fg = re.split('>|<',    getFG(player_list[1])[i])[1]
       h_fga = re.split('>|<',    getFGA(player_list[1])[i])[1]
       h_tpp = re.split('>|<',    getTPP(player_list[1])[i])[1]
       h_tpm = re.split('>|<',    getTPM(player_list[1])[i])[1]
       h_tpa = re.split('>|<',    getTPA(player_list[1])[i])[1]
       h_ftp = re.split('>|<',    getFTP(player_list[1])[i])[1]                     
       h_ftm = re.split('>|<',    getFTM(player_list[1])[i])[1] 
       h_fta = re.split('>|<',    getFTA(player_list[1])[i])[1] 
       h_reb = re.split('>|<',    getREB(player_list[1])[i])[1] 
       h_oreb = re.split('>|<',    getOREB(player_list[1])[i])[1] 
       h_dreb = re.split('>|<',    getDREB(player_list[1])[i])[1] 
       h_ast = re.split('>|<',    getAST(player_list[1])[i])[1] 
       h_stl = re.split('>|<',    getSTL(player_list[1])[i])[1] 
       h_blk = re.split('>|<',    getBLK(player_list[1])[i])[1] 
       h_tov = re.split('>|<',    getTOV(player_list[1])[i])[1] 
       h_pf = re.split('>|<',    getPF(player_list[1])[i])[1] 
       h_pts = re.split('>|<',    getPTS(player_list[1])[i])[1] 
       pd_games_det.loc[h_index+i] = {'Type':Type,'Team':host_team,'Host':1,'Player':h_player,\
       'Starting':h_starting,'Min':h_min,'FGP':h_fgp,'FGM':h_fg,'FGA':h_fga,'TPP':h_tpp,\
       'TPM':h_tpm,'TPA':h_tpa,'FTP':h_ftp,'FTM':h_ftm,'FTA':h_fta,'REB':h_reb,\
       'OREB':h_oreb,'DREB':h_dreb,'AST':h_ast,'STL':h_stl,'BLK':h_blk,'TOV':h_tov,\
       'PF':h_pf,'PTS':h_pts,'DATE':gameDate}

#write the data to mysql
def to_mysql(v_pandas):
      ##length = v_pandas.count()
      conn = create_engine('mysql+pymysql://mysql:gaoxu@192.168.163.131:3306/test?charset=utf8')  
      pd.io.sql.to_sql(v_pandas,'nba_data',con=conn,\
                         index=False,\
                         if_exists='append')    

for i in range(41400,42391):
   try: 
      url = 'http://www.stat-nba.com/game/'+str(i)+'.html'
      html = getHtml(url)
      get_team_player(html)
      if i%100==0:
          print i
      to_mysql(pd_games_det)
      pd_games_det=pd_games_det.iloc[0:0]
   except (IndexError,IOError),e:
      print e
      continue
