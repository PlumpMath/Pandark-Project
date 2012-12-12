import yaml

class Generic(yaml.YAMLObject):

    yaml_tag = u'!Generic'

    def __init__(self,model,body,props):
    	self.model  = model
    	self.parent = props['parent']
    	self.pos    = props['pos']
    	self.quat   = props['quat']
        self._setPhysics(body)

    def getNode(self):
        return self.model.getParent()

    def command(self,cmd):
        pass

    def _setPhysics(self,body):
        np = render.attachNewNode(body)

        np.setPosQuat(self.pos,self.quat)

        self.model.reparentTo(np)

        self._cleanup()

    def _getSize(self):
        hpr = self.model.getHpr()
        self.model.setHpr(0,0,0)
        minLimit, maxLimit = self.model.getTightBounds()
        self.model.setHpr(hpr) 
        return maxLimit - minLimit

    def _cleanup(self):
    	self.init = None
    	del self.init, self.parent, self.pos, self.quat   

    def __del__(self):
    	self._cleanup()    	
    	self.model.remove()
    	print 0