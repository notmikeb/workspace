# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from functools import partial
import sys


class Bu1(QWidget):
    def __init__(self, parent=None):
        super(Bu1, self).__init__(parent)
        # 水平盒式布局
        layout = QHBoxLayout()
        # 显示
        self.lbl = QLabel('no button is pressed')
        # 循环5个按钮
        for i in range(5):
            but = QPushButton(str(i)+"**")
            layout.addWidget(but)
            # 信号和槽连接
            but.clicked.connect(self.cliked)

            # 使用封装，lambda
        but = QPushButton('5**')
        layout.addWidget(but)
        but.clicked.connect(lambda: self.on_click('5'))
        # 使用个who变量，结果不正常，显示 False is pressed
        # but.clicked.connect(lambda who="5": self.on_click(who))

        # 使用封装，partial函数
        but = QPushButton('6**')
        layout.addWidget(but)
        but.clicked.connect(partial(self.on_click, '6'))

        layout.addWidget(self.lbl)
        # 设置布局
        self.setLayout(layout)

        # 传递额外参数

    def cliked(self):
        bu = self.sender()
        if isinstance(bu, QPushButton):
            self.lbl.setText('%s is pressed' % bu.text())
        else:
            self.lbl.setText('no effect')

    def on_click(self, n):
        self.lbl.setText('%s is pressed' % n)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    bu = Bu1()
    bu.show()
    app.exec_()