class CueComp():

	def __init__(self, ownerComp):
		self.ownerComp = ownerComp
		self.FPlayer = op.FPlayer
		self.FPlayerCueComp = True
		self.Timer = ownerComp.op('timer1')
		self.selExternalIndex = ownerComp.op('selExternalIndex')
		self.MasterIndex = ownerComp.op('masterIndex')

	def Start(self):
		if self.IsMasterIndexSource:
			self.Timer.par.start.pulse()
		pass

	def End(self):
		if self.IsMasterIndexSource:
			self.Timer.par.initialize.pulse()
		pass

	@property
	def Duration(self):
		return self.ownerComp.par.Duration.eval()

	@Duration.setter
	def Duration(self, value):
		self.ownerComp.par.Duration = value

	@property
	def IsMasterIndexSource(self):
		isMasterSync = self.FPlayer.NODE.Ismastersync
		return tdu.Dependency(isMasterSync).val

	@property
	def MasterIndexSource(self):
		return self.selExternalIndex.par.chop.eval()

	@MasterIndexSource.setter
	def MasterIndexSource(self, value):
		self.selExternalIndex.par.chop = value

	@property
	def NODE(self):
		return self.FPlayer.NODE

	@property
	def PreviewScale(self):
		previewNode = self.FPlayer.PREVIEW_NODE
		return (previewNode.Noderendersizeh / previewNode.Canvassizeh)	

	
