

class CueUIExt:
	"""
	CueUIExt description
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		self.parExec = ownerComp.op('parexecParent')
		

		self.cuePars = ownerComp.op('cuePars')	
		self.movFilePars = ownerComp.op('movFilePars')
		self.audioFilePars = ownerComp.op('audioFilePars')

		self.cueViewer = ownerComp.op('../cueViewer')

		self.runGroup = str(ownerComp.id)


	def activePulse(self):
		#print('ActivePulse')
		self.parExec.par.active = False
		
		for r in runs:
			if r.group == self.runGroup:
				r.kill()

		run("args[0].par.active = True", self.parExec,
			delayFrames=4)

	def Load(self, cue):

		self.cueViewer.par.top = cue.Texture
		self.cuePars.par.op = cue		
		self.movFilePars.par.op = cue.MovFileIn
		self.audioFilePars.par.op = cue.AudioFileIn

		self.activePulse()

		for par in self.ownerComp.customPars:

			setattr(self.ownerComp.par, par.name, getattr(cue, par.name))

