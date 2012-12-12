import os
from pandac.PandaModules import loadPrcFile#, loadPrcFileData
from pandac.PandaModules import Filename
loadPrcFile(Filename.expandFrom("$MAIN_DIR/etc/config.prc"))

# coresNum =  int( os.environ["NUMBER_OF_PROCESSORS"] )

# threadsNum = str(pow(coresNum,3) )

# loadPrcFileData('', 'loader-num-threads ' + threadsNum ) 

from direct.showbase.ShowBase import ShowBase

from pandark.core import Core

from pandark.physics.physicsmanager import PhysicsManager

import __builtin__

__builtin__.physicsMgr = PhysicsManager()

class Main(ShowBase):
  
    def __init__(self):
        ShowBase.__init__(self)

        self.core = Core()

        self.core.demand("Menu", "MainMenu")

        self.accept('a', self.load)
        self.accept('escape', self.exit)
        self.accept('f1', self.toggleWireframe)
        self.accept('f2', self.toggleTexture)
        self.accept('f3', self.toggleDebug)

        self.debugNP = physicsMgr.debug()

        #render.setShaderAuto()

        self.run()

    def toggleDebug(self):
        if self.debugNP.isHidden():
            #render.setShaderAuto()
            self.debugNP.show()
        else:
            #render.setShaderOff()
            #render.clearLight()
            self.debugNP.hide()

    def load(self):
        #scene name
        sceneName = "scenario01"
        self.core.demand("Loading", sceneName)

    def exit(self):
        os._exit(0)

try:
    import psyco
    psyco.full()
except ImportError:
    print 'Psyco is not installed.'

Main()