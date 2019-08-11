CueComp = op.FPlayer.op('modules/CueComp').module.CueComp
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
	def Period(self):
		if self.NODE.Ispreviewrender:
			return 1.0
		else:
			return self.NODE.Canvassizew / self.NODE.Noderendersizew

	@property
	def Scalex(self):
		return self.ownerComp.par.Scalex

	@property
	def Scaley(self):
		return self.ownerComp.par.Scaley

	@property
	def Translatex(self):
		tx = self.ownerComp.par.Translatex.eval()
		if self.NODE.Ispreviewrender:
			return tx
		else:
			return (tx + .5 * 
					self.NODE.Canvassizew / self.NODE.Noderendersizew 
					* self.Scalex
					- self.NODE.Noderenderoffsetx 
					/ self.NODE.Noderendersizew * self.Scalex
					- 2 * self.NODE.Noderendersizew
					/ self.NODE.Canvassizew )

	@property
	def Translatey(self):
		ty = self.ownerComp.par.Translatey.eval()
		if self.NODE.Ispreviewrender:
			return ty

		return (ty + .5 * self.NODE.Canvassizeh / self.NODE.Noderendersizeh 
				* self.Scaley
				- self.NODE.Noderenderoffsety 
				/ self.NODE.Noderendersizeh * self.Scaley
				- 2 * self.NODE.Noderendersizew
				/ self.NODE.Canvassizew) + 1.5


	
