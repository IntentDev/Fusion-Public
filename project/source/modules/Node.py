class Node:

	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		self.viewOutput = ownerComp.op('viewOutput')
		self.viewMasterUI = ownerComp.op('viewMasterUI')

	@property
	def Index(self):
		return self.ownerComp.digits

	@property
	def Address(self):
		return self.ownerComp.par.Address.eval()

	@Address.setter
	def Address(self, value):
		self.ownerComp.par.Address = value

	@property
	def Server(self):
		return self.ownerComp.par.Server.eval()

	@Server.setter
	def Server(self, value):
		self.ownerComp.par.Server = value

	@property
	def Gpu(self):
		return self.ownerComp.par.Gpu.eval()

	@Gpu.setter
	def Gpu(self, value):
		self.ownerComp.par.Gpu = value

	@property
	def Monitor(self):
		return self.ownerComp.par.Monitor.eval()

	@Monitor.setter
	def Monitor(self, value):
		self.ownerComp.par.Monitor = value

	@property
	def Winsizew(self):
		return self.ownerComp.par.Winsizew.eval()

	@Winsizew.setter
	def Winsizew(self, value):
		self.ownerComp.par.Winsizew = value

	@property
	def Winsizeh(self):
		return self.ownerComp.par.Winsizeh.eval()

	@Winsizeh.setter
	def Winsizeh(self, value):
		self.ownerComp.par.Winsizeh = value

	@property
	def Winoffsetx(self):
		return self.ownerComp.par.Winoffsetx.eval()

	@Winoffsetx.setter
	def Winoffsetx(self, value):
		self.ownerComp.par.Winoffsetx = value

	@property
	def Winoffsety(self):
		return self.ownerComp.par.Winoffsety.eval()

	@Winoffsety.setter
	def Winoffsety(self, value):
		self.ownerComp.par.Winoffsety = value

	@property
	def Rendercanvas(self):
		return self.ownerComp.par.Rendercanvas.eval()

	@Rendercanvas.setter
	def Rendercanvas(self, value):
		self.ownerComp.par.Rendercanvas = value

	@property
	def Canvassizew(self):
		return self.ownerComp.par.Canvassizew.eval()

	@Canvassizew.setter
	def Canvassizew(self, value):
		self.ownerComp.par.Canvassizew = value

	@property
	def Canvassizeh(self):
		return self.ownerComp.par.Canvassizeh.eval()

	@Canvassizeh.setter
	def Canvassizeh(self, value):
		self.ownerComp.par.Canvassizeh = value

	@property
	def Noderendersizew(self):
		return self.ownerComp.par.Noderendersizew.eval()

	@Noderendersizew.setter
	def Noderendersizew(self, value):
		self.ownerComp.par.Noderendersizew = value

	@property
	def Noderendersizeh(self):
		return self.ownerComp.par.Noderendersizeh.eval()

	@Noderendersizeh.setter
	def Noderendersizeh(self, value):
		self.ownerComp.par.Noderendersizeh = value

	@property
	def Noderenderoffsetx(self):
		return self.ownerComp.par.Noderenderoffsetx.eval()

	@Noderenderoffsetx.setter
	def Noderenderoffsetx(self, value):
		self.ownerComp.par.Noderenderoffsetx = value

	@property
	def Noderenderoffsety(self):
		return self.ownerComp.par.Noderenderoffsety.eval()

	@Noderenderoffsety.setter
	def Noderenderoffsety(self, value):
		self.ownerComp.par.Noderenderoffsety = value

	@property
	def Ismaster(self):
		return self.ownerComp.par.Ismaster.eval()

	@Ismaster.setter
	def Ismaster(self, value):
		self.ownerComp.par.Ismaster = value

		state = bool(value)

		if state:
			self.viewOutput.outputCOMPConnectors[0].connect(self.viewMasterUI)
		
		else:
			self.viewMasterUI.inputCOMPConnectors[0].disconnect()

	@property
	def Ismastersync(self):
		return self.ownerComp.par.Ismastersync.eval()

	@Ismastersync.setter
	def Ismastersync(self, value):
		self.ownerComp.par.Ismastersync = value

	@property
	def Ispreviewrender(self):
		return self.ownerComp.par.Ispreviewrender.eval()

	@Ispreviewrender.setter
	def Ispreviewrender(self, value):
		self.ownerComp.par.Ispreviewrender = value

	@property
	def Isbackup(self):
		return self.ownerComp.par.Isbackup.eval()

	@Isbackup.setter
	def Isbackup(self, value):
		self.ownerComp.par.Isbackup = value

	@property
	def Outputvideo(self):
		return self.ownerComp.par.Outputvideo.eval()

	@Outputvideo.setter
	def Outputvideo(self, value):
		self.ownerComp.par.Outputvideo = value

	@property
	def Outputaudio(self):
		return self.ownerComp.par.Outputaudio.eval()

	@Outputaudio.setter
	def Outputaudio(self, value):
		self.ownerComp.par.Outputaudio = value

	@property
	def Username(self):
		return self.ownerComp.par.Username.eval()

	@Username.setter
	def Username(self, value):
		self.ownerComp.par.Username = value

	@property
	def Password(self):
		return self.ownerComp.par.Password.eval()

	@Password.setter
	def Password(self, value):
		self.ownerComp.par.Password = value

	@property
	def Movfilepostfix(self):
		return self.ownerComp.par.Movfilepostfix.eval()

	@Movfilepostfix.setter
	def Movfilepostfix(self, value):
		self.ownerComp.par.Movfilepostfix = value


	

