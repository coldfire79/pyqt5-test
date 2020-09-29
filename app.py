import sys
import os
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QMainWindow
from PyQt5.QtCore import QCoreApplication

import numpy as np

from canvas import MatplotCanvas
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage

data_dir = Path(os.path.abspath(os.path.dirname(__file__))) / 'data'

# to fix `Could not find QtWebEngineProcess` error
if hasattr(sys, '_MEIPASS'):
    if sys.platform == 'darwin':
        os.environ['QTWEBENGINEPROCESS_PATH'] = os.path.normpath(os.path.join(
            sys._MEIPASS, 'PyQt5', 'Qt', 'lib',
            'QtWebEngineCore.framework', 'Helpers', 'QtWebEngineProcess.app',
            'Contents', 'MacOS', 'QtWebEngineProcess'
        ))
        print("-"*50)
        print('QTWEBENGINEPROCESS_PATH:', os.environ['QTWEBENGINEPROCESS_PATH'])
        print("-"*50)


class WebEnginePage(QWebEnginePage):
    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
        print("javaScriptConsoleMessage: ", level, message, lineNumber, sourceID)



class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.initUI()

    def initUI(self):
        form_widget = FormWidget(self)
        # form_widget = QPushButton("Dummy", self)

        canvas = MatplotCanvas(parent=self, width=8, height=8, dpi=200)
        self.update(canvas)

        btn = QPushButton('Quit', self)
        btn.move(50, 50)
        btn.resize(btn.sizeHint())
        btn.clicked.connect(QCoreApplication.instance().quit)

        _widget = QWidget()
        mainLayout = QVBoxLayout(_widget)
        subLayout = QHBoxLayout()
        subLayout.addWidget(canvas)
        subLayout.addWidget(btn)

        mainLayout.addLayout(subLayout)
        mainLayout.addWidget(form_widget)

        self.setCentralWidget(_widget)

        self.setWindowTitle('Quit Button')
        self.setGeometry(300, 300, 300, 200)
        self.show()

    def update(self, canvas):
        canvas.axes.plot(np.random.rand(10), ls="--", lw=0.3, c='r')
        canvas.draw()

class FormWidget(QWidget):
    def __init__(self, parent):
        super(FormWidget, self).__init__(parent)
        self.__controls()
        self.__layout()

    def __controls(self):
        html = open(f"{data_dir}/test.html", 'r').read()
        self.browser = QWebEngineView()
        self.browser.setPage(WebEnginePage(self.browser))
        self.browser.setHtml(html)
        self.browser.loadFinished.connect(self.onLoadFinished)

    def onLoadFinished(self, ok):
        if ok:
            self.browser.page().runJavaScript("helloWorld(1, \"12\")", self.ready)

    def __layout(self):
        self.vbox = QVBoxLayout()
        self.hBox = QVBoxLayout()
        self.hBox.addWidget(self.browser)
        self.vbox.addLayout(self.hBox)
        self.setLayout(self.vbox)

    def ready(self, returnValue):
        print(returnValue)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())