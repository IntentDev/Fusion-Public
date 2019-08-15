class SyncExt:

	def __init__(self, ownerComp):

		self.ownerComp = ownerComp
		self.fplayer = parent.FPlayer
		self.syncOut = ownerComp.op('syncout')
		self.syncIn = ownerComp.op('syncin')
		self.nullSyncIn = ownerComp.op('nullSyncIn')
		self.shdmemOut = ownerComp.op('sharedmemoutSync')
		self.shdmemIn = ownerComp.op('sharedmeminSync')
		self.touchOut = ownerComp.op('touchoutSync')
		self.touchIn = ownerComp.op('touchinSync')
		self.switchSync = ownerComp.op('switchSync')
		self.syncSources = ownerComp.op('syncSources')
		self.selCrossDataComp1 = self.syncSources.op('selCrossDataComp1')
		self.selCrossDataComp2 = self.syncSources.op('selCrossDataComp2')

		ownerComp.par.Cuestart = False

		self.syncAddress = '239.255.1.1'
		self.syncPort = 15000
		self.syncTimeout = 34

	def SyncOutActive(self, state):
		if self.Syncmode == 'SYNC_CHOP':
			if self.syncOut:
				self.syncOut.par.active = state
				self.syncOut.bypass = not state
			else:
				self.syncOut = self.ownerComp.create(syncoutCHOP, 'syncout')
				self.syncOut.par.multicastaddress = self.syncAddress
				self.syncOut.par.port = self.syncPort
				self.syncOut.par.timeout = self.syncTimeout
				self.syncSources.outputConnectors[0].connect(self.syncOut)
			
			self.shdmemOut.par.active = False
			self.touchOut.par.active = False

		elif self.Syncmode == 'SHARED_MEM':
			if self.syncOut:
				self.syncOut.par.active = False
				self.syncOut.bypass = True
				self.syncOut.destroy()
			self.shdmemOut.par.active = state
			self.touchOut.par.active = False

		elif self.Syncmode == 'TOUCH_IN_OUT':
			if self.syncOut:
				self.syncOut.par.active = False
				self.syncOut.bypass = True
				self.syncOut.destroy()
			self.shdmemOut.par.active = False
			self.touchOut.par.active = state			

	def SyncInActive(self, state):
		if self.Syncmode == 'SYNC_CHOP':
			if self.syncIn:		
				self.syncIn.par.active = state
				self.syncIn.bypass = not state
			else:
				self.syncIn = self.ownerComp.create(syncinCHOP, 'syncin')
				self.syncIn.par.multicastaddress = self.syncAddress
				self.syncIn.par.port = self.syncPort
				self.syncIn.par.timeout = self.syncTimeout
				self.syncIn.outputConnectors[0].connect(self.nullSyncIn)
				self.syncIn.nodeX = -725
				self.syncIn.nodeY = -400
				self.nullSyncIn.lock = False

			self.shdmemIn.par.active = False
			self.touchIn.par.active = False

		elif self.Syncmode == 'SHARED_MEM':
			if self.syncIn:
				self.nullSyncIn.lock = True
				self.syncIn.par.active = False
				self.syncIn.bypass = True
				self.syncIn.destroy()
			self.shdmemIn.par.active = state
			self.touchIn.par.active = False

		elif self.Syncmode == 'TOUCH_IN_OUT':
			if self.syncIn:
				self.nullSyncIn.lock = True
				self.syncIn.par.active = False
				self.syncIn.bypass = True
				self.syncIn.destroy()
			self.shdmemIn.par.active = False
			self.touchIn.par.active = state			
		
		self.switchSync.par.index = int(state)

	def SetCrossComps(self, comp1, comp2):
		index1 = comp1.op('index')
		self.selCrossDataComp1.par.chop = index1.path
		self.selCrossDataComp1.par.renameto = index1.path
		index2 = comp2.op('index')
		self.selCrossDataComp2.par.chop = index2.path
		self.selCrossDataComp2.par.renameto = index2.path

	def Cuestart(self, val):
		self.fplayer.CueStartSync()

	@property
	def Syncmode(self):
		return self.ownerComp.par.Syncmode.eval()
