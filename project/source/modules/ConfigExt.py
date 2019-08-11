import shutil
import os
class ConfigExt():

	def __init__(self, ownerComp):
		
		self.ownerComp = ownerComp
		self.FPlayer = parent.FPlayer
		self.masterNode = ownerComp.op('node0')

	def GetNodes(self):

		nodes = self.ownerComp.findChildren(tags=['NODE'], name='^masterNode0')
		nodes.sort(key=lambda x: x.digits)

		return nodes

	def OnNumChildrenChange(self):

		nodes = self.GetNodes()
		nodeNames = [node.name for node in nodes]

		self.ownerComp.par.Selectnode.menuNames = nodeNames
		self.ownerComp.par.Selectnode.menuLabels = nodeNames


	def InitNode(self, node):

		node.Ismaster = False
		node.Ismastersync = False
		node.Ispreviewrender = False
		node.Isbackup = False
		node.Outputaudio = False

		viewOutput = node.op('viewOutput')
		viewOutput.outputCOMPConnectors[0].disconnect()
		viewOutput.outputCOMPConnectors[0].connect(node.op('output0'))
		
		if node.op('viewMasterUI'):
			node.op('viewMasterUI').destroy()


	def Saveallnodes(self, *args):

		confirm = ui.messageBox('Confirm Overwrite', 
		'''Save/Overwrite All Nodes?\n\nPrevious versions will be copied to: config/nodes/backup/''', 
		buttons=['Cancel', 'Save All Nodes'])

		if confirm == 1:

			path = '/config/nodes/'	
			dstDir = project.folder + path + 'backup'
			if not os.path.isdir(dstDir):
				os.mkdir(dstDir)

			backupFiles = [f for f in os.listdir(dstDir) if os.path.isfile(os.path.join(dstDir, f))]

			i = 0
			for backupFile in backupFiles:
				i = max(i, int(backupFile.split('.')[-2:][0]))
			i += 1

			for node in self.FPlayer.NODES:
				name = node.name + '.tox'
				
				srcPath = project.folder + path + node.name + '.tox'

				if os.path.isfile(srcPath):
					
					# better method above to maximum increment so backups
					# are in order if earlier files are deleted	
					#i = 0
					#while os.path.isfile(dstDir + '/'+ node.name + '.{}'.format(i) + '.tox'):
					#	i += 1

					dstPath = dstDir + '/'+ node.name + '.{}'.format(i) + '.tox'
					shutil.copy2(srcPath, dstPath)

				node.save(srcPath)






	

