import os

class PlaylistsExt:

	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		self.SetPlaylists()

	def PlaylistSelect(self, playlist):
		self.CurrentPlaylist = playlist

	def PlaylistCreate(	self, label=None, duration=10):
		playlistID = self.NumPlaylists
		name = 'playlist' + str(playlistID + 1)

		self.CurrentPlaylist = self.ownerComp.copy(self.FPlayer.MasterPlaylist)
		self.CurrentPlaylist.nodeX = 0
		self.CurrentPlaylist.nodeY = playlistID * -200
		self.CurrentPlaylist.name = name

		if not label:

			label = name

		self.CurrentPlaylist.Setup(label, duration)

		self.SetPlaylists()

	def PlaylistDelete(self, playlist):
		if self.FPlayer.NODE.Ismaster:
			message = 'Are you sure you want to Delete: ' + playlist.Label
			confirm = ui.messageBox('Delete Playlist', message, buttons=['Cancel', 'Delete Playlist'])
			
			if confirm == 1:

				playlist.destroy()
				self.SetPlaylists()

		else:
			playlist.destroy()
			self.SetPlaylists()	
	

	def Reorder(self, indices):

		for index in indices:

			playlist = index[0]
			index = index[1]
			playlist.Playlistindex = index



	def SetPlaylists(self):

		playlistComps = self.ownerComp.findChildren(tags=['PLAYLIST'])

		playlists = []

		for playlistComp in playlistComps:

			playlists.append([playlistComp.Label, playlistComp])


		playlists.sort(key=lambda x: x[1].Playlistindex)	

		self.Playlists = playlists			


	def Createnewplaylist(self, *args):
		self.PlaylistCreate()


	def DeleteAllPlaylists(self):

		print('DeleteAllPlaylists')
	
		playlists = self.ownerComp.findChildren(tags=['PLAYLIST'])
		for playlist in playlists:
			playlist.destroy()	



		self.SetPlaylists()

	def Deleteallplaylists(self, *args):

		self.DeleteAllPlaylists()

	@property
	def FPlayer(self):
		return self.ownerComp.par.Fplayer.eval()

	@FPlayer.setter
	def FPlayer(self, value):
		self.ownerComp.par.Fplayer = value

	@property
	def Playlists(self):
		return self.ownerComp.fetch('Playlists', tdu.Dependency([])).val

	@Playlists.setter
	def Playlists(self, value):
		self.ownerComp.store('Playlists', tdu.Dependency(value))


	@property
	def NumPlaylists(self):
		return len(self.Playlists)


	@property
	def CurrentPlaylist(self):
		return self.ownerComp.fetch('CurrentPlaylist', None)

	@CurrentPlaylist.setter
	def CurrentPlaylist(self, value):
		self.ownerComp.store('CurrentPlaylist', value)