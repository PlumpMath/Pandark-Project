import yaml

class Generic(yaml.YAMLObject):

    yaml_tag = u'!Generic'

    def __init__(self,model,body,props):
    	self.model  = model
    	self.pos    = props['pos']
    	self.quat   = props['quat']

    def getNode(self):
        return self.model.getParent()

    def command(self,cmd):
        pass

    def _getSize(self):
        hpr = self.model.getHpr()
        self.model.setHpr(0,0,0)
        minLimit, maxLimit = self.model.getTightBounds()
        self.model.setHpr(hpr) 
        return maxLimit - minLimit

    def _cleanup(self):
        print 'removing model', self.model
        self.model.remove()
        del self.model

    def __del__(self):
    	self._cleanup()