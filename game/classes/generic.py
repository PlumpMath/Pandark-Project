import yaml

class Generic(yaml.YAMLObject):

    yaml_tag = u'!Generic'

    def __init__(self,model,props):
    	self.model  = model
    	self.parent = props['parent']
    	self.pos    = props['pos']
    	self.quat   = props['quat']

    def getNode(self):
    	return self._np

    def _getSize(self):
        self.model.clearModelNodes()

        self.model.flattenLight()

        minLimit, maxLimit = self.model.getTightBounds()   

        return maxLimit - minLimit

    def _cleanUp(self):
    	self.init = None
    	del self.init, self.parent, self.pos, self.quat

    def command(self,cmd):
    	pass

    def __del__(self):
    	self.__cleanUp()    	
    	self.model.remove()
    	print 0