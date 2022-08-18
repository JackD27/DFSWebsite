import pandas as pd
import json 
from urllib.request import Request, urlopen

def fileGrabber(sportName=None):
        req = Request('https://api.prizepicks.com/projections', headers={'User-Agent': 'Mozilla/5.0'})
        dataFile = json.loads(urlopen(req).read())
        names = []
        for dataNames in dataFile['included']:
                #print('Player ID: ',dataNames['id'], 'Name: ',dataNames['attributes']['name'])
                names.append({
                        'PID': dataNames['id'],
                        'Name': dataNames['attributes']['name']
                })
        namesFrame = pd.DataFrame(names)


        projections = []
        for dataText in dataFile['data']:
                #print('Projection Type: ', dataText['attributes']['projection_type'], "Stat Type: ", dataText['attributes']['stat_type'])
                projections.append({
                        'Projection Type': dataText['attributes']['projection_type'],
                        'Stat Type': dataText['attributes']['stat_type'],
                        'OverUnder': dataText['attributes']['line_score'],
                        'PID': dataText['relationships']['new_player']['data']['id'],
                        'LID': dataText['relationships']['league']['data']['id']
                
                })
        
        dataFrame = pd.DataFrame(projections)

        finalFrame = pd.merge(dataFrame, namesFrame)
        #region Change League Names
        finalFrame.loc[finalFrame['LID'] == "7", 'League'] = 'NBA'
        finalFrame.loc[finalFrame['LID'] == "8", 'League'] = 'NHL'
        finalFrame.loc[finalFrame['LID'] == "2", 'League'] = 'MLB'
        finalFrame.loc[finalFrame['LID'] == "3", 'League'] = 'WNBA'
        finalFrame.loc[finalFrame['LID'] == "191", 'League'] = 'USFL'
        finalFrame.loc[finalFrame['LID'] == "121", 'League'] = 'LoL'
        finalFrame.loc[finalFrame['LID'] == "162", 'League'] = 'Cricket'
        finalFrame.loc[finalFrame['LID'] == "12", 'League'] = 'UFC'
        finalFrame.loc[finalFrame['LID'] == "1", 'League'] = 'PGA'
        finalFrame.loc[finalFrame['LID'] == "145", 'League'] = 'CoD'
        finalFrame.loc[finalFrame['LID'] == "5", 'League'] = 'Tennis'
        finalFrame.loc[finalFrame['LID'] == "124", 'League'] = 'CSGO'
        finalFrame.loc[finalFrame['LID'] == "11", 'League'] = 'CFL'
        finalFrame.loc[finalFrame['LID'] == "82", 'League'] = 'FIFA'
        finalFrame.loc[finalFrame['LID'] == "189", 'League'] = 'NCAA Baseball'
        finalFrame.loc[finalFrame['LID'] == "231", 'League'] = 'MLB Live'
        finalFrame.loc[finalFrame['LID'] == "193", 'League'] = 'WNBA1H'
        finalFrame.loc[finalFrame['LID'] == "163", 'League'] = 'NFLFUT'
        finalFrame.loc[finalFrame['LID'] == "9", 'League'] = 'NFL'
        finalFrame.loc[finalFrame['LID'] == "157", 'League'] = 'DISC'
        finalFrame.loc[finalFrame['LID'] == "230", 'League'] = 'LAX'
        finalFrame.loc[finalFrame['LID'] == "159", 'League'] = 'VAL'
        finalFrame.loc[finalFrame['LID'] == "172", 'League'] = 'CFBFUT'
        #endregion
        finalFrame = finalFrame.sort_values(by=['League'])
        finalFrame = finalFrame[['LID', 'Projection Type', 'Stat Type', 'Name','OverUnder', 'League']]
        
        if sportName == None:
                return finalFrame
        else:
                finalFrame = finalFrame.loc[finalFrame['League'] == sportName]
                return finalFrame
        
        return finalFrame

    
def overUnderCalc(dataFile):
        file = fileGrabber()
        newDf = pd.DataFrame(dataFile, columns=['Name', 'fpts'])

        result = newDf.merge(file, how='inner')
        result = result[result["Projection Type"].str.contains("Fantasy Score") == True]
        difference = result["fpts"] - result["OverUnder"]
        result['Difference'] = difference.round(decimals=2)
        result = result[['Name', 'League','OverUnder', 'fpts', 'Difference']].sort_values(by='Difference', ascending=False)
        return result


ALLOWED_EXTENSIONS = set(['csv'])

def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
   