import subprocess

# Display resolution
EPD_WIDTH       = 800
EPD_HEIGHT      = 480

EPD_IMAGE_PATH = 'epd_image.png'

class EPD:
    """
    epd7in5 Dummy class.
    """
    def __init__(self):
        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT
        # windowプロセスを起動する
        self.winProc = subprocess.Popen(
            ['python', 'epd7in5_window.py']
            )

    def __del__(self):
        # windowプロセスを終了させる
        if self.winProc.poll:
            self.winProc.kill()

    def reset(self):
        pass

    def send_command(self, command):
        pass

    def send_data(self, data):
        pass

    def send_data2(self, data):
        pass

    def ReadBusy(self):
        pass
        
    def SetLut(self, lut_vcom, lut_ww, lut_bw, lut_wb, lut_bb):
        pass

    def init(self):
        return 0

    def getbuffer(self, image):
        img = image
        # 画像ファイルを保存する
        img.save(EPD_IMAGE_PATH)
        # dummyではbufは使わない
        buf = bytearray()
        return buf

    def display(self, image):
        pass

    def Clear(self):
        pass

    def sleep(self):
        pass

### END OF FILE ###

