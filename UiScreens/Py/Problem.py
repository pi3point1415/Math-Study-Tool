# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui/Problem.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Problem(object):
    def setupUi(self, Problem):
        Problem.setObjectName("Problem")
        Problem.resize(959, 514)
        self.verticalLayout = QtWidgets.QVBoxLayout(Problem)
        self.verticalLayout.setObjectName("verticalLayout")
        self.title = QtWidgets.QLabel(Problem)
        font = QtGui.QFont()
        font.setPointSize(28)
        font.setBold(False)
        font.setWeight(50)
        font.setKerning(True)
        self.title.setFont(font)
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setObjectName("title")
        self.verticalLayout.addWidget(self.title)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.score = QtWidgets.QLabel(Problem)
        self.score.setObjectName("score")
        self.horizontalLayout_3.addWidget(self.score)
        self.score_percent = QtWidgets.QLabel(Problem)
        self.score_percent.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.score_percent.setObjectName("score_percent")
        self.horizontalLayout_3.addWidget(self.score_percent)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.frame = QtWidgets.QFrame(Problem)
        self.frame.setStyleSheet("QWidget#frame {background-color: rgb(192, 192, 192);}")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame.setLineWidth(3)
        self.frame.setObjectName("frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.problem_frame = QtWidgets.QFrame(self.frame)
        self.problem_frame.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.problem_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.problem_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.problem_frame.setObjectName("problem_frame")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.problem_frame)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.problem = QSvgWidget(self.problem_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.problem.sizePolicy().hasHeightForWidth())
        self.problem.setSizePolicy(sizePolicy)
        self.problem.setObjectName("problem")
        self.verticalLayout_4.addWidget(self.problem)
        self.verticalLayout_2.addWidget(self.problem_frame)
        self.answer_frame = QtWidgets.QFrame(self.frame)
        self.answer_frame.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.answer_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.answer_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.answer_frame.setObjectName("answer_frame")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.answer_frame)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.answer = QSvgWidget(self.answer_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.answer.sizePolicy().hasHeightForWidth())
        self.answer.setSizePolicy(sizePolicy)
        self.answer.setObjectName("answer")
        self.verticalLayout_3.addWidget(self.answer)
        self.verticalLayout_2.addWidget(self.answer_frame)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.button_new = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_new.sizePolicy().hasHeightForWidth())
        self.button_new.setSizePolicy(sizePolicy)
        self.button_new.setObjectName("button_new")
        self.horizontalLayout.addWidget(self.button_new)
        self.text_entry = QtWidgets.QLineEdit(self.frame)
        self.text_entry.setObjectName("text_entry")
        self.horizontalLayout.addWidget(self.text_entry)
        self.button_check = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_check.sizePolicy().hasHeightForWidth())
        self.button_check.setSizePolicy(sizePolicy)
        self.button_check.setObjectName("button_check")
        self.horizontalLayout.addWidget(self.button_check)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(1, 1)
        self.verticalLayout.addWidget(self.frame)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.button_back = QtWidgets.QPushButton(Problem)
        self.button_back.setObjectName("button_back")
        self.horizontalLayout_2.addWidget(self.button_back)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.button_help = QtWidgets.QPushButton(Problem)
        self.button_help.setObjectName("button_help")
        self.horizontalLayout_2.addWidget(self.button_help)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.button_home = QtWidgets.QPushButton(Problem)
        self.button_home.setObjectName("button_home")
        self.horizontalLayout_2.addWidget(self.button_home)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(Problem)
        QtCore.QMetaObject.connectSlotsByName(Problem)

    def retranslateUi(self, Problem):
        _translate = QtCore.QCoreApplication.translate
        Problem.setWindowTitle(_translate("Problem", "Form"))
        self.title.setText(_translate("Problem", "Problems"))
        self.score.setText(_translate("Problem", "Score: 0/0"))
        self.score_percent.setText(_translate("Problem", "0%"))
        self.button_new.setText(_translate("Problem", "New"))
        self.button_check.setToolTip(_translate("Problem", "<html><head/><body><p>Please note that your answer is checked by a computer which lacks the intuition of a human and may be incorrect</p></body></html>"))
        self.button_check.setText(_translate("Problem", "Check"))
        self.button_back.setText(_translate("Problem", "Back"))
        self.button_help.setText(_translate("Problem", "Help"))
        self.button_home.setText(_translate("Problem", "Home"))
from PyQt5.QtSvg import QSvgWidget


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Problem = QtWidgets.QWidget()
    ui = Ui_Problem()
    ui.setupUi(Problem)
    Problem.show()
    sys.exit(app.exec_())