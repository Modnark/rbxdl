Metalhead's ROBLOX asset downloader

#Arguments
	Required:
		Download Mode [downl, bulk, range, roulette]
		Asset ID
	optional:
		-cdir 
		-ver
		-spd
		-smt
		-tvr
	(can be used together)
#Usage

	Basic:
		Download a single asset from ROBLOX
		#Example:
			py rbxdl.py downl YOURID
		this will download the asset to a folder named downloads and it will be inside 
		a folder named by what type of asset it is
		if you download a model it would be:
			downloads\model\YOURID.rbxm
	
	cdir arg:
		If you wish to use a directory besides \downloads\ you can with -cdir
		#Example:
			py rbxdl.py downl YOURID -cdir "Nice Name"
		this will download the asset just as it does normally except it will be
		in the \Nice Name\ directory

	ver arg:
		If you wish to get a specific version of an asset you may with -ver
		#Example:
			py rbxdl.py downl YOURID -ver 4
		this would download the 4th version of the asset ID you enter so long it exists
		otherwise you will get a 404 error

	spd arg:	
		If you want to seperate each asset into its own folder use -spd
		#Example:
			py rbxdl.py downl YOURID -spd
		doing this would give you something similar to the following:
			\downloads\Model\YOURID\YOURID.xml 
		(note that \downloads\ and \Model\ may be different depending on your arguments)
	
	smt arg:
		This argument will enable the saving of metadata of an asset
		The metadata includes the following:
			AssetID
			AssetTypeId
			CreatorId
			CreatorName
			etc.
		this will be saved with the asset file
	
	tvr arg:
		[WARNING] This is very unstable 
		attempts to download up to 10 versions of an asset
		use the -ver arg to specify the max attempts to try
		#Example:
			py rbxdl.py downl YOURID -tvr -ver 10
#Download Modes
	
	downl:
		downloads single asset
		#Example:
			 py rbxdl.py downl YOURID
	
	bulk:
		downloads assets within brackets (no spaces)
		#Example:
			py rbxdl.py downl [YOURID1,YOURID2,YOURID3,YOURID4] 	
		you can have as many as you want within the brackets
	
	range:
		downloads assets from a minimum and maximum ID
		#Example:
			py rbxdl.py downl [MINID, MAXID]
	roulette:
		tries downloading a random asset
		#Example:
			py rbxdl.py roulette 10 
		(id here will instead be the amount of times it loops around)		