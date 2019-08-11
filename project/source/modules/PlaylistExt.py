import os
import re

class PlaylistExt:
	"""
	PlaylistExt description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		self.playlists = ownerComp.parent()
		self.FPlayer = self.playlists.par.Fplayer.eval()
		self.playlistsComp = ownerComp.parent()

		fileTypes = tdu.fileTypes['movie'] + tdu.fileTypes['image']
		fileTypes = ['.' + fileType for fileType in fileTypes]
		self.fileExtensions = fileTypes
		
		self.SetPlaylist()

	def Setup(self, label, duration):

		self.Label = label

	def CueSelect(self, cue):
		self.CurrentCue = cue

	def CueCreate(	self, label=None, top=None, comp=None, audioChop=None, 
					movFile=None, duration=10, insert=-1):
		cueID = self.MaxCueIndex + 1
		name = 'cue' + str(cueID)

		self.CurrentCue = self.ownerComp.copy(self.FPlayer.MasterCue)
		self.CurrentCue.nodeX = 0
		self.CurrentCue.nodeY = cueID * -200
		self.CurrentCue.name = name

		if not label:
			if comp:
				if 'CUE_COMP' in comp.tags:
					if comp.par.Label.eval() != '':
						label = comp.par.Label.eval()
					else:
						label = comp.name
				else:
					label = comp.name
			elif top:
				label = top.name
			else:
				label = name

		self.CurrentCue.Setup(	cueID, label=label, top=top, comp=comp,
								audioChop=audioChop, duration=duration,
								movFile=movFile, insert=-1)

		self.SetPlaylist()

	def CueDelete(self, cue, remoteDelete=False):
		if self.FPlayer.NODE.Ismaster:
			message = 'Are you sure you want to Delete: ' + cue.Label
			confirm = ui.messageBox('Delete Cue', 
				message, buttons=['Cancel', 'Delete Cue'])			
			if confirm == 1:
				cue.destroy()
				self.FPlayer.Remote.GetAttr(self.ownerComp, 
				'CueDelete', cue, remoteDelete=True)
				self.SetPlaylist()
		elif remoteDelete:
			cue.destroy()
			self.SetPlaylist()	

	def Initialize(self):
		if self.FPlayer.NODE.Ismaster:
			lister = self.FPlayer.UI_Playlist.op('playlist/list/lister')
			if len(lister.SelectedRows) > 0:
				lister.DeselectRow(lister.SelectedRows[0])

		cue = self.Playlist[0][1]	
		self.FPlayer.GetAttr('CueSelect', cue)
		if not self.FPlayer.Startcueonselect:
			self.FPlayer.GetAttr('CueStart')

	def LoadDirectory(self, directory, insert=-1):	
		filePaths = []
		for (root, dir, files) in os.walk(directory):
			for file in files:
				filePaths.append(os.path.join(root, file))

		for filePath in filePaths:	
			self.LoadFile(filePath, insert)
			if insert != -1:
				insert += 1

	def LoadFile(self, filePath, insert=-1):
		fileExt = os.path.splitext(filePath)[1]
		if fileExt in self.fileExtensions:
			self.CueCreate(movFile=filePath)
	
	def ParseDropString(self, string, insert):		
		#if os.path.isfile(string):
			#self.LoadFile(string, insert)
		# need better method for multi-node
		if os.path.isdir(string):
			self.LoadDirectory(string, insert)
		else:
			self.LoadFile(string, insert)
		run("args[0].cook(force=True, recurse=True)",
			self.ownerComp, delayFrames=30)

	def LoadOP(self, operator, comp=None, insert=-1):	
		self.CueCreate(top=operator, comp=comp, insert=insert)

	def LoadCOMP(self, comp, insert=-1):
		outTops = comp.findChildren(type=outTOP)
		if len(outTops) > 0:

			outTops.sort(key=lambda x: x.digits)
			self.LoadOP(outTops[0], comp=comp, insert=insert)

	def Reorder(self, cuesIndices):
		mod.pprint.pprint(cuesIndices)
		for cuesIndex in cuesIndices:
			cue = cuesIndex[0]
			index = cuesIndex[1]
			cue.Playindex = index + 1

	def SetPlaylist(self):
		cueComps = self.ownerComp.findChildren(tags=['CUE'])
		playlist = []
		for cueComp in cueComps:
			playlist.append([cueComp.Label, cueComp])

		playlist.sort(key=lambda x: x[1].Playindex)	
		self.Playlist = playlist			

	def Createnewcue(self, *args):
		label = 'Empty Cue'
		self.CueCreate(label=label)

	def DeleteAllCues(self):
	
		cues = self.ownerComp.findChildren(tags=['CUE'])
		for cue in cues:
			if cue.Playindex != 0:
				cue.destroy()	

		self.SetPlaylist()

	def Deleteallcues(self, *args):
		self.DeleteAllCues()

	@property
	def Label(self):
		return self.ownerComp.par.Label.eval()

	@Label.setter
	def Label(self, value):
		self.ownerComp.par.Label = value
		self.playlistsComp.SetPlaylists()

	@property
	def Playlistindex(self):
		return self.ownerComp.par.Playlistindex.eval()

	@Playlistindex.setter
	def Playlistindex(self, value):
		self.ownerComp.par.Playlistindex = value
		self.playlistsComp.SetPlaylists()

	@property
	def Playlist(self):
		return self.ownerComp.fetch('Playlist', tdu.Dependency([])).val

	@Playlist.setter
	def Playlist(self, value):
		self.ownerComp.store('Playlist', tdu.Dependency(value))

	@property
	def MaxCueIndex(self):
		i = 0
		for cue in self.Playlist:
			i = max(cue[1].digits, i)

		return i

	@property
	def NumCues(self):
		return len(self.Playlist)

	@property
	def CurrentCue(self):
		return self.ownerComp.fetch('CurrentCue', None)

	@CurrentCue.setter
	def CurrentCue(self, value):
		self.ownerComp.store('CurrentCue', value)