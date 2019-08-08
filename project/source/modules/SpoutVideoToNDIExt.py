"""
Extension classes enhance TouchDesigner components with python. An
extension is accessed via ext.ExtensionClassName from any operator
within the extended component. If the extension is promoted via its
Promote Extension parameter, all its attributes with capitalized names
can be accessed externally, e.g. op('yourComp').PromotedFunction().

Help: search "Extensions" in wiki
"""

from TDStoreTools import StorageManager
TDF = op.TDModules.mod.TDFunctions

class SpoutVideoToNDIExt:
	"""
	SpoutVideoToNDIExt description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		self.FPlayer = op.FPlayer

	@property
	def Node(self):
		return self.FPlayer.NODE

	@property
	def CanvasType(self):
		if self.FPlayer.NODE_INDEX < 7:
			return 'WALLS'
		else:
			return 'FLOOR'

	@property
	def CanvasIndex(self):
		if self.FPlayer.NODE_INDEX < 7:
			return 0
		else:
			return 1

	@property
	def CanvasSizeW(self):
		return self.Node.Canvassizew
	@property
	def CanvasSizeH(self):
		return self.Node.Canvassizeh
	@property
	def RenderSizeW(self):
		return self.Node.Rendersizew
	@property
	def RenderSizeH(self):
		return self.Node.Rendersizeh
	@property
	def RenderOffsetX(self):
		return self.Node.Renderoffsetx
	@property
	def RenderOffsetY(self):
		return self.Node.Renderoffsety
		
	@property
	def PreviewScale(self):
		return (self.FPlayer.NODES[1].Rendersizeh / self.FPlayer.NODES[1].Canvassizeh)	

	@property
	def Scale(self):
		if self.CanvasType == 'WALLS':
			if self.FPlayer.NODE_INDEX <= 1:
				return self.ownerComp.par.Wallscale * self.PreviewScale
			else:
				return self.ownerComp.par.Wallscale
		else:
			return self.ownerComp.par.Floorscale.eval()

	@property
	def TranslateX(self):
		if self.CanvasType == 'WALLS':
			tx = self.ownerComp.par.Wallstranslatex.eval()
		else:
			tx = self.ownerComp.par.Floortranslatex.eval()
		if self.FPlayer.NODE_INDEX <= 1:	
			return (tx - self.Node.Renderoffsetx) * self.PreviewScale
		else:
			return tx - self.Node.Renderoffsetx


	@property
	def TranslateY(self):
		if self.CanvasType == 'WALLS':
			ty = self.ownerComp.par.Wallstranslatey.eval()
		else:
			ty = self.ownerComp.par.Floortranslatey.eval()
		
		if self.FPlayer.NODE_INDEX <= 1:	
			return (ty - self.Node.Renderoffsety) * self.PreviewScale	
		else:
			return ty - self.Node.Renderoffsety	

