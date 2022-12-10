import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QLabel
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QPixmap

EPD_IMAGE_PATH = 'epd_image.png'

# Display resolution
EPD_WIDTH       = 800
EPD_HEIGHT      = 480

class EpdWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('epd7in5')      # ウィンドウのタイトル
        self.setGeometry(100, 100, EPD_WIDTH + 20, EPD_HEIGHT + 20)   # ウィンドウの位置と大きさ
        # ラベルの設定
        self.label = QLabel(self)
        self.label.move(10, 10)                             # ラベルの位置
        self.label.setFixedSize(EPD_WIDTH, EPD_HEIGHT)      # ラベルのサイズ指定
        # *ラベルのサイズをあらかじめ指定しておかないと、画像ファイルの表示がうまくいかない
        # タイマーの設定
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._run)
        self.timer.start(1000)  # 1秒間隔
    # タイマー
    def _run(self):
        # 画像ファイルが存在する場合
        if os.path.isfile(EPD_IMAGE_PATH):
            # 画像ファイル読み込み
            pix = QPixmap(EPD_IMAGE_PATH)
            # 画像ファイルをラベルに設定
            self.label.setPixmap(pix)

qAp = QApplication(sys.argv)
epdwindow = EpdWindow()
epdwindow.show()
qAp.exec()