CueProperties = op('CueProperties').module.CueProperties

class CueExt(CueProperties):
	"""
	CueExt description
	"""
	def __init__(self, ownerComp):
		CueProperties.__init__(self, ownerComp)
		self.ownerComp = ownerComp
		self.node = parent.FPlayer.NODE
		self.isPreview = self.node.Ispreviewrender
		
	def ParChange(self, par):
		#self.FPlayer.CueParChange(self.ownerComp, par)
		self.FPlayer.SetAttr(par.owner, par.name, par.eval())
		self.playlist.SetPlaylist()

	def Start(self):
		if self.Texsource == 'FILE':
			if self.MovFileCue:
				self.MovFileCue = False
			else:
				self.MovFileIn.par.cuepulse.pulse()

		if self.Comp and self.FPlayerCueCompLoaded:
			if self.FPlayer.RemoteCtrl:
				self.Comp.IsMasterIndexSource = False
				self.Comp.MasterIndexSource = self.index

			self.Comp.Start()

		if self.Audiosource == 'AUDIO_FILE' and self.isPreview:
			self.Audiochop.par.Cuepulse.pulse()

	def End(self):
		if self.Texsource == 'FILE':			
			self.MovFileCue = True

		if self.Comp and self.FPlayerCueCompLoaded:
			self.Comp.End()

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

	def Preload(self):
		self.MovFileIn.preload(self.MovFileCuePoint)

	def SetDurFromMovFile(self):
		if self.MovFileIn.numImages > 1:
			self.Duration = self.MovFileIn.numSeconds




