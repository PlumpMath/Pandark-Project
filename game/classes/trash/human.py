from game.classes.generic import Generic

class Human(Generic):

	yaml_tag = u'!Human'

	sounds_list = []
	actions = []
	model = None

	def _init(self):
		self.speed = 10
		self.force = 10

		self.playActions()

	def _doPhysics(self,body,size):
		physicsMgr.createCapsule(body,size[0]/2,size[2])

	def _playSound(self,id=0,loop=False,play=True):
		#snd = loader.loadSound(base.musicManager,'game/assets/sounds/'+path)
		print self.sounds_list,'list'
		
		if len(self.sounds_list) >= id+1:
			snd = loader.loadSfx('game/assets/sounds/'+self.sounds_list[id])
			snd.setLoop(loop)
			if play:
				snd.play()
		else:
			print 'Warning: Sound id:',id,'not found.'

	def playActions(self):
		for act in self.actions:
			exec('self._'+act)

	def _run(self):
		print 'runnig'




		#from panda3d.core import FilterProperties
		#fp = FilterProperties()
		#fp.addReverb(0.6, 0.5, 0.1, 0.1, 0.1)
		#base.musicManager.configureFilters(fp)