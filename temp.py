from PyQt6 import QtCore, QtGui, QtWidgets
import sys

class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.widget = QtWidgets.QWidget()
        self.widget.setSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        self.setCentralWidget(self.widget)

        self.h_layout = QtWidgets.QHBoxLayout()
        # self.h_layout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetNoConstraint)
        self.widget.setLayout(self.h_layout)

        self.label = QtWidgets.QLabel()
        self.label.setSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        self.label.setText("1234567891011121314151617181920212223242526272829303132333435363738")
        self.h_layout.addWidget(self.label)

        self.button = QtWidgets.QPushButton()
        self.button.setSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        self.button.setText("<=>")
        self.h_layout.addWidget(self.button)

app = QtWidgets.QApplication(sys.argv)
main = Main()
main.show()
sys.exit(app.exec())