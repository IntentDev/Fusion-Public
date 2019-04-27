import pickle
class NodeStatusExt():

	def __init__(self, ownerComp):
		
		self.ownerComp = ownerComp
		self.FPlayer = parent.FPlayer
		self.masterNode = ownerComp.op('node0')
		self.perform = ownerComp.op('perform')

		self.udpOut = ownerComp.op('udpoutStatus')
		self.udpIn = ownerComp.op('udpinStatus')
		self.NodeStatus = ownerComp.op('nodeStatus')

	def SendStatus(self):

		if absTime.frame % self.Sendinterval == 0:

			node = self.FPlayer.NODE
			node_index = node.Index
			node_name = node.name

			fps = int(self.perform['fps'])
			dropped_frames = int(self.perform['dropped_frames'])
			read_ahead_misses = int(self.perform['read_ahead_misses'])
			gpu_mem_used = int(self.perform['gpu_mem_used'])
			cpu_mem_used = int(self.perform['cpu_mem_used'])




			msg = [node_index, node_name, fps, dropped_frames, 
					read_ahead_misses, gpu_mem_used, cpu_mem_used]

			msg = pickle.dumps(msg)
			self.udpOut.sendBytes(msg)




	def ReceiveStatus(self, bytes):

		msg = pickle.loads(bytes)

		self.NodeStatus.replaceRow(msg[0] + 1, msg[1:])

		pass
	



	@property
	def Sendinterval(self):
		return self.ownerComp.par.Sendinterval.eval()