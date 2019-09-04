parprops = iop.Modules.op('parproperties').module
CueProperties = iop.Modules.op('cueproperties').module.CueProperties

class CueExt(CueProperties):
	"""
	CueExt description
	"""
	def __init__(self, ownerComp):
		self.ownerComp = ownerComp
		parprops.parProperties(self, parCallbacksDAT=ownerComp.op('parCallbacks'))
		CueProperties.__init__(self, ownerComp)

		self.node = parent.FPlayer.NODE
		self.isPreview = self.node.Ispreviewrender

		# set par property post setters
		self.ParpGrp.Label.fPostSet = self.LabelPostSetter
		self.ParpGrp.Playindex.fPostSet = self.PlayindexPostSetter
		self.ParpGrp.Comp.fPostSet = self.CompPostSetter
		self.ParpGrp.Top.fPostSet = self.TopPostSetter
		self.ParpGrp.Audiochop.fPostSet = self.AudiochopPostSetter

		# you can define getters and setters (pre set) as well
		# technically your appending/prepending the getter and setter functions
		# which are already getting/setting the par value
		#self.ParpGrp.Someparname.fGet = self.Somefunction
		#self.ParpGrp.Someparname.fSet = self.SomeOtherFunction

	def ParChange(self, par):
		#self.FPlayer.CueParChange(self.ownerComp, par)
		self.FPlayer.Remote.SetAttr(par.owner, par.name, par.eval())
		self.playlist.SetPlaylist()

	def Start(self):
		if self.Texsource == 'FILE':
			if self.MovFileCue:
				self.MovFileCue = False
			else:
				self.MovFileIn.par.cuepulse.pulse()

		if self.Comp and self.FPlayerCueCompLoaded:
			if self.FPlayer.RemoteCtrl:
				self.Comp.MasterIndexSource = self.index

			self.Comp.Start()

		if self.Audiosource == 'AUDIO_FILE' and self.node.Outputaudio:
			if self.AudioFileCue:
				self.AudioFileCue = False
			else:
				self.AudioFileIn.par.cuepulse.pulse()

	def End(self):
		if self.Texsource == 'FILE':			
			self.MovFileCue = True

		if self.Comp and self.FPlayerCueCompLoaded:
			self.Comp.End()

		if self.Audiosource == 'AUDIO_FILE' and self.node.Outputaudio:
			self.AudioFileCue = True

	def Pulse(self):	
		if self.Texsource == 'FILE':
			self.MovFileIn.par.cuepulse.pulse()	

	def Setup(	self, cueID, label=None, 
				top=None, comp=None, audioChop=None, 
				movFile=None, duration=10, insert=-1):

		if top:
			self.Texsource = 'TOP'
			self.Top = top
			self.Comp = comp
			self.Audiochop = audioChop
			self.Duration = duration
			self.Label = label

		elif movFile:
			#print(movFile)
			self.Texsource = 'FILE'
			self.Movfile = movFile
			self.MovFileIn.preload(0)

			run("args[0].SetDurFromMovFile()", self.ownerComp,
				delayFrames=10)

			movName = movFile.split('/')[-1:][0]
			movName = movName.split('.')[:1][0]
			movName = movName.replace('__PREVIEW_1', '')

			self.Label = movName

		else:
			self.Label = label

		self.Playindex = cueID
		self.selSync.par.channames = self.index.path[1:]
		self.ownerComp.cook(force=True, recurse=True)


	def Preload(self):
		self.MovFileIn.preload(self.MovFileCuePoint)

	def SetDurFromMovFile(self):
		if self.MovFileIn.numImages > 1:
			self.Duration = self.MovFileIn.numSeconds

	def LabelPostSetter(self, value):
		self.playlist.SetPlaylist()
			
	def PlayindexPostSetter(self, value):
		self.playlist.SetPlaylist()
		
	def CompPostSetter(self, value):
		if hasattr(value, 'FPlayerCueComp'):
			self.FPlayerCueCompLoaded = True
			self.selCompIndex.par.chop = self.Comp.MasterIndex	
			
	def TopPostSetter(self, value):
		self.selectTop.cook(force=True)
		self.ownerComp.par.Top = value
		
	def AudiochopPostSetter(self, value):
		self.selectAudioChop.cook(force=True)
		self.ownerComp.par.Audiochop = value	

