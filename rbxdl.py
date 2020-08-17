# pylint: disable=unused-variable

#Spaghetti code time!!!

import requests, time, os, sys, argparse, json, random
from ast import literal_eval

downlUrl = 'https://www.roblox.com/asset/?id='
infoUrl = 'https://api.roblox.com/Marketplace/ProductInfo?assetId='

#Maybe I could somehow scrape this from the wiki page?
#todo: combine below with filetypes (arrays instead of strings)
assetTypes = {
  0:['Unknown', ''], #handle weird things
  1:['Image', '.png'],
  2:['TeeShirt', '.xml'],
  3:['Audio', '.xml'],
  4:['Mesh', ''],
  5:['Lua', ''],
  8:['Hat', '.xml'],
  9:['Place', '.rbxl'],
  10:['Model', '.rbxm'],
  11:['Shirt', '.xml'],
  12:['Pants', '.xml'],
  13:['Decal', '.xml'],
  17:['Head', '.xml'],
  18:['Face', '.xml'],
  19:['Gear', '.xml'],
  21:['Badge', ''],
  24:['Animation', '.xml'],
  27:['Torso', '.xml'],
  28:['RightArm', '.xml'],
  29:['LeftArm', '.xml'],
  30:['LeftLeg', '.xml'],
  31:['RightLeg', '.xml'],
  32:['Package', '.xml'],
  33:['YouTubeVideo', ''],
  34:['GamePass', '.xml'],
  38:['Plugin', '.xml'],
  39:['SolidModel', '.xml'],
  40:['MeshPart', '.rbxm'],
  41:['HairAccessory', '.xml'],
  42:['FaceAccessory', '.xml'],
  43:['NeckAccessory', '.xml'],
  44:['ShoulderAccessory', '.xml'],
  45:['FrontAccessory', '.xml'],
  46:['BackAccessory', '.xml'],
  47:['WaistAccessory', '.xml'],
  48:['ClimbAnimation', ''],
  49:['DeathAnimation', ''],
  50:['FallAnimation', ''],
  51:['IdleAnimation', ''],
  52:['JumpAnimation', ''],
  53:['RunAnimation', ''],
  54:['SwimAnimation', ''],
  55:['WalkAnimation', ''],
  56:['PoseAnimation', ''],
  57:['EarAccessory', '.xml'],
  58:['EyeAccessory', '.xml'],
  61:['EmoteAnimation', ''],
  62:['Video', '']   
}

#todo: scan the HTML of audio pages to get the actual location of the mp3
args = None

cwd = os.getcwd()
reqCooldown = 1 #prevent being rate limited (I hope)
curVer = '1.10'

print(f'Metalhead\'s ROBLOX asset downloader version: {curVer}\nType -h for help')

def getType(assetID):
  metaJsonReq = requests.get(f'{infoUrl}{assetID}')
  metaJson = metaJsonReq.json()
  if 'AssetTypeId' in metaJson:
    return metaJson['AssetTypeId']
  return 0

def writeToLogs(msg):
  logs = open('logs.txt', 'a')
  logs.write(f'####################################################################\n{msg}\n\n')
  logs.close

def makeDirectory(dirName):
  if not os.path.isdir(dirName):
    os.mkdir(dirName)

def saveFile(fname, assetID, fileMode, enc = None):
  try:
    aType = getType(assetID)
    if args.customdir:
      useDir = args.customdir
      makeDirectory(useDir)
    else:  
      useDir = 'downloads'    
      makeDirectory(useDir)
    if args.sepdir:
      makeDirectory(f'{useDir}\\{assetTypes[aType][0]}')
      makeDirectory(f'{useDir}\\{assetTypes[aType][0]}\\{assetID}')
      fileUseDir = f'{useDir}\\{assetTypes[aType][0]}\\{assetID}\\{fname}' 
    else:
      fileUseDir = f'{useDir}\\{assetTypes[aType][0]}\\{fname}'   
    makeDirectory(f'{useDir}\\{assetTypes[aType][0]}')
    if args.assetver:
        fname = f'version{args.assetver}-{fname}'
    if os.path.isfile(fileUseDir):
      os.unlink(fileUseDir)
    if enc != None:
      theFile = open(fileUseDir, fileMode, encoding='utf-8')  
    else:
      theFile = open(fileUseDir, fileMode)
    return theFile
  except Exception as e:
    print(f'Exception occured in saveFile. Logged to file')
    writeToLogs(e)

