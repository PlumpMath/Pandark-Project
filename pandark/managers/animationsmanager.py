from direct.interval.IntervalGlobal import *

class AnimationsManager(object):

	def __init__(self):
		self.__animationsDict = {}
		self.__sequences  = {}
		self.__animations = {}

	def getAnimation(self,name):
		return self.__animationsDict[name]

	def createAnimation(self,ent,animations):
		node = ent.getNode()

		if animations:
			for anim in animations:
				self.__sequences[anim] = Sequence()								
				prevTime = 0
				for val in animations[anim]['seq']:
					self.__sequences[anim].append( node.posQuatScaleInterval(val[0]-prevTime,val[1],val[2],val[3]) )
					prevTime = val[0]					
				if animations[anim]['enable']:
					self.play(anim, animations[anim]['loop'])

	def play(self, name, loop=False):
		if loop:
			self.__sequences[name].loop()
		else:
			self.__sequences[name].start()