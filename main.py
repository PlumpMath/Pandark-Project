from pandac.PandaModules import loadPrcFile, loadPrcFileData
from pandac.PandaModules import Filename
loadPrcFile(Filename.expandFrom("$MAIN_DIR/etc/config.prc"))

#from panda3d.core import ConfigVariableString
#maxThreads = ConfigVariableString( 'max-num-threads', '' )

# import multiprocessing
# coresNum = multiprocessing.cpu_count()

import os
coresNum =  int( os.environ["NUMBER_OF_PROCESSORS"] )

#threadsNum = [ pow(coresNum,3) , int(maxThreads.getValue()) ]

#loadPrcFileData('', 'loader-num-threads ' + str( min(threadsNum) ) )

if coresNum > 1:
    loadPrcFileData('', 'threading-model  cull/draw' )

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

        physicsMgr.debug().show()


        #m = loader.loadModel('smiley')
        #m.reparentTo(render)

        self.run()

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