def getMeta(assetID):
  try:
    metaJsonReq = requests.get(f'{infoUrl}{assetID}')
    metaJson = metaJsonReq.json()
    assetMeta = saveFile(f'{assetID}-meta.txt', assetID, 'a', 'utf-8')
    for key in metaJson:
      if key != 'Creator':
        assetMeta.write(f'{key}: {metaJson[key]}\n')
      if key == 'Creator':
        for creaKey in metaJson[key]:
          assetMeta.write(f'{creaKey}: {metaJson[key][creaKey]}\n')
    assetMeta.close()
  except Exception as e:
    print(f'Exception occured in getMeta. Logged to file')
    writeToLogs(e)

def makeDownloadReq(assetID, tryVer = None):
  try:
    if args.assetver and tryVer == None:
      assetReq = requests.get(f'{downlUrl}{assetID}&version={args.assetver}')
      print(f'Downloading asset: {assetID} with version of: {args.assetver}')
    elif tryVer != None:
      assetReq = requests.get(f'{downlUrl}{assetID}&version={tryVer}')
      print(f'Downloading asset: {assetID} with version of: {tryVer}')    
    else:
      assetReq = requests.get(f'{downlUrl}{assetID}')
      print(f'Downloading asset: {assetID}')   

    resCode = assetReq.status_code
    if resCode == 200:
      assetType = getType(assetID)
      fExt = assetTypes[assetType][1]
      if tryVer != None:
        fName = f'{tryVer}-{assetID}{fExt}'
      else:
        fName = f'{assetID}{fExt}'
      saved = saveFile(fName, assetID, 'wb')
      saved.write(assetReq.content)
      if args.savemeta:
        getMeta(assetID)
      return 0   
    elif resCode == 404:
      print(f'asset {assetID} not found')
    elif resCode == 403:
      print(f'asset {assetID} is most likely copylocked')
    elif resCode == 429:
      print(f'Too many requests are being sent!')
    else:
      print(f'Error while downloading: {assetID} reason: HTTP {resCode}')
    return 1
  except Exception as e:
    print(f'Exception occured in makeDownloadReq. Logged to file')
    writeToLogs(e)

def doRetries(assetId):
  if not args.assetver:
    sys.exit('Please use -ver to specify the number of attempts')
  for i in range(1,args.assetver+1):
    makeDownloadReq(assetId, i)
  return 1

def download():
  idArr = literal_eval(args.assetid) #converts the input into an int or in the case of bulk and range to an array
  if args.downlmode == 'downl':
    if args.tryvers:
      doRetries(idArr)
    else:
       makeDownloadReq(idArr)
    print(f'Completed download of asset: {idArr}')
  elif args.downlmode == 'bulk':
    for i in range(len(idArr)):
      if args.tryvers:
        doRetries(idArr)
      else:
        makeDownloadReq(idArr[i])
      time.sleep(reqCooldown)
    print(f'Completed download of assets: {args.assetid}')
  elif args.downlmode == 'roulette':
    for i in range(idArr):
      while True:
        randId = random.randint(1000, 5000000000)
        if makeDownloadReq(randId) == 0:
          break
  else:
    if len(idArr) > 2:
      sys.exit(f'range mode can only have a length of 2 not {len(idArr)}')
    minRange = idArr[0]
    maxRange = idArr[1]
    for i in range(minRange, maxRange+1):
      if args.tryvers:
        doRetries(i)
      else:
        makeDownloadReq(idArr[i])
      time.sleep(reqCooldown)
    print(f'Completed download of assets between {minRange} and {maxRange}')   

def postInput():
  valid = ['downl', 'bulk', 'range', 'roulette']
  if not args.downlmode in valid:
    sys.exit(f'The specified download mode "{args.downlmode}" is invalid. Please use [-h] to get all valid options')
  download()

parser = argparse.ArgumentParser(description='Download assets from ROBLOX with various extra options')
parser.add_argument('downlmode', help='Choose between: downl, bulkdownl, rangedownl, and roulette', type=str)
parser.add_argument('assetid', help='The ID of the asset. bulk example: [id1,id2,id3, etc.]. range is the same but with a min and max id', type=str)
parser.add_argument('-ver', '--assetver', help='Version number for the asset ID', type=int)
parser.add_argument('-cdir', '--customdir', help='Saves files to a custom directory. Will create directory if it doesn\'t exist', type=str)
parser.add_argument('-spd', '--sepdir', help='Save assets in their own directories named by their ID', action='store_true')
parser.add_argument('-smt', '--savemeta', help='Save extra info of an asset (eg. creator name)', action='store_true')
parser.add_argument('-tvr', '--tryvers', help='[Warning: This is unstable] will try to download every version of the asset specified', action='store_true')
args = parser.parse_args()
postInput()
