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
__version__ = ' 0.1 '
__license__ = ' GPL '
__author__ = ' juancarlospaco '
__email__ = ' juancarlospaco@ubuntu.com '
__url__ = ''
__date__ = ' 15/05/2013 '
__prj__ = ' base64 '
__docformat__ = 'html'
__source__ = ''
__full_licence__ = ''


# imports
from os import path
from os import linesep
from base64 import b64encode
from mimetypes import guess_type

from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QCompleter
from PyQt4.QtGui import QDirModel
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QFileDialog
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QDockWidget
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QSizePolicy
from PyQt4.QtGui import QCursor
from PyQt4.QtGui import QLineEdit
from PyQt4.QtGui import QIcon
try:
    from PyKDE4.kdeui import KTextEdit as QPlainTextEdit
except ImportError:
    from PyQt4.QtGui import QPlainTextEdit  # lint:ok

from PyQt4.QtCore import Qt
from PyQt4.QtCore import QDir

from ninja_ide.gui.explorer.explorer_container import ExplorerContainer
from ninja_ide.core import plugin


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
            ';;'.join(['(*.%s)' % e for e in ['jpg', 'png', 'webp', '*']])))))

        self.output = QPlainTextEdit('''
        We can only see a short distance ahead,
        but we can see plenty there that needs to be done.
        - Alan Turing ''')
        self.output.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.button = QPushButton(QIcon.fromTheme("face-smile"), ' OK ! ')
        self.button.setCursor(QCursor(Qt.PointingHandCursor))
        self.button.clicked.connect(lambda: self.output.setText(str(''.join((
            '"data:',
            guess_type(str(self.infile.text()).strip(), strict=False)[0],
            ';base64,',
            b64encode(open(str(self.infile.text()).strip(), "rb").read()),
            '"')))))

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
            QLabel(linesep + ' Base64 String Output: '), self.output,
            self.button,
        ))
        self.dock = QDockWidget()
        self.dock.setFeatures(QDockWidget.DockWidgetFloatable |
                              QDockWidget.DockWidgetMovable)
        self.dock.setWindowTitle(__doc__)
        self.dock.setStyleSheet('QDockWidget::title{text-align: center;}')
        self.dock.setWidget(tw)
        ec.addTab(self.dock, "Base64")


###############################################################################


if __name__ == "__main__":
    print(__doc__)
