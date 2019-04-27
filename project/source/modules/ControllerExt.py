System = iop.Modules.op('System').module.System

class ControllerExt(System):
	"""
	ControllerExt description
	"""
	def __init__(self, ownerComp):
		
		System.__init__(self, ownerComp)

		self.ownerComp = ownerComp
		self.Remote = ownerComp.op('remote')
		self.sync = self.Remote.op('sync')
		self.Sync = self.sync.op('sync')
		self.Cross = ownerComp.op('cross')
		self.UI = ownerComp.op('ui')
		self.UI_Playlists = self.UI.op('playlists')
		self.UI_Playlist =  self.UI.op('playlist')
		self.UI_Cue = self.UI.op('cue')

		controlModeLookup = {'LOCAL': 0, 'LOCAL_CONTROL_EXTERNAL': 1, 
							'CONTROL_EXTERNAL': 2, 'EXTERNAL': 3, 'BACKUP_UI': 4}


		self.SetCtrlInternalExternal()

	# Cue Functions
	########################################################################
	def CueParChange(self, cue, par):
		
		#if cue == self.ownerComp.CurrentCue:
		#	self.UI.CueLoad(cue)

		#cue.parent().SetPlaylist()

		pass


	def CueSelect(self, cue):
		#print('CueSelect')
		if cue:
			self.UI.CueLoad(cue)	
			self.ownerComp.CurrentPlaylist.CueSelect(cue)
			
			if self.ownerComp.Startcueonselect and self.MasterCtrl:	
				#debug('Start on Cue Select')
				run("args[0].GetAttr('CueStart')", self.ownerComp, delayFrames=6)
			
			elif self.ownerComp.Startcueonselect and self.NODE.Ispreviewrender:
				run("args[0].CueStart()", self.ownerComp, delayFrames=6)
				pass

	def CueStart(self):

		if self.Ismastersync:

			self.sync.par.Cuestart.pulse()
			pass

	def CueStartSync(self):

		cue = self.ownerComp.CurrentCue
		cue.Start()	

		if self.ownerComp.Usecuecrossdur:
			self.Cross.Crossduration = cue.Crossduration

		if self.MasterCtrl:
			self.Cross.CrossFade(cue)
		elif self.RemoteCtrl:
			self.Cross.CrossFadeRemote(cue)




	def CueSetLabel(self, cue, label):

		cue.Label = label
		self.UI_Cue.Load(cue)


	# Playlist Functions
	########################################################################	
	def PlaylistReorder(self, cuesIndices):

		self.ownerComp.CurrentPlaylist.Reorder(cuesIndices)

	def PlaylistOnDrop(self, dropData):
		#print('Playlist On Drop:', dropData)
		dragItems = dropData['dragItems']
		row = dropData['row']

		insert = -1

		if row != -1:
			insert = row - 1

		for item in dropData['dragItems']:

			if type(item) == str:
				self.ownerComp.CurrentPlaylist.ParseDropString(item, insert)	
			
			elif item.isTOP:
				self.ownerComp.CurrentPlaylist.LoadOP(item, insert=insert)

			elif item.isCOMP:

				if type(item) == listCOMP:

					row = dropData['fromListerInfo'][0]
					obj = item.Data[row]['rowObject']
					item = obj[1]
				
				self.ownerComp.CurrentPlaylist.LoadCOMP(item, insert)

			if row != -1:
				insert += 1

	def CueDelete(self, cue):

		if cue:
			self.ownerComp.CurrentPlaylist.CueDelete(cue)

	def CueCreate(self):
		label = 'Empty Cue'
		self.ownerComp.CurrentPlaylist.CueCreate(label=label)


	# Playlists Functions
	########################################################################

	def PlaylistSelect(self, playlist):

		self.ownerComp.Playlists.CurrentPlaylist = playlist
		self.CueSelect(self.ownerComp.Playlists.CurrentPlaylist.CurrentCue)
		

	def PlaylistStart(self):

		pass


	def PlaylistSetLabel(self, playlist, label):

		playlist.Label = label

	def PlaylistDelete(self, playlist):

		if playlist:
			self.ownerComp.Playlists.PlaylistDelete(playlist)	

	def PlaylistCreate(self):
		
		self.ownerComp.Playlists.PlaylistCreate()



	# Sync 
	########################################################################

	def SetSyncSelects(self):
			#debug('SetSyncSelects')
			top1 = self.Cross.Select1.par.top.eval()

			if top1:
				comp1 = top1.parent()
			else:
				comp1 = self.ownerComp.MasterCue

			top2 = self.Cross.Select2.par.top.eval()

			if top2:
				comp2 = top2.parent()
			else:
				comp2 = self.ownerComp.MasterCue

			self.sync.SetCrossComps(comp1, comp2)

	def SetCtrlInternalExternal(self):

		self.MasterCtrl = tdu.Dependency(self.Controlmode in ['LOCAL', 
															'LOCAL_CONTROL_EXTERNAL', 
															'CONTROL_EXTERNAL'])
		self.CtrlInt = tdu.Dependency(self.Controlmode in ['LOCAL', 'LOCAL_CONTROL_EXTERNAL'])
		self.CtrlExt = tdu.Dependency(self.Controlmode in ['LOCAL_CONTROL_EXTERNAL', 
											'CONTROL_EXTERNAL', 'BACKUP_UI'])
		self.RemoteUI = tdu.Dependency(self.Controlmode in ['BACKUP_UI'])
		self.RemoteCtrl = tdu.Dependency(self.Controlmode == 'EXTERNAL')


	# System Functions
	########################################################################

	# located in inherited System module/class


	# System Wrapper Functions
	########################################################################

	def GetAttr(self, attribute, *args, **kwargs):
		'''
		if self.CtrlInt:

			getattr(self.ownerComp, attribute)(*args, **kwargs)

		if self.CtrlExt:
			#print('GetAttr Ext:', attribute)
			self.Remote.GetAttr(self.ownerComp, attribute, *args, **kwargs)'''

		getattr(self.ownerComp, attribute)(*args, **kwargs)
		self.Remote.GetAttr(self.ownerComp, attribute, *args, **kwargs)

	def SetAttr(self, comp, attribute, value):
		'''
		if self.CtrlInt:

			setattr(comp, attribute, value)

		if self.CtrlExt:

			self.Remote.SetAttr(comp, attribute, value)'''

		setattr(comp, attribute, value)
		self.Remote.SetAttr(comp, attribute, value)




	@property
	def Controlmode(self):
		return self.ownerComp.par.Controlmode.eval()

	@Controlmode.setter
	def Controlmode(self, value):
		self.ownerComp.par.Controlmode = value
		self.SetCtrlInternalExternal()
		self.Remote.SetMode(value)

	@property
	def Ismastersync(self):
		return self.ownerComp.par.Ismastersync.eval()

	@Ismastersync.setter
	def Ismastersync(self, value):
		self.ownerComp.par.Ismastersync = value
		self.SetCtrlInternalExternal()
		self.Remote.SetMode(self.ownerComp.par.Controlmode.eval())

	




	

