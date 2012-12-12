from game.classes.generic import Generic

class Human(Generic):

    yaml_tag = u'!Human'

    def init(self,model,body,props):
    	Generic.__init__(self,model,body,props)