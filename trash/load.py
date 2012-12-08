from pandac.PandaModules import loadPrcFileData 
loadPrcFileData("", "load-display tinydisplay")
loadPrcFileData("", "window-type none") 
loadPrcFileData("", "model-cache-dir $MAIN_DIR/tmp/pandacache")

from direct.directbase import DirectStart

import sys

if len(sys.argv) == 2:
	print sys.argv[1]
else:
	print 'Usage: load <file>'

def callback(model):
	print model

loader.loadModel('assets/models/humans/rachel')

open('tmp/.cache','wb').close()