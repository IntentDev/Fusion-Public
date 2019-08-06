import copy
class ParProperty:
	# todo: - setup per parp execute getter, setter, postSetter and parCallback
	#		- setup filtering handling of par expressions, exports and bindings
	def __init__(	self, obj, name, ownerComp, parpGroup, fGet=None, 
					fSet=None, fPostSet=None, fDelete=None, 
					fParCallback=None, doc=None):

		self.obj = obj
		self.name = name
		self.ownerComp = ownerComp
		self.par = getattr(self.ownerComp.par, self.name)
		self.notPulse = not self.par.isPulse
		self.parpGroup = parpGroup
		self.fGet = fGet
		self.fSet = fSet
		self.fPostSet = fPostSet
		self.fDelete = fDelete
		self.fParCallback = fParCallback

		if doc is None and fGet is not None:
			doc = fGet.__doc__
		self.__doc__ = doc

	def __get__(self, obj, objType=None):

		if obj is None:
			return self

		value = getattr(self.ownerComp.par, self.name).eval()

		if self.fGet is not None and self.parpGroup.execGet:
			self.fGet(value)

		return value

	def __set__(self, obj, value):

		# print(	'\n__set__ called on attribute set - which calls both',
		# 		'fSet() and fPostSet() functions if they exist')	

		if self.parpGroup.toggleExecParCallback:
			for r in runs:
				if r.group == self.parpGroup.name:
					r.kill()
			self.parpGroup.execParCallback = False
			run("getattr(args[0], args[1]).execParCallback = True", 
				self.ownerComp, self.parpGroup.name,
				delayFrames=1, group=self.parpGroup.name)

		if self.notPulse:
			prev = self.par.eval()

		if self.fSet is not None and self.parpGroup.execSet:
			value = self.fSet(value)
		
		setattr(self.ownerComp.par, self.name, value)
	
		if self.fPostSet is not None and self.parpGroup.execPostSet:
			self.fPostSet(value)

		if self.fParCallback is not None and self.parpGroup.setCallParCallback:
			if self.notPulse:
				args = [self.obj, self.par, self.ownerComp, prev]
			else:
				args = [self.obj, self.par, self.ownerComp]
				
			self.fParCallback(*args)

	def __delete__(self, obj):

		print('\nParProperty:\t\t\t\t', self.name, 'has been deleted')
		if self.fDelete is not None:
			self.fDelete(obj)

	def parCallback(self, par, *args):

		if self.fParCallback is not None:
			self.fParCallback(self.obj, par, *args)


def parProperty(obj, name, ownerComp=None, parpGroup=None, 
				fGet=None, fSet=None, fPostSet=None,
				fDelete=None, fParCallback=None, doc=None,
				parCallbacksDAT=None):

	ownerComp = getOwnerComp(obj, ownerComp)

	if not parpGroup:
		parpGroup = 'ParpGrp'

	if not hasattr(obj, parpGroup):
		setattr(obj, parpGroup, 
				copy.deepcopy(ParpGroup(obj, ownerComp, parpGroup)))

	parg = getattr(obj, parpGroup)

	parp = ParProperty(	obj, name, ownerComp, parg,
						fGet=fGet, fSet=fSet, fPostSet=fPostSet,
						fDelete=fDelete, fParCallback=fParCallback,
						doc=doc)

	setattr(obj.__class__, name, parp)
	parp = getattr(obj.__class__, name)
	parg.appendParp(name, parp)
	if parCallbacksDAT:
		parg.setParCallbacks(parCallbacksDAT)
	return parp


def parProperties(	obj, parNames=None, parpGroup=None, 
					ownerComp=None, filterPars=[], customPars=True, 
					builtinPars=False, parCallbacksDAT=None):

	ownerComp = getOwnerComp(obj, ownerComp)

	if not parpGroup:
		parpGroup = 'ParpGrp'

	if not hasattr(obj, parpGroup):
		setattr(obj, parpGroup, 
				copy.deepcopy(ParpGroup(obj, ownerComp, parpGroup)))
		
	if parNames:
		for name in parNames:
		
			if name not in filterPars:
				parProp = parProperty(
							obj, name, ownerComp, parpGroup)

	else:

		pars = []
		if customPars and builtinPars: pars = ownerComp.pars()
		elif customPars: pars = ownerComp.customPars
		elif builtinPars: 
			for par in ownerComp.pars():
				if not par.isCustom:
					pars.append(par)

		for par in pars:
			
			if par.tupletName not in filterPars:
				parp = parProperty(
							obj, par.name, ownerComp, parpGroup)

	parg = getattr(obj, parpGroup)	
	if parCallbacksDAT:
		parg.setParCallbacks(parCallbacksDAT)			

	return parg

class ParpGroup:

	def __init__(	self, obj, ownerComp, name, parNames=[], 
					toggleExecParCallback=True,
					setCallParCallback=True):

		self.obj = obj
		self.ownerComp = ownerComp
		self.name = name
		self.parNames = parNames
		self._parCallbacksDAT = None
		self.toggleExecParCallback = toggleExecParCallback
		self.setCallParCallback = setCallParCallback
		self.execFuncs = True
		self._execGet = True
		self._execSet = True
		self._execPostSet = True
		self._execParCallback = tdu.Dependency(True)

	def setParCallbacks(self, parCallbacksDAT):
		
		if parCallbacksDAT:
			self._parCallbacksDAT = parCallbacksDAT

			parCallbacks = self._parCallbacksDAT.module
			for parName in self.parNames:

				parp = getattr(self, parName)
				if parp.fParCallback is None:
					if hasattr(parCallbacks, parName):
						parCallback = getattr(parCallbacks, parName)
						parp.fParCallback = parCallback

	def appendParp(self, name, parp):

		setattr(self, name, parp)

		if name not in self.parNames:
			self.parNames.append(name)

	@property
	def parCallbacksDAT(self):
		return self._parCallbacksDAT
	
	@parCallbacksDAT.setter
	def parCallbacksDAT(self, value):
		self.setParCallbacks(value)

	@property
	def execGet(self):
		return self._execGet and self.execFuncs

	@execGet.setter
	def execGet(self, value):
		self._execGet = value
	
	@property
	def execSet(self):
		return self._execSet and self.execFuncs

	@execSet.setter
	def execSet(self, value):
		self._execSet = value

	@property
	def execPostSet(self):
		return self._execPostSet and self.execFuncs

	@execPostSet.setter
	def execSet(self, value):
		self._execPostSet = value

	@property
	def execParCallback(self):
		return self._execParCallback.val and self.execFuncs

	@execParCallback.setter
	def execParCallback(self, value):
		self._execParCallback.val = value

def getOwnerComp(obj, ownerComp):

	if not ownerComp:
		if hasattr(obj, 'ownerComp'):
			ownerComp = obj.ownerComp
		else:
			raise AttributeError (	
					'Extension does not have "ownerComp" ' +
					'attribute, specify extension ownerComp ' +
					'attribute via ownerComp argument')

	return ownerComp


