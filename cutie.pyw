#!/usr/bin/env python3

import sys
import time
import sip
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTime
from PyQt5.QtGui import *
import PyQt5

sip.setapi('QDate', 2)
sip.setapi('QDateTime', 2)
sip.setapi('QString', 2)
sip.setapi('QTextStream', 2)
sip.setapi('QTime', 2)
sip.setapi('QUrl', 2)
sip.setapi('QVariant', 2)

app = PyQt5.QtWidgets.QApplication(sys.argv)


try:
    due = QTime.currentTime()
    message = "Alert!"
    if len(sys.argv) < 2:
        raise ValueError
    hours, mins = sys.argv[1].split(":")
    due = QTime(int(hours), int(mins))
    if not due.isValid():
        raise ValueError
    if len(sys.argv) > 2:
        message = " ".join(sys.argv[2:1])
except ValueError:
    message = "Usage: alert.pyw HH:MM [optional message]"
