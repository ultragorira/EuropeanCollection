#Author: Loris De Luca
import os
import json
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

base_dir = os.path.dirname(__file__)
JSON_Folder = os.path.join(base_dir, 'JSON_Output/')

if not os.path.exists(JSON_Folder):
  os.makedirs(JSON_Folder)


def getData():
  #Google Sheet
  scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive.file','https://www.googleapis.com/auth/drive']
  creds = ServiceAccountCredentials.from_json_keyfile_name('EuropeanColl_Creds.json', scope)
  client = gspread.authorize(creds)
  sheet = client.open('EUCOLLPython').worksheet('JSON_Raw_Py')

  df = pd.DataFrame(sheet.get_all_records())
  #print(df)
  print('Getting Data from Gsheet ' + sheet.title) 
  createJSONs(df)

def createJSONs(full_data):

  # List to hold dictionaries
  json_list = []
  fileCount = 0
  # Iterate through each row in worksheet and fetch values into dict
  for rownum in range(len(full_data.index)):
      #data = OrderedDict()
      data = {}
      #row_values = full_data.row_values(rownum)
      data['sessionLocalStartTime'] = int(full_data['sessionLocalStartTime'][rownum]) 
      data['audioFileName'] = full_data['audioFileName'][rownum]
      data['collectionId'] = full_data['collectionId'][rownum]
      data['collectionUuid'] = full_data['collectionUuid'][rownum] 
      data['audioFormat'] = {}
      if (full_data['bigEndian'][rownum] == 'Little'):
          endian = "true"
      else:
          endian = "false" 
      data['audioFormat']['bigEndian'] = endian
      data['audioFormat']['channels'] = int(full_data['channels'][rownum])
      data['audioFormat']['encoding'] = full_data['encoding'][rownum]
      data['audioFormat']['frameRate'] = int(full_data['frameRate'][rownum])
      data['audioFormat']['frameSize'] = int(full_data['frameSize'][rownum])
      data['audioFormat']['sampleRate'] = int(full_data['sampleRate'][rownum])
      data['audioFormat']['sampleSizeInBits'] = int(full_data['sampleSizeInBits'][rownum])
      data['audioFormat']['audioDurationMillis'] = int(full_data['audioDurationMillis'][rownum])
      data['audioFormat']['format'] = full_data['format'][rownum]
      data['audioFormat']['sourceType'] = full_data['sourceType'][rownum]
      data['sessionInfo'] = {}
      data['sessionInfo']['languageCollected'] = full_data['language_collected'][rownum]
      data['sessionInfo']['ageRange'] = full_data['age_range'][rownum]
      data['sessionInfo']['gender'] = full_data['gender'][rownum]
      data['sessionInfo']['countryLived'] = full_data['country_lived'][rownum]
      data['sessionInfo']['languageSpokenDaily'] = full_data['language_spoken_daily'][rownum]
      data['sessionInfo']['primaryMicrophone'] = full_data['primaryMicrophone'][rownum]
      data['transcription'] = {}
      data['transcription']['audioDurationMillis'] = int(full_data['audioDurationMillis'][rownum])
      data['transcription']['domain'] = full_data['domain'][rownum]
      data['transcription']['id'] = str(full_data['id'][rownum])
      data['transcription']['phrase'] = full_data['phrase'][rownum]
      data['transcription']['startEndpoint'] = full_data['startEndpoint'][rownum]
      data['transcription']['stopEndpoint'] = full_data['stopEndpoint'][rownum]
      data['transcription']['type'] = full_data['type'][rownum]
      data['transcription']['qualityChecks'] = {}
      data['transcription']['wakeword'] = full_data['wakeword'][rownum]
      data['transcription']['intent'] = full_data['intent'][rownum]
      data['additionalMetadata'] = {}
      data['additionalMetadata']['annotation'] = "null"
      data['additionalMetadata']['phoneModel'] = full_data['phoneModel'][rownum]
      data['additionalMetadata']['phoneBrand'] = full_data['phoneBrand'][rownum]
      data['additionalMetadata']['speakerId'] = full_data['speakerId'][rownum]
      data['additionalMetadata']['dialect'] = full_data['dialect'][rownum]
      data['additionalMetadata']['backgroundNoiseLevelInDb'] = full_data['backgroundNoiseLevelInDb'][rownum]
      data['additionalMetadata']['operatingSystem'] = full_data['operatingSystem'][rownum]
      data['additionalMetadata']['backgroundNoise'] = full_data['backgroundNoise'][rownum]
      data['additionalMetadata']['SNR'] = str(full_data['SNR'][rownum])
 


      #json_list.append(data)
      # Serialize the list of dicts to JSON
      if data['sessionLocalStartTime'] == "None" or data['sessionLocalStartTime'] == "" or data['sessionLocalStartTime'] == None:
        break
      j = json.dumps(data, indent=4, ensure_ascii=False).encode('utf8')
      # Write to file
      with open(os.path.join(JSON_Folder, data['audioFileName'].replace('wav','') + 'json'), 'wb') as f:
        f.write(j)
        json_list.clear()
      fileCount += 1
  print("{} JSON files have been generated!".format(fileCount))
  os.startfile(JSON_Folder)

  # Run the file standalone.
if __name__=="__main__":
    getData()