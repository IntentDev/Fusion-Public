import pickle
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class RemoteExt:

	def __init__(self, ownerComp):

		self.ownerComp = ownerComp
		self.fPlayer = parent.FPlayer
		self.tcpip = ownerComp.op('tcpip')
		self.sync = ownerComp.op('sync')

		self.remoteFuncs = [self.setAttr, self.setPar, self.getAttr,
			self.parPulse, self.setDatCell, self.setDatText]

	def SetMode(self, mode):

		# modes = 	'LOCAL', 'LOCAL_CONTROL_EXTERNAL', 
		# 			'CONTROL_EXTERNAL', 'EXTERNAL', 'BACKUP_UI'

		self.tcpip.par.active = not mode == 'LOCAL'

		if mode == 'LOCAL':
			self.ConnectionMode = 'server'
			self.sync.SyncOutActive(False)
			self.sync.SyncInActive(False)

		elif mode == 'LOCAL_CONTROL_EXTERNAL':
			self.ConnectionMode = 'server'
			self.sync.SyncOutActive(self.fPlayer.Ismastersync)
			self.sync.SyncInActive(True)

		elif mode == 'CONTROL_EXTERNAL':
			self.ConnectionMode = 'server'	
			self.sync.SyncOutActive(self.fPlayer.Ismastersync)
			self.sync.SyncInActive(False)

		elif mode == 'EXTERNAL':
			self.ConnectionMode = 'client'
			self.sync.SyncOutActive(self.fPlayer.Ismastersync)
			self.sync.SyncInActive(True)

		elif mode == 'BACKUP_UI':
			self.ConnectionMode = 'client'
			self.sync.SyncOutActive(False)
			self.sync.SyncInActive(False)



	# Call to Call function, set attribute or set parameter on remote component
	##########################################
	def SetAttr(self, comp, attribute, value):
		args = pickle.dumps([0, comp.path, attribute, value])
		self.tcpip.sendBytes(args)

	def SetPar(self, comp, attribute, value):
		args = pickle.dumps([1, comp.path, attribute, value])
		self.tcpip.sendBytes(args)

	def GetAttr(self, comp, attribute, *args, **kwargs):
		#print(comp, attribute, *args, **kwargs)	
		data = pickle.dumps([2, comp.path, attribute, args, kwargs])
		self.tcpip.sendBytes(data)

	def ParPulse(self, comp, parName):
		args = pickle.dumps([3, comp.path, parName])
		self.tcpip.sendBytes(args)

	def SetDatCell(self, dat, row, col, val):
		args = pickle.dumps([4, dat.path, row, col, val])
		self.tcpip.sendBytes(args)

	def SetDatText(self, dat):
		args = pickle.dumps([5, dat.path, dat.text])
		self.tcpip.sendBytes(args)	

	# Receive
	##########################################
	def ReceiveBytes(self, bytes):
		if not self.fPlayer.NODE.Ismaster:
			data = pickle.loads(bytes)
			self.remoteFuncs[data[0]](data[1:])

	def setAttr(self, data):
		comp = op(data[0])
		attribute = data[1]
		value = data[2]
		setattr(comp, attribute, value)

	def setPar(self, data):
		comp = op(data[0])
		attribute = data[1]
		value = data[2]
		setattr(comp.par, attribute, value)

	def getAttr(self, data):
		#print(data)
		comp = op(data[0])
		attribute = data[1]
		args = data[2]
		kwargs = data[3]
	
		getattr(comp, attribute)(*args, **kwargs)

	def parPulse(self, data):
		comp = op(data[0])
		parName = data[1]
		if comp:		
			getattr(comp.par, parName).pulse()

	def setDatCell(self, data):
		dat = op(data[0])
		row = data[1]
		col = data[2]
		val = data[3]
		if dat:		
			dat[row, col] = val

	def setDatText(self, data):
		dat = op(data[0])
		text = data[1]
		if dat:		
			dat.text = text  
			
	@property
	def ConnectionMode(self):
		return self.tcpip.par.mode.eval()

	@ConnectionMode.setter
	def ConnectionMode(self, value):
		self.tcpip.par.mode = value	

	@property
	def Port(self):
		return self.tcpip.par.port.eval()

	@Port.setter
	def Port(self, value):
		self.tcpip.par.port = value	


	@property
	def Address(self):
		return self.tcpip.par.address.eval()

	@Address.setter
	def Address(self, value):
		self.tcpip.par.address = value	