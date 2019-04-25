class FPlayerExt:
	"""
	FPlayerExt description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		self.Cross = ownerComp.op('cross')
		self.UI = ownerComp.op('ui')
		self.MasterComps = ownerComp.op('masterComps')
		self.MasterPlaylists = self.MasterComps.op('masterPlaylists')
		self.MasterPlaylist = self.MasterPlaylists.op('masterPlaylist0')
		self.MasterCue = self.MasterPlaylist.op('masterCue0')
		self.Output = ownerComp.op('output')

	@property
	def Playlists(self):
		return self.ownerComp.par.Playlists.eval()
	
	@Playlists.setter
	def Playlists(self, value):
		self.ownerComp.par.Playlists = value


	@property
	def CurrentPlaylist(self):
		#return self.ownerComp.fetch('CurrentPlaylist', self.ownerComp.op('playlist0'))
		return self.ownerComp.Playlists.CurrentPlaylist

	@CurrentPlaylist.setter
	def CurrentPlaylist(self, value):
		self.ownerComp.store('CurrentPlaylist', value)

	@property
	def CurrentCue(self):
		return self.CurrentPlaylist.CurrentCue

	@property
	def PreviousCue(self):
		return self.Cross.PrevComp

	@property
	def Startcueonselect(self):
		return self.ownerComp.par.Startcueonselect.eval()

	@Startcueonselect.setter
	def Startcueonselect(self, value):
		self.ownerComp.par.Startcueonselect = value


	@property
	def Updatecueuionselect(self):
		return self.ownerComp.par.Updatecueuionselect.eval()

	@Updatecueuionselect.setter
	def Updatecueuionselect(self, value):
		self.ownerComp.par.Updatecueuionselect = value

	@property
	def Usecuecrossdur(self):
		return self.ownerComp.par.Usecuecrossdur.eval()

	@Usecuecrossdur.setter
	def Usecuecrossdur(self, value):
		self.ownerComp.par.Usecuecrossdur = value

	@property
	def Audiorate(self):
		return self.ownerComp.par.Audiorate.eval()

	@property
	def Resw(self):
		return self.ownerComp.par.Resw.eval()

	@property
	def Resh(self):
		return self.ownerComp.par.Resh.eval()
	

