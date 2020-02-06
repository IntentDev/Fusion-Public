"""
Extension classes enhance TouchDesigner components with python. An
extension is accessed via ext.ExtensionClassName from any operator
within the extended component. If the extension is promoted via its
Promote Extension parameter, all its attributes with capitalized names
can be accessed externally, e.g. op('yourComp').PromotedFunction().

Help: search "Extensions" in wiki
"""

import re
import os

class VideoConvertor:
	"""
	VideoConvertor description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp

		# attributes:
		self.movIn = ownerComp.op('moviefilein1')
		self.movOut = ownerComp.op('moviefileout0')
		self.FPlayer = parent.FPlayer
		self.batchFolder = ownerComp.op('batchFolder')
		self.outputs = 4
		self.movOuts = []
		self.texOuts = []

		for i in range(0, self.outputs):
			movOut = ownerComp.op('moviefileout{}'.format(i))
			self.movOuts.append(movOut)
			texOut = ownerComp.op('tex{}'.format(i))
			self.texOuts.append(texOut)

		self.time = self.ownerComp.time
		self.Record = False

		ownerComp.par.Outputfilename = ''	
		self.projRealTime = bool(project.realTime) # make sure it's a copy

		self.filePathsToConvert = []
	
	def Inputfile(self, par):
		val = par.eval()	
		self.SetupMovie(val)

	def SetupMovie(self, path):
		self.movIn.par.file = path
		self.movIn.cook(force=True)
		numFrames = self.ownerComp.time.rate / self.movIn.rate * self.movIn.numImages	
		self.time.end = numFrames
		self.time.rangeEnd = numFrames
		self.time.frame = 1
		self.time.play = False

	def Convert(self):
		f = tdu.PathInfo(self.movIn.par.file.eval())
		if f.ext.replace('.', '') in tdu.fileTypes['image']:
			self.Saveimages()
		
		else:
			path = self.ownerComp.par.Outputfolder.eval()
			name = self.ownerComp.par.Outputfilename.eval()

			if name == '':

				name = f.split('/')[-1:][0].replace(f.ext, '')
				codec = self.ownerComp.par.Codec.eval()

			if name != '':

				for i in range(0, self.outputs):
					path = self.ownerComp.par.Outputfolder.eval()

					nodeIndex = i
					node = self.FPlayer.NODES[nodeIndex]
					# uncomment to add render to network location 
					# specified in node	
					# address = node.Address
					# path = '//' + address + '/' + path		
					# path = path.replace(':', '')

					if not os.path.isdir(path):
						os.mkdir(path, 0o777)
				
					path += '/' + name	
					filePath = path
					postfix = '_' + node.Movfilepostfix
					filePath += postfix + '.mov'
					self.movOuts[i].par.file = filePath

			else:

				for i in range(0, self.outputs):
					self.movOuts[i].par.file = ''

			self.StartRecord()

	def Saveimages(self, *args):	
		path = self.ownerComp.par.Outputfolder.eval()
		name = self.ownerComp.par.Outputfilename.eval()

		if name == '':
			f = tdu.PathInfo(self.movIn.par.file.eval())	
			name = f.split('/')[-1:][0].replace(f.ext, '')

		for i in range(0, self.outputs):
			path = self.ownerComp.par.Outputfolder.eval()
			nodeIndex = i

			node = self.FPlayer.NODES[nodeIndex]
			# uncomment to add render to network location 
			# specified in node	
			# address = node.Address
			# path = '//' + address + '/' + path		
			# path = path.replace(':', '')

			if not os.path.isdir(path):
				os.mkdir(path, 0o777)
		
			path += '/' + name		
			if name != '':
				filePath = path

			postfix = '_' + node.Movfilepostfix
			filePath += postfix + self.ownerComp.par.Imagetype.eval()
			self.texOuts[i].save(filePath)

		# if len(self.filePathsToConvert) > 0:
		# 	run("args[0].startNextBatchFile()", self.ownerComp,
		# 	delayFrames=1, fromOP=self.ownerComp)

	def startNextBatchFile(self):
		self.ownerComp.par.Inputfile = self.filePathsToConvert[0]
		self.filePathsToConvert.pop(0)			
		run("args[0].Convert()", self.ownerComp,
		delayFrames=1, fromOP=self.ownerComp)

	# need to change local time level in order to function... 	
	def Startbatchconvert(self, par):
		self.filePathsToConvert = []	
		for r in self.batchFolder.rows()[1:]:
			self.filePathsToConvert.append(r[1].val)
		self.startNextBatchFile()
			
	def Startconversion(self, par):	
		self.Convert()

	def Stopconversion(self, par):		
		self.StopRecord()

	def StopRecord(self):
		self.Record = False
		self.time.play = False
		self.time.frame = 1
		project.realTime = self.projRealTime
		# if len(self.filePathsToConvert) > 0:
		# 	run("args[0].startNextBatchFile()", self.ownerComp,
		# 	delayFrames=1, fromOP=self.ownerComp)

	def StartRecord(self):	
		self.projRealTime = bool(project.realTime)		
		project.realTime = False
		self.time.frame = 1
		self.Record = True
		self.time.play = True

	def FrameStart(self, frame):
		if frame == self.ownerComp.time.end:
			self.Record = False
			run("args[0].Record=False", self.ownerComp,
				delayFrames=1)

	def FrameEnd(self, frame):
		if frame == self.ownerComp.time.end:
			self.StopRecord()

	@property
	def Mode(self):
		return self.ownerComp.par.Rendermode.eval()

	@Mode.setter
	def Mode(self, value):
		self.ownerComp.par.Rendermode = value		

	@property 
	def Record(self):
		return self.ownerComp.fetch('Record', False)

	@Record.setter
	def Record(self, state):
		self.ownerComp.store('Record', state)
		for movOut in self.movOuts:
			movOut.par.record = state


