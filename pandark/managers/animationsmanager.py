from direct.interval.IntervalGlobal import *

class AnimationsManager(object):

	def __init__(self):
		self.__animationsDict = {}
		self.__sequences  = {}
		self.__animations = {}

	def getAnimation(self,name):
		return self.__animationsDict[name]

	def createAnimation(self,node,animations):
		entName = node.getName()
		self.__sequences[entName] = {}
		if animations:
			for anim in animations:
				self.__sequences[entName][anim] = Sequence()								
				prevTime = 0
				for val in animations[anim]['seq']:
					self.__sequences[entName][anim].append( node.posQuatScaleInterval(val[0]-prevTime,val[1],val[2],val[3]) )
					prevTime = val[0]					
				if animations[anim]['enable']:
					self.play(entName, anim, animations[anim]['loop'])

	def play(self,entName, aniName, loop=False):
		if loop:
			self.__sequences[entName][aniName].loop()
		else:
			self.__sequences[entName][aniName].start()