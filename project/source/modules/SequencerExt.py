parprops = iop.Modules.op('parproperties').module

class SequencerExt:
	"""
	SequencerExt description
	"""
	def __init__(self, ownerComp):
		self.ownerComp = ownerComp
		parprops.parProperties(self, parCallbacksDAT=ownerComp.op('parCallbacks'))
		self.fPlayer = parent.FPlayer
		self.Timer = ownerComp.op('timer1')
		
		self.Timer.par.initialize.pulse()

	def Start(self):
		self.Timer.par.start.pulse()
		self.Timer.par.play = True

	def Play(self, value):
		self.Timer.par.play = value

	def Initialize(self):
		self.Timer.par.initialize.pulse()
		self.Timer.par.play = False

		self.fPlayer.GetAttr('PlaylistInitialize')

	def OnDone(self, value):
		self.Timer.par.ondone = value	

	def SegmentLength(self, cueIndex):
		cue = self.cue(cueIndex)
		nextCue = self.cue((cueIndex + 1) % len(self.curPlaylist))
		duration = cue.Duration
		duration -= nextCue.Crossduration
		return duration

	def SegmentCycle(self, cueIndex):
		cue = self.cue(cueIndex)
		followAction = cue.Followaction
		return int(followAction in ['CYCLE', 'CYCLE_LIMIT'])

	def SegmentCycleLimit(self, cueIndex):
		cue = self.cue(cueIndex)
		followAction = cue.Followaction
		return int(followAction == 'CYCLE_LIMIT')

	def SegmentMaxCycles(self, cueIndex):
		cue = self.cue(cueIndex)
		return cue.Maxcycles

	def GoToCue(self):
		if self.currentCue:
			followAction = self.currentCue.Followaction
			if followAction == 'GO_TO_CUE':
				return True	
		return False

	def TimerOnSegmentEnter(self, segment):
		cue = self.curPlaylist[segment+1][1]	
		self.fPlayer.GetAttr('CueSelect', cue)
		self.fPlayer.GetAttr('CueStart')
		self.currentCue = cue

	def TimerOnSegmentExit(self, segment):
		if self.GoToCue():
			goToSegment = self.currentCue.Gotocue	
			self.Timer.goTo(segment=goToSegment)

	def TimerOnInitialize(self):
		self.currentCue = None

	def TimerOnDone(self):
		endAction = self.EndAction
		if endAction == 'RE-INIT':
			self.Initialize()
		elif endAction == 'RE-START':
			run("args[0].Start()", self.ownerComp, delayFrames=2)

	def cue(self, cueIndex):
		return self.curPlaylist[cueIndex][1]

	@property
	def curPlaylist(self):
		return self.fPlayer.CurrentPlaylist.Playlist

	@property
	def EndAction(self):
		return self.fPlayer.UI_Sequencer.op('endAction').par.Value0.eval()



