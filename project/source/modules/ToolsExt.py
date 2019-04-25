class ToolsExt:

	def __init__(self, ownerComp):
		# The component to which this extension is attached
		self.ownerComp = ownerComp
		self.propertiesText = ownerComp.op('propertiesText')


	def PropertyFromPar(self, par):

		text = '\t@property\n'
		text += '\tdef ' + par.name + '(self):\n'
		text += '\t\treturn self.ownerComp.par.' + par.name + '.eval()\n\n'
		text += '\t@' + par.name + '.setter\n'
		text += '\tdef ' + par.name + '(self, value):\n'
		text += '\t\tself.ownerComp.par.' + par.name + ' = value\n\n'

		return text


	def PropertiesFromPars(self, comp, builtin=False):

		properties = ''

		if not builtin:

			for par in comp.customPars:

				properties += self.PropertyFromPar(par)	

		else:

			for par in comp.pars():

				properties += self.PropertyFromPar(par)	

		self.propertiesText.text = properties


	def Createpropertiesfrompars(self, *args):

		comp = self.ownerComp.par.Propertiescomp.eval()

		if comp:
			builtin = self.ownerComp.par.Getbuiltinpars.eval()
			self.PropertiesFromPars(comp, builtin=builtin)

	def Viewpropertiestext(self, *args):

		self.propertiesText.openViewer()
		









	

