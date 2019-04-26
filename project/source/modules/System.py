import subprocess

class System:

	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		self.Config = ownerComp.op('config')
		self.Globals = self.Config.op('globals')
		self.CueGlobals = self.Globals.op('cueGlobals')
		self.Output = ownerComp.op('output')

		nameSplit = project.name.split('.')
		del nameSplit[-2]
		self.fileName = '.'.join(nameSplit)

	

	def SetInstanceConfig(self):

		if self.ownerComp.var('NODE'):
			self.NODE_INDEX = int(self.ownerComp.var('NODE'))
		else:
			self.NODE_INDEX = 0

		if self.ownerComp.var('SERVER'):		
			self.SERVER = int(self.ownerComp.var('SERVER'))
		else:
			self.SERVER = 0

		if self.ownerComp.var('GPU'):	
			self.GPU = max(0, int(self.ownerComp.var('GPU')))
		else:
			self.GPU = 0	 	


		self.NODE = self.NODES[self.NODE_INDEX]

		self.ConfigureSytem()


	def ConfigureSytem(self):

		if self.NODE.par.Ismaster.eval():

			if len(self.NODES) == 1:
				self.ownerComp.Controlmode = 0
			
			else:
				if self.NODE.par.Ispreviewrender.eval() or self.NODE.par.Outputvideo.eval():			
					self.ownerComp.Controlmode = 1
				else:
					self.ownerComp.Controlmode = 2

		else:
			self.ownerComp.Controlmode = 3


		self.ownerComp.Ismastersync = self.NODE.par.Ismastersync.eval()

	
	def OnStart(self):

		self.SetInstanceConfig()

		pass
	
	def OnSavePre(self):

		#print('Saving: Fusion.toe')

		pass

	def Quit(self, quitAllNodes=False, quitMaster=False, nodeIndex=-1):

		if self.NODE == self.MASTER and quitMaster:
			project.quit(force=True)
		
		if self.NODE != self.MASTER and quitAllNodes:
			project.quit(force=True)

		elif nodeIndex > 0:

			quitNode = self.NODES[nodeIndex]
			if quitNode == self.NODE:
				project.quit(force=True)

	def Enablenodepreview(self, *args):

		state = bool(args[0])
		isPreviewRender = self.ownerComp.NODE.Ispreviewrender

		if self.ownerComp.NODE.Ismaster:

			self.Output.op('syphonspoutin1').bypass = not isPreviewRender and not state




	# Node Start/Stop Functions
	########################################################################
	def LoadLocal(self, projectName, node = 0, server = 0, gpu = -1, monitor=0):

		#if not (op.DATABASE.fetch('PREVIEW_NODE') == 'master' and node == 'node0'):

			binFolder = app.binFolder
			binFolder = re.sub('[/]', '\\\\', binFolder)

			projectFolder = project.folder
			projectFolder = re.sub('[/]', '\\\\', projectFolder)
			#projectFolder = '"' + projectFolder + '"'

			projectPath = '"' + projectFolder + '\\' + projectName + '"'
			
			exeName = 'touchdesigner099.exe'

			if gpu != -1:
				arg0 = ' -gpuformonitor ' + str(monitor) + ' '
				launchCommand = exeName + arg0
			else:
				launchCommand = exeName + ' '

			pOpenCommand = launchCommand + projectPath

			envV = mod.os.environ
			envV["NODE"] = str(node)
			envV["SERVER"] = str(server)
			envV["GPU"] = str(gpu)

			p = subprocess.Popen(pOpenCommand, cwd = binFolder, env=envV)

			print(	'Launching:\t', 'NODE' + str(node), '\n\t\t\t', 
					'Server', self.ownerComp.NODE.Address, '\n\t\t\t', 
					'GPU', gpu, '\n\t\t\t', 'File ', projectPath)

		#print(p.pid)

	def StopLocal(self, pid):
		
		try:
			mod.os.kill(pid, 0)
		except:
			pass

	def rawStr(self, string):
		rStr = "%r"%string
		return rStr[1:-1]

	def LoadRemote(self, client, userName, password, projectName, 
					node = 0, server =0, gpu =-1, monitor=0):

		masterIP = self.NODE.par.Address.eval()

		binFolder = app.binFolder
		binFolder = re.sub('[/]', '\\\\', binFolder)

		projectDir = project.folder
		projectDir = re.sub('[/]', '\\\\', projectDir)
		lmDir = projectDir.replace('\\project', '\\assets')
		projectFolder = projectDir.replace(':', '') 
		projectFolder = '"\\\\' + masterIP + '\\' + projectFolder 
		projectPath = projectFolder + '\\' + projectName
			
		exeName = 'touchdesigner099.exe'
		if gpu != -1:
			arg0 = ' -gpuformonitor ' + str(monitor) + ' '
			launchCommand = exeName + '" ' + arg0
		else:
			launchCommand = exeName + '" '
		
		launchCommand = '"'+ binFolder + '\\' + launchCommand + projectPath + '"'

		psCommand = ('cmd /c set SERVER='+ str(server) +'& set GPU='+ str(gpu) + 
					'& set NODE='+ str(node) +'& ' + launchCommand)

		dirExe = self.rawStr(projectDir + '\externalTools\PSTools\PsExec.exe -d -i \\')
		rDir = self.rawStr(projectDir + '\externalTools\PSTools')
		UserName = self.rawStr(userName)
		pOpenCommand = dirExe + client +' -u '+ UserName +' -p '+ password +' '+ psCommand
		
		run("mod.subprocess.Popen(args[0], cwd = args[1])", 
			pOpenCommand, rDir, delayFrames = 15 * node)

		print('Launching:\t', 'NODE' + str(node), '\n\t\t\t', 'Server', client, '\n\t\t\t', 
			'GPU', gpu, '\n\t\t\t', 'File ', projectPath)#,
		#'\n\t\t\t', 'pOpenCommand ', pOpenCommand,
		#'\n\t\t\t', 'Launch Command ', launchCommand)

	def KillRemoteNode(self, node):

		client = node.Address
		username = node.Username
		password = node.Password
		processName = 'TouchDesigner099.exe'

		projectDir = project.folder
		projectDir = re.sub('[/]', '\\\\', projectDir)

		dirExe = self.rawStr(projectDir + '\externalTools\PSTools\PsKill.exe -t \\')
		rDir = self.rawStr(projectDir + '\externalTools\PSTools')
		username = self.rawStr(username)
		pOpenCommand = dirExe + client +' -u '+ username +' -p '+ password +' '+ processName
		
		run("mod.subprocess.Popen(args[0], cwd = args[1])", 
			pOpenCommand, rDir, delayFrames = 15 * node.Index)



	def KillRemoteNodes(self):

		self.Config.op('killAllRemoteNodes').run()


	def StopRemote(self, client, userName, password, pid):

		command = (r'C:\PSTools\pskill.exe \\'+ client +' -u '+ userName +
					' -p '+ password + ' ' + str(pid))

		mod.subprocess.Popen(command, cwd = r"C:\PSTools")

	def LoadNode(self, node):

		if node.Address == self.MASTER.Address or node.Address == 'localhost':
			self.LoadLocal(self.fileName, node.Index, node.Server, node.Gpu)

		else:

			#print(node.Address, node.Username, node.Password, 
			#				self.fileName, node.Index, 
			#				node.Server, node.Gpu, node.Monitor)

			self.LoadRemote(node.Address, node.Username, node.Password, 
							self.fileName, node.Index, 
							node.Server, node.Gpu, node.Monitor)	

	def Loadallnodes(self, *args):

		self.Config.op('loadAllNodes').run()

		
		# not working, no delay need to call script above
		'''
		for i, node in enumerate(self.NODES[1:]):
			delay = i * 60	
			run("args[0].LoadNode(args[1])", self.ownerComp, node,
			delayFrames = delay, fromOP=self.ownerComp)	

			#self.LoadNode(node)'''

		pass

	def Quitallnodes(self, *args):

		self.ownerComp.GetAttr('Quit', quitAllNodes=True)

		pass

	def Killallremotenodes(self, *args):


		self.KillRemoteNodes()

	def Loadnode(self, *args):

		selectNodeIndex = self.ownerComp.par.Selectnode.menuIndex + 1
		node = self.NODES[selectNodeIndex]

		self.LoadNode(node)


	def Quitnode(self, *args):

		selectNodeIndex = self.ownerComp.par.Selectnode.menuIndex + 1
		self.ownerComp.GetAttr('Quit', nodeIndex=selectNodeIndex)

		pass

	
	@property
	def MASTER(self):
		return self.NODES[0]

	@property
	def NODES(self):
		return self.Config.GetNodes()

	@property
	def NODE_INDEX(self):
		return self.ownerComp.fetch('NODE_INDEX', 0)
	
	@NODE_INDEX.setter
	def NODE_INDEX(self, value):
		self.ownerComp.store('NODE_INDEX', int(value))

	@property
	def NODE(self):
		return self.ownerComp.fetch('NODE', self.NODES[self.NODE_INDEX])
	
	@NODE.setter
	def NODE(self, value):
		self.ownerComp.store('NODE', value)

	@property
	def SERVER(self):
		return self.ownerComp.fetch('SERVER', 0)
	
	@SERVER.setter
	def SERVER(self, value):
		self.ownerComp.store('SERVER', int(value))	

	@property
	def GPU(self):
		return self.ownerComp.fetch('GPU', 0)
	
	@GPU.setter
	def GPU(self, value):
		self.ownerComp.store('GPU', int(value))
