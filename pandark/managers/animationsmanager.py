from direct.interval.IntervalGlobal import *

class AnimationsManager(object):

	def __init__(self):
		self.reset()

	def reset(self):
		self.__animationsDict = {}
		self.__sequences  = {}
		self.play = True

	def getAnimation(self,name):
		return self.__sequences[name]

	def createAnimation(self,node,animations):		
		if animations:
			entName = node.getName()
			self.__sequences[entName] = {}
			for anim in animations:
				seq = Sequence(name=entName)								
				prevTime = 0
				for val in animations[anim]['seq']:
					seq.append( node.posQuatScaleInterval(val[0]-prevTime,val[1],val[2],val[3]) )
					prevTime = val[0]
				self.__sequences[entName][anim] = seq					
				if animations[anim]['enable']:
					self.playAnim(entName, anim, animations[anim]['loop'])

	def playAnim(self,entName, aniName, loop=False):
		if loop:
			self.__sequences[entName][aniName].loop()
		else:
			self.__sequences[entName][aniName].start()

	def togglePlay(self):
		self.play = not self.play
		if self.play:
			taskMgr.add(self.update, 'update')
			print self.ivals
			for i in self.ivals: 
				i.resume()
		else:
			taskMgr.remove('update')
			ivals=ivalMgr.getIntervalsMatching('*')
			self.ivals = []
			for i in ivals: 
				self.ivals.append(i)
				i.pause()

	def cleanup(self):
		ivals=ivalMgr.getIntervalsMatching('*')
		for i in ivals: 
			i.finish()
		self.reset()

	def destroy(self):
		self.cleanup()
		print 'destroy AnimationsManager'

	def __del__(self):
		print 'delete AnimationsManager'

