import sys

from UIController import UIController

controller=UIController()
controller.window.show()
sys.exit(controller.application.exec_())