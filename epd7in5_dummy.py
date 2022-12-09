import logging

# Display resolution
EPD_WIDTH       = 800
EPD_HEIGHT      = 480

logger = logging.getLogger(__name__)

class EPD:
    """
    epd7in5 Dummy class.
    """
    def __init__(self):
        self.width = EPD_WIDTH
        self.height = EPD_HEIGHT

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
        img.save("epd_image.png")
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

