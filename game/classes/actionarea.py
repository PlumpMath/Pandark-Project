import yaml

class ActionArea(yaml.YAMLObject):

    yaml_tag = u'!ActionArea'

    def init(self,props):
		self.name = props['name']
		dimensions = props['dimensions']

		print self.name

		ghost = physicsMgr.createGhost( self.shape_type, dimensions )
		# ghostNP = render.attachNewNode(ghost)
		# ghostNP.setPos( props['origin'] )