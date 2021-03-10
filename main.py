# For the icon
import ctypes
# For closing the program properly
import sys

# PyQt5
import PyQt5.QtGui as QtGui
import PyQt5.QtWidgets as Qtw

# Main window module
from screens import MainWindow

# Helps set the icon correctly
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('math')

# Create application, set the style, set the icon, start the main window, and start the app
if __name__ == '__main__':
    app = Qtw.QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setWindowIcon(QtGui.QIcon('icon.ico'))
    win = MainWindow()
    sys.exit(app.exec_())
