from game.classes.generic import Generic

class Door(Generic):

    yaml_tag = u'!Door'

    def init(self,model,props):
		Generic.__init__(self,model,props)
		model.clearModelNodes()
		model.setPos(props['pos'])
		model.setQuat(props['quat'])
		model.setScale(props['scale'])
		model.flattenLight()
		model.reparentTo(self.parent)