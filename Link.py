class Links(object):
	def __init__(self,identity,start,dest,length,buffersize,method,minthreshold,maxthreshold):
		self.twoend = (start,dest)
		self.buffer = collections.deque()
		self.size = buffersize
		self.linkid = identity
		self.linklen = length
		self.method = method
		self.averagequeuelength = 0
		self.minthreshold = minthreshold
		self.maxthreshold = maxthreshold

	def getLinkLen(self):
		return self.linklen

	def getLinkId(self):
		return self.linkid

	def getTwoEnd(self):
		return self.twoend

	def getBufferSize(self):
		return self.size

	def getCurrentBufferSize(self):
		return len(self.buffer)

	def addPacketToLink(self,packetId):
		if self.method == 'RED':
			return False

		elif self.method == 'DropTail':
			if l
				en(self.buffer) == self.size():
				return
			self.buffer.append(packetId)










