class FPlayerUIExt:

	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		self.fPlayer = ownerComp.parent.FPlayer

		self.UI_Playlists = ownerComp.op('playlists')
		self.UI_Playlist =  ownerComp.op('playlist')
		self.UI_Cue = ownerComp.op('cue')

	def CueLoad(self, cue):

		pass



