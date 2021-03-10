# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui/FlashcardSetEdit.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_FlashcardSetEdit(object):
    def setupUi(self, FlashcardSetEdit):
        FlashcardSetEdit.setObjectName("FlashcardSetEdit")
        FlashcardSetEdit.resize(1024, 420)
        self.verticalLayout = QtWidgets.QVBoxLayout(FlashcardSetEdit)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.title = QtWidgets.QLabel(FlashcardSetEdit)
        font = QtGui.QFont()
        font.setPointSize(28)
        font.setBold(False)
        font.setWeight(50)
        font.setKerning(True)
        self.title.setFont(font)
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setObjectName("title")
        self.verticalLayout.addWidget(self.title)
        self.frame = QtWidgets.QFrame(FlashcardSetEdit)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame.setObjectName("frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.scrollArea = QtWidgets.QScrollArea(self.frame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 984, 267))
        self.scrollAreaWidgetContents.setStyleSheet("QWidget#scrollAreaWidgetContents{background-color: rgb(192, 192, 192);}")
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_2.addWidget(self.scrollArea)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.new_button = QtWidgets.QPushButton(self.frame)
        self.new_button.setObjectName("new_button")
        self.horizontalLayout_3.addWidget(self.new_button)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.delete_button = QtWidgets.QPushButton(self.frame)
        self.delete_button.setObjectName("delete_button")
        self.horizontalLayout_3.addWidget(self.delete_button)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.verticalLayout.addWidget(self.frame)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.button_back = QtWidgets.QPushButton(FlashcardSetEdit)
        self.button_back.setObjectName("button_back")
        self.horizontalLayout_2.addWidget(self.button_back)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.button_help = QtWidgets.QPushButton(FlashcardSetEdit)
        self.button_help.setObjectName("button_help")
        self.horizontalLayout_2.addWidget(self.button_help)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.button_home = QtWidgets.QPushButton(FlashcardSetEdit)
        self.button_home.setObjectName("button_home")
        self.horizontalLayout_2.addWidget(self.button_home)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(FlashcardSetEdit)
        QtCore.QMetaObject.connectSlotsByName(FlashcardSetEdit)

    def retranslateUi(self, FlashcardSetEdit):
        _translate = QtCore.QCoreApplication.translate
        FlashcardSetEdit.setWindowTitle(_translate("FlashcardSetEdit", "Form"))
        self.title.setText(_translate("FlashcardSetEdit", "Edit Set"))
        self.new_button.setText(_translate("FlashcardSetEdit", "New Item"))
        self.delete_button.setText(_translate("FlashcardSetEdit", "Delete Set"))
        self.button_back.setText(_translate("FlashcardSetEdit", "Back"))
        self.button_help.setText(_translate("FlashcardSetEdit", "Help"))
        self.button_home.setText(_translate("FlashcardSetEdit", "Home"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    FlashcardSetEdit = QtWidgets.QWidget()
    ui = Ui_FlashcardSetEdit()
    ui.setupUi(FlashcardSetEdit)
    FlashcardSetEdit.show()
    sys.exit(app.exec_())
