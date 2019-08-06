class CueProperties():

	def __init__(self, ownerComp):
		# The component to which this extension is attached

		self.ownerComp = ownerComp
		self.playlist = ownerComp.parent()
		self.FPlayer = ownerComp.parent(2).par.Fplayer.eval()

		self.Texture = ownerComp.op('textureOut')			
		self.Audio = ownerComp.op('audioOut')

		self.MovFileIn = ownerComp.op('moviefilein')
		self.AudioFileIn = ownerComp.op('audiofilein')
		self.setMovFile = ownerComp.op('setMovFile')

		self.selSync = ownerComp.op('selSync')
		self.index = ownerComp.op('index')

		self.switchTexSource = ownerComp.op('switchTexSource')
		self.switchAudioSource = ownerComp.op('switchAudioSource')
		self.selectTop = ownerComp.op('selectTop')
		self.selectAudioChop = ownerComp.op('selectAudioChop')
		self.selCompIndex = ownerComp.op('selCompIndex')

	# Non Comp Par Properties
	###############################################################
	@property
	def FPlayerCueCompLoaded(self):
		return self.ownerComp.fetch('FPlayerCueCompLoaded', False)

	@FPlayerCueCompLoaded.setter
	def FPlayerCueCompLoaded(self, value):
		self.ownerComp.store('FPlayerCueCompLoaded', value)

	@property
	def MovFileCuePoint(self):
		return self.MovFileIn.par.cuepoint.eval()

	@MovFileCuePoint.setter
	def MovFileCuePoint(self, value):
		self.MovFileIn.par.cuepoint = value

	@property
	def MovFileCue(self):
		return self.MovFileIn.par.cue.eval()

	@MovFileCue.setter
	def MovFileCue(self, value):
		self.MovFileIn.par.cue = value

	@property
	def MovFilePostfix(self):
		if self.Nodepostfixactive:
			postfix = self.FPlayer.NODE.Movfilepostfix
			#print(postfix)
			movFile = self.Movfile.replace('PREVIEW_1', postfix)
			return movFile
		else:
			return self.Movfile


	
