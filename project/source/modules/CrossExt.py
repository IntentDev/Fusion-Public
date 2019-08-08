class CrossExt:
	"""
	CrossExt description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		self.fPlayer = parent.FPlayer
		self.crossBlend = ownerComp.op('crossBlend')
		self.trigger = ownerComp.op('trigger1')
		self.crossChop = ownerComp.op('crossVal')
		self.Select1 = ownerComp.op('select1')
		self.Select2 = ownerComp.op('select2')

		self.selects = [self.Select1, self.Select2]
		#self.CrossVal = 0

		self.runGroup = str(ownerComp.id)

	def CrossFade(self, comp):
		trigVal = self.trigger[0].eval()
		if trigVal == 0.0 or trigVal == 1.0:
			#if self.fPlayer.CtrlInt:	
			self.NextTop = comp.Texture
			self.Cross()
			self.fPlayer.SetSyncSelects()

		else:
			for r in runs:
				if r.group == self.runGroup:
					r.kill()

			run("args[0].CrossFade(args[1])", self.ownerComp, comp,
			delayFrames=1, group=self.runGroup)

	def CrossFadeRemote(self, comp):
		self.CrossVal = round(self.crossChop[0].eval())
		self.NextTop = comp.Texture
		self.Cross()
		self.fPlayer.SetSyncSelects()

	def CrossFadeEnd(self):
		if self.PrevComp and self.PrevComp != self.CurrentTop.parent():		
			self.PrevComp.End()

	def Cross(self, *args):
		self.CrossVal = -1 * self.CrossVal + 1

	def SetCrossBlend(self, val, prev):
		self.crossBlend.par.index = val
		if (val == 1.0 or val == 0.0):
			self.crossBlend.par.blend = False
		else:
			self.crossBlend.par.blend = True
	
	def Resw(self, par):
		self.crossBlend.par.resolution1 = par.eval()

	def Resh(self, par):
		self.crossBlend.par.resolution2 = par.eval()

	@property
	def CrossVal(self):
		return self.ownerComp.fetch('CrossVal', 0)

	@CrossVal.setter
	def CrossVal(self, value):
		self.ownerComp.store('CrossVal', value)

	@property
	def currentSelect(self):
		return self.selects[self.CrossVal]

	@property
	def nextSelect(self):
		return self.selects[-1 * self.CrossVal + 1]

	@property
	def CurrentTop(self):
		return self.currentSelect.par.top.eval()

	@property
	def NextTop(self):
		return self.nextSelect.par.top.eval()

	@NextTop.setter
	def NextTop(self, value):
		self.nextSelect.par.top = value

	@property
	def PrevComp(self):
		PrevComp = self.fPlayer.MasterCue
		if self.nextSelect.par.top.eval():
			PrevComp = self.nextSelect.par.top.eval().parent()
		return PrevComp

	@property
	def Crossduration(self):
		return self.ownerComp.par.Crossduration.eval()

	@Crossduration.setter
	def Crossduration(self, value):
		self.ownerComp.par.Crossduration = value



	

	
	

