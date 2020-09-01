import requests, argparse, time, os, random
from ast import literal_eval
#Still have yet to find a way to reduce this... 
astTypes = {
  0:['Unknown', ''],
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
#urls used in program
astUrl = 'https://www.roblox.com/asset/?id='
apiUrl = 'https://api.roblox.com/marketplace/productinfo?assetId='
#Creates web requests and handles most errors and status codes
def makeWebReq(url):
    try:
        resp = requests.get(url)
        resp.close()
        return [resp.status_code, resp]
    except requests.RequestException as e:
        print("Exception occured whilst making request. This has been logged.")
        writeLogs(e)
#used for getting metadata of an asset
def getMeta(astId, specific = None):
    resp = makeWebReq(f'{apiUrl}{astId}')
    if resp[0] == 200:
        return resp[1].json().get(specific) or resp[1].json()
    else:
        return 0
#Reduces amount of code I need to write
def createDirectory(dirName):
    if not os.path.isdir(str(dirName)):
        os.mkdir(str(dirName))
    return(str(dirName)) 
#Save asset to file
def saveAsset(astId, astTypeStr, cDir, sDirName, astData, astVer):
    try:
        createDirectory(cDir)
        createDirectory(f'{cDir}\\{astTypeStr}')
        saveLocation = createDirectory(f'{cDir}\\{astTypeStr}\\{astId}') if sDirName is True else f'{cDir}\\{astTypeStr}'
        fileName = f'{saveLocation}\\{astId}-version{astVer}' if astVer is not None else f'{saveLocation}\\{astId}'
        assetSave = open(f'{fileName}{astTypes[getMeta(astId, "AssetTypeId")][1]}','wb+')
        assetSave.write(astData)
        assetSave.close()
        jsonMeta = getMeta(astId)
        if jsonMeta != 0:
            metaSaveLoc = f'{fileName}-META.txt'
            if not os.path.isfile(metaSaveLoc):
                metaFile = open(f'{metaSaveLoc}', 'a', encoding = 'utf-8')
                for i in jsonMeta:
                    if i == 'Creator':
                        metaFile.write('Creator: \n')
                        for e in jsonMeta[i]:
                            metaFile.write(f'\t{e} : {jsonMeta[i][e]}\n')
                    else:
                        metaFile.write(f'{i}: {jsonMeta[i]}\n')
        metaFile.close()
        return 1
    except OSError as e:
        writeLogs(e)
        return e
#Download asset  
def download(astId, astVer, args):
    cDir = args.dir if args.dir is not None else 'Downloaded'
    sDir = args.sdirs
    url = f'{astUrl}{astId}&version={astVer}' if astVer is not None else f'{astUrl}{astId}'
    print(f'Downloading: {url}...')
    resp = makeWebReq(url)
    if resp[0] == 200:
        print(f'Saving: {url}...')
        save = saveAsset(astId, astTypes[getMeta(astId, 'AssetTypeId')][0], cDir, sDir, resp[1].content, astVer)
        if save == 1:
            print(f'Saved asset sucessfully!')
        else:
            print(f'Save failed, Check logs for more info...')
        return 1
    elif resp[0] == 404:
        print('Could not download because asset was not found')
    elif resp[0] == 403:
        print('Could not download because asset is copylocked')
    else:
        print(f'Could not download due to {resp[0]}')
    return 0
#attempt to get every version of the asset
def allVer(astId, args):
    aVer = 1
    while True:
        if download(astId, aVer, args) == 0:
            break
        aVer += 1
def writeLogs(msg):
    logFile = open('rbxdl.log', 'a')
    logFile.write(f'{msg}\n\n')
    logFile.close()
#Reduces code
def startDL(astId, astVer, args, getAll=False):
    if getAll:
        allVer(astId, args)
    else:
        return download(astId, astVer, args)        
#Handle the user input 
def handleArgs(args):
    astId = literal_eval(args.assetid)
    dlm = args.downlmode
    astVer = args.ver 
    getAll = args.allVer
    if dlm == 'single':
        startDL(astId, astVer, args, getAll)
    elif dlm == 'bulk':
        if isinstance(astId, list):
            for i in astId:
                startDL(i, astVer, args, getAll)
        else:
            raise TypeError('Incorrect format for bulk downloading. Should be layed out as [id1,id2,id3,etc..]')   
    elif dlm == 'range':
        if isinstance(astId, list) and len(astId) == 2:
            for i in range(astId[0], astId[1]+1):
                startDL(i, astVer, args, getAll)
        else:
            raise TypeError('Incorrect format for range downloading. Should be laid out as [minId, maxId]') 
    elif dlm == 'roulette':
        rlAmn = args.rltAmnt if args.rltAmnt is not None else 1  
        rlType = args.rltType
        for i in range(1,rlAmn+1):
            while True:
                canDl = True
                randomId = random.randint(1000, 5000000000)
                if rlType is not None:
                    if getMeta(randomId, 'AssetTypeId') != rlType:
                        canDl = False    
                if canDl:
                    if startDL(randomId, None, args) == 1:
                        break                
#argparse 
cmdParse = argparse.ArgumentParser(description='Download assets from ROBLOX.')
cmdParse.add_argument('downlmode', choices=['single', 'bulk', 'range', 'roulette'], help='mode for asset downloading', type=str)
cmdParse.add_argument('assetid', help='id(s) of asset', type=str)
cmdParse.add_argument('--dir', help='save assets into your own directory', type=str)
cmdParse.add_argument('--ver', help='version(s) of the asset(s)', type=str)
cmdParse.add_argument('--sdirs', help='save assets in their own directories', action='store_true')
cmdParse.add_argument('--allVer', help='Download all of the versions of an asset (slow)', action='store_true')
cmdParse.add_argument('--rltAmnt', help='How many times should the roulette download something?', type=int)
cmdParse.add_argument('--rltType', help='What specific asset type should the roulette look for?', type=int)
args = cmdParse.parse_args()
handleArgs(args)
