import yaml

class ActionArea(yaml.YAMLObject):

    yaml_tag = u'!ActionArea'

    def init(self,props):
		self.name = props['name']
		dimensions = props['dimensions']

		ghost = physicsMgr.createGhost( self.name, self.shape_type, dimensions )
		ghostNP = render.attachNewNode(ghost)
		ghostNP.setPos( props['origin'] )