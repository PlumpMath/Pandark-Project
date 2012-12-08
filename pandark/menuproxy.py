import types
from errors import ScenarioLoadingError

class MenuProxy(object):

	def __init__(self, menu):

		if isinstance(menu, types.StringTypes):
			import game.gui as gui
			try:
				self.menu = getattr(gui, menu)()
			except AttributeError:
				raise ScenarioLoadingError(menu)
		else:
			self.menu = menu()