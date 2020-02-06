CueComp = iop.FPlayer.op('modules/cuecomp').module.CueComp

class CueComp2DExt(CueComp):
	"""
	default custom content component for rendering 2D content
	across nodes.
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		CueComp.__init__(self, ownerComp)

	@property
	def Scale(self):
		if self.FPlayer.NODE.Ispreviewrender:
			return self.ownerComp.par.Scale * self.PreviewScale
		else:
			return self.ownerComp.par.Scale

	@property
	def TranslateX(self):
		tx = self.ownerComp.par.Translatex.eval()
		if self.FPlayer.NODE.Ispreviewrender:	
			return (tx - self.NODE.Noderenderoffsetx) * self.PreviewScale
		else:
			return tx - self.NODE.Noderenderoffsetx

	@property
	def TranslateY(self):
		ty = self.ownerComp.par.Translatey.eval()
		if self.FPlayer.NODE.Ispreviewrender:		
			return (ty - self.NODE.Noderenderoffsety) * self.PreviewScale	
		else:
			return ty - self.NODE.Noderenderoffsety	
	
