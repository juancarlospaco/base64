# -*- coding: utf-8 -*-
# PEP8:OK, LINT:OK, PY3:OK


#############################################################################
## This file may be used under the terms of the GNU General Public
## License version 2.0 or 3.0 as published by the Free Software Foundation
## and appearing in the file LICENSE.GPL included in the packaging of
## this file.  Please review the following information to ensure GNU
## General Public Licensing requirements will be met:
## http:#www.fsf.org/licensing/licenses/info/GPLv2.html and
## http:#www.gnu.org/copyleft/gpl.html.
##
## This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
## WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
#############################################################################


# metadata
" Base64 Data URI Encoder "
__version__ = ' 0.6 '
__license__ = ' GPL '
__author__ = ' juancarlospaco '
__email__ = ' juancarlospaco@ubuntu.com '
__url__ = ''
__date__ = ' 15/07/2013 '
__prj__ = ' base64 '
__docformat__ = 'html'
__source__ = ''
__full_licence__ = ''


# imports
from os import path, linesep
from base64 import b64encode
from mimetypes import guess_type
from sip import setapi

from PyQt4.QtGui import (QLabel, QCompleter, QDirModel, QPushButton, QWidget,
  QFileDialog, QDockWidget, QVBoxLayout, QSizePolicy, QCursor, QLineEdit, QIcon,
  QCheckBox, QDialog, QGraphicsDropShadowEffect, QColor, QApplication)

from PyQt4.QtCore import Qt, QDir

try:
    from PyKDE4.kdeui import KTextEdit as QPlainTextEdit
except ImportError:
    from PyQt4.QtGui import QPlainTextEdit  # lint:ok


from ninja_ide.gui.explorer.explorer_container import ExplorerContainer
from ninja_ide.core import plugin


# API 2
(setapi(a, 2) for a in ("QDate", "QDateTime", "QString", "QTime", "QUrl",
                        "QTextStream", "QVariant"))


# constans


###############################################################################


class Main(plugin.Plugin):
    " Main Class "
    def initialize(self, *args, **kwargs):
        " Init Main Class "
        ec = ExplorerContainer()
        super(Main, self).initialize(*args, **kwargs)

        self.infile = QLineEdit(path.expanduser("~"))
        self.infile.setPlaceholderText(' /full/path/to/file ')
        # directory auto completer
        self.completer = QCompleter(self)
        self.dirs = QDirModel(self)
        self.dirs.setFilter(QDir.AllEntries | QDir.NoDotAndDotDot)
        self.completer.setModel(self.dirs)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.infile.setCompleter(self.completer)

        self.open = QPushButton(QIcon.fromTheme("folder-open"), 'Open')
        self.open.setCursor(QCursor(Qt.PointingHandCursor))
        self.open.clicked.connect(lambda: self.infile.setText(str(
            QFileDialog.getOpenFileName(self.dock, "Open a File to Encode...",
            path.expanduser("~"),
            ';;'.join(['(*.{})'.format(e)
            for e in ['*', 'jpg', 'png', 'webp', 'svg', 'gif', 'webm']])))))
        self.chckbx1 = QCheckBox(' Use basic Caesar Cipher (ROT13)')
        self.chckbx1.setToolTip(' Use "string".decode("rot13") to Decipher ! ')
        self.chckbx2 = QCheckBox(' Use "data:type/subtype;base64,..."')
        self.chckbx2.setChecked(True)
        self.chckbx3 = QCheckBox(' Copy encoded output to Clipboard')

        self.output = QPlainTextEdit('''
        We can only see a short distance ahead,
        but we can see plenty there that needs to be done.
        - Alan Turing ''')
        self.output.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.button = QPushButton(QIcon.fromTheme("face-cool"), 'Encode BASE64')
        self.button.setCursor(QCursor(Qt.PointingHandCursor))
        self.button.setMinimumSize(100, 50)
        self.button.clicked.connect(self.run)

        def must_glow(widget_list):
            ' apply an glow effect to the widget '
            for glow, each_widget in enumerate(widget_list):
                try:
                    if each_widget.graphicsEffect() is None:
                        glow = QGraphicsDropShadowEffect(self)
                        glow.setOffset(0)
                        glow.setBlurRadius(99)
                        glow.setColor(QColor(99, 255, 255))
                        each_widget.setGraphicsEffect(glow)
                        glow.setEnabled(True)
                except:
                    pass

        must_glow((self.button, ))

        class TransientWidget(QWidget):
            ' persistant widget thingy '
            def __init__(self, widget_list):
                ' init sub class '
                super(TransientWidget, self).__init__()
                vbox = QVBoxLayout(self)
                for each_widget in widget_list:
                    vbox.addWidget(each_widget)

        tw = TransientWidget((QLabel('<i>Encode file as plain text string</i>'),
            QLabel(linesep + ' File to Encode: '), self.infile, self.open,
            self.chckbx2, self.chckbx3, self.chckbx1,
            QLabel(linesep + ' Base64 String Output: '), self.output,
            self.button,
        ))
        self.dock = QDockWidget()
        self.dock.setWindowTitle(__doc__)
        self.dock.setStyleSheet('QDockWidget::title{text-align: center;}')
        self.dock.setWidget(tw)
        ec.addTab(self.dock, "Base64")

    def run(self):
        ' run the encoding '
        mimetype = guess_type(str(self.infile.text()).strip(), strict=False)[0]
        _mime = mimetype if mimetype is not None else self.ask_mime()
        output = '"{}{}{}{}"'.format(
            'data:' if self.chckbx2.isChecked() is True else '',
            _mime if self.chckbx2.isChecked() is True else '',
            ';base64,' if self.chckbx2.isChecked() is True else '',
            b64encode(open(str(
            self.infile.text()).strip().replace('file:///', '/'), "rb").read()))
        if self.chckbx1.isChecked() is True:
            output = str(output).encode('rot13')
        if self.chckbx3.isChecked() is True:
            QApplication.clipboard().setText(output)
        self.output.setText(output)

    def ask_mime(self):
        ' ask user for mime type '
        dialog = QDialog(self.dock)
        textInput = QLineEdit('application/octet-stream')
        textInput.setPlaceholderText(' Write a MIME-Type Here ')
        ok = QPushButton(' O K ')
        ok.clicked.connect(dialog.close)
        ly = QVBoxLayout()
        [ly.addWidget(wdgt) for wdgt in (QLabel('<b>Auto MIME-Type Failed !'),
            QLabel('<i>Please write a MIME-Type for the File:'), textInput, ok)]
        dialog.setLayout(ly)
        dialog.exec_()
        return str(textInput.text()).strip().lower()


###############################################################################


if __name__ == "__main__":
    print(__doc__)
