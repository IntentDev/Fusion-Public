class SyncExt:

	def __init__(self, ownerComp):

		self.ownerComp = ownerComp
		self.fplayer = parent.FPlayer
		self.syncOut = ownerComp.op('syncout')
		self.syncIn = ownerComp.op('syncin')
		self.switchSync = ownerComp.op('switchSync')
		self.syncSources = ownerComp.op('syncSources')
		self.selCrossDataComp1 = self.syncSources.op('selCrossDataComp1')
		self.selCrossDataComp2 = self.syncSources.op('selCrossDataComp2')

	def SyncOutActive(self, state):

		self.syncOut.par.active = state
		self.syncOut.bypass = not state

	def SyncInActive(self, state):

		self.syncIn.par.active = state
		self.syncIn.bypass = not state
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
