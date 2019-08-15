class ScenesExt:
	"""
	ScenesExt component extension to manage scene components 
	that can be selected and triggered by cues. All scenes
	need to have a 'CUE_COMP' tag in order to make use of 
	the CueCallback system.
	"""
	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp

	@property
	def SceneComps(self):
		return self.ownerComp.findChildren(tags=['CUE_COMP'])