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

	# None Par Properties
	###############################################################
	@property
	def FPlayerCueCompLoaded(self):
		return self.ownerComp.fetch('FPlayerCueCompLoaded', False)

	@FPlayerCueCompLoaded.setter
	def FPlayerCueCompLoaded(self, value):
		self.ownerComp.store('FPlayerCueCompLoaded', value)

	@property
	def Movfile(self):
		return self.ownerComp.par.Movfile.eval()

	@Movfile.setter
	def Movfile(self, value):
		self.ownerComp.par.Movfile = value

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


	# Par Properties
	###############################################################

	@property
	def Label(self):
		return self.ownerComp.par.Label.eval()

	@Label.setter
	def Label(self, value):
		self.ownerComp.par.Label = value
		self.playlist.SetPlaylist()

	@property
	def Playindex(self):
		return self.ownerComp.par.Playindex.eval()

	@Playindex.setter
	def Playindex(self, value):
		self.ownerComp.par.Playindex = value
		self.playlist.SetPlaylist()

	@property
	def MovFilePostfix(self):

		if self.Nodepostfixactive:
			postfix = self.FPlayer.NODE.Movfilepostfix
			print(postfix)
			movFile = self.Movfile.replace('PREVIEW_1', postfix)

			if self.FPlayer.NODE.digits > 6:
				movFile = movFile.replace('wall', 'floor' )
			return movFile
		else:
			return self.Movfile

	@property
	def Nodepostfixactive(self):
		return self.ownerComp.par.Nodepostfixactive.eval()

	@Nodepostfixactive.setter
	def Nodepostfixactive(self, value):
		self.ownerComp.par.Nodepostfixactive = value

	@property
	def Comp(self):
		return self.ownerComp.par.Comp.eval()

	@Comp.setter
	def Comp(self, value):

		self.ownerComp.par.Comp = value

		if hasattr(value, 'FPlayerCueComp'):
			self.FPlayerCueCompLoaded = True
			self.selCompIndex.par.chop = self.Comp.MasterIndex

	@property
	def Top(self):
		return self.ownerComp.par.Top.eval()

	@Top.setter
	def Top(self, value):
		self.selectTop.par.top = value
		self.selectTop.cook(force=True)
		self.ownerComp.par.Top = value

	@property
	def Audiochop(self):
		return self.ownerComp.par.Audiochop.eval()

	@Audiochop.setter
	def Audiochop(self, value):
		self.selectAudioChop.par.chop = value
		self.selectAudioChop.cook(force=True)
		self.ownerComp.par.Audiochop = value

	@property
	def Texsource(self):
		return self.ownerComp.par.Texsource.eval()

	@Texsource.setter
	def Texsource(self, value):
		self.ownerComp.par.Texsource = value

	@property
	def Audiosource(self):
		return self.ownerComp.par.Audiosource.eval()

	@Audiosource.setter
	def Audiosource(self, value):
		self.ownerComp.par.Audiosource = value

	@property
	def Duration(self):
		return self.ownerComp.par.Duration.eval()

	@Duration.setter
	def Duration(self, value):
		self.ownerComp.par.Duration = value

	@property
	def Crossduration(self):
		return self.ownerComp.par.Crossduration.eval()

	@Crossduration.setter
	def Crossduration(self, value):
		self.ownerComp.par.Crossduration = value

	@property
	def Movplay(self):
		return self.ownerComp.par.Movplay.eval()

	@Movplay.setter
	def Movplay(self, value):
		self.ownerComp.par.Movplay = value

	@property
	def Movcuepoint(self):
		return self.ownerComp.par.Movcuepoint.eval()

	@Movcuepoint.setter
	def Movcuepoint(self, value):
		self.ownerComp.par.Movcuepoint = value

	@property
	def Movspeed(self):
		return self.ownerComp.par.Movspeed.eval()

	@Movspeed.setter
	def Movspeed(self, value):
		self.ownerComp.par.Movspeed = value

	@property
	def Movtrim(self):
		return self.ownerComp.par.Movtrim.eval()

	@Movtrim.setter
	def Movtrim(self, value):
		self.ownerComp.par.Movtrim = value

	@property
	def Movtrimstartend1(self):
		return self.ownerComp.par.Movtrimstartend1.eval()

	@Movtrimstartend1.setter
	def Movtrimstartend1(self, value):
		self.ownerComp.par.Movtrimstartend1 = value

	@property
	def Movtrimstartend2(self):
		return self.ownerComp.par.Movtrimstartend2.eval()

	@Movtrimstartend2.setter
	def Movtrimstartend2(self, value):
		self.ownerComp.par.Movtrimstartend2 = value

	@property
	def Movextend(self):
		return self.ownerComp.par.Movextend.eval()

	@Movextend.setter
	def Movextend(self, value):
		self.ownerComp.par.Movextend = value

	@property
	def Movfilelength(self):
		return self.ownerComp.par.Movfilelength.eval()

	@Movfilelength.setter
	def Movfilelength(self, value):
		self.ownerComp.par.Movfilelength = value

	@property
	def Audiofile(self):
		return self.ownerComp.par.Audiofile.eval()

	@Audiofile.setter
	def Audiofile(self, value):
		self.ownerComp.par.Audiofile = value

	@property
	def Audioplay(self):
		return self.ownerComp.par.Audioplay.eval()

	@Audioplay.setter
	def Audioplay(self, value):
		self.ownerComp.par.Audioplay = value

	@property
	def Audiocuepoint(self):
		return self.ownerComp.par.Audiocuepoint.eval()

	@Audiocuepoint.setter
	def Audiocuepoint(self, value):
		self.ownerComp.par.Audiocuepoint = value

	@property
	def Levelshue(self):
		return self.ownerComp.par.Levelshue.eval()

	@Levelshue.setter
	def Levelshue(self, value):
		self.ownerComp.par.Levelshue = value

	@property
	def Levelssaturation(self):
		return self.ownerComp.par.Levelssaturation.eval()

	@Levelssaturation.setter
	def Levelssaturation(self, value):
		self.ownerComp.par.Levelssaturation = value

	@property
	def Levelsbrightness(self):
		return self.ownerComp.par.Levelsbrightness.eval()

	@Levelsbrightness.setter
	def Levelsbrightness(self, value):
		self.ownerComp.par.Levelsbrightness = value

	@property
	def Levelsgamma(self):
		return self.ownerComp.par.Levelsgamma.eval()

	@Levelsgamma.setter
	def Levelsgamma(self, value):
		self.ownerComp.par.Levelsgamma = value

	@property
	def Levelscontrast(self):
		return self.ownerComp.par.Levelscontrast.eval()

	@Levelscontrast.setter
	def Levelscontrast(self, value):
		self.ownerComp.par.Levelscontrast = value

