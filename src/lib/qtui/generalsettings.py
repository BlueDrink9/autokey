#!/usr/bin/env python
# coding=UTF-8
#
# Generated by pykdeuic4 from generalsettings.ui on Wed Feb 29 20:25:38 2012
#
# WARNING! All changes to this file will be lost.
from PyKDE4 import kdecore
from PyKDE4 import kdeui
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(491, 444)
        self.verticalLayout_4 = QtGui.QVBoxLayout(Form)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.groupBox = QtGui.QGroupBox(Form)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.promptToSaveCheckbox = QtGui.QCheckBox(self.groupBox)
        self.promptToSaveCheckbox.setObjectName(_fromUtf8("promptToSaveCheckbox"))
        self.verticalLayout.addWidget(self.promptToSaveCheckbox)
        self.showTrayCheckbox = QtGui.QCheckBox(self.groupBox)
        self.showTrayCheckbox.setObjectName(_fromUtf8("showTrayCheckbox"))
        self.verticalLayout.addWidget(self.showTrayCheckbox)
        self.verticalLayout_4.addWidget(self.groupBox)
        self.groupBox_2 = QtGui.QGroupBox(Form)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.allowKbNavCheckbox = QtGui.QCheckBox(self.groupBox_2)
        self.allowKbNavCheckbox.setObjectName(_fromUtf8("allowKbNavCheckbox"))
        self.verticalLayout_2.addWidget(self.allowKbNavCheckbox)
        self.sortByUsageCheckbox = QtGui.QCheckBox(self.groupBox_2)
        self.sortByUsageCheckbox.setObjectName(_fromUtf8("sortByUsageCheckbox"))
        self.verticalLayout_2.addWidget(self.sortByUsageCheckbox)
        self.verticalLayout_4.addWidget(self.groupBox_2)
        self.groupBox_3 = QtGui.QGroupBox(Form)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.enableUndoCheckbox = QtGui.QCheckBox(self.groupBox_3)
        self.enableUndoCheckbox.setObjectName(_fromUtf8("enableUndoCheckbox"))
        self.verticalLayout_3.addWidget(self.enableUndoCheckbox)
        self.verticalLayout_4.addWidget(self.groupBox_3)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(kdecore.i18n(_fromUtf8("Form")))
        self.groupBox.setTitle(kdecore.i18n(_fromUtf8("Application")))
        self.promptToSaveCheckbox.setText(kdecore.i18n(_fromUtf8("Prompt for unsaved changes")))
        self.showTrayCheckbox.setText(kdecore.i18n(_fromUtf8("Show a notification icon")))
        self.groupBox_2.setTitle(kdecore.i18n(_fromUtf8("Popup Menu")))
        self.allowKbNavCheckbox.setText(kdecore.i18n(_fromUtf8("Allow keyboard navigation of popup menu")))
        self.sortByUsageCheckbox.setText(kdecore.i18n(_fromUtf8("Sort menu items with most frequently used first")))
        self.groupBox_3.setTitle(kdecore.i18n(_fromUtf8("Expansions")))
        self.enableUndoCheckbox.setText(kdecore.i18n(_fromUtf8("Enable undo by pressing backspace")))

