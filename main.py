from pandac.PandaModules import loadPrcFile, loadPrcFileData
from pandac.PandaModules import Filename
loadPrcFile(Filename.expandFrom("$MAIN_DIR/etc/config.prc"))

from panda3d.core import ConfigVariableString
maxThreads = ConfigVariableString( 'max-num-threads', '' )

# import multiprocessing
# coresNum = multiprocessing.cpu_count()
import os

coresNum =  int( os.environ["NUMBER_OF_PROCESSORS"] )

threadsNum = [ pow(coresNum,3) , int(maxThreads.getValue()) ]

#threadsNum = [ pow(coresNum,3) , int(q) ]

loadPrcFileData('', 'loader-num-threads ' + str( min(threadsNum) ) )

if coresNum > 1:
    loadPrcFileData('', 'threading-model  cull/draw' )

from direct.showbase.ShowBase import ShowBase

from pandark.core import Core

class Main(ShowBase):
  
    def __init__(self):
        ShowBase.__init__(self)

        self.core = Core()

        self.core.demand("Menu", "MainMenu")
        self.accept('a', self.load)
        self.accept('b', self.ex)

        #s = loader.loadSound(base.musaicManager,'game/assets/sounds/breathing.wav')
        #s.play()

        self.run()

    def ex(self):
        base.setFrameRateMeter(False)

    def onload(self,sound):
        print sound

    def load(self):
        self.core.demand("Loading", "scene2")

import psyco
psyco.full()

Main()