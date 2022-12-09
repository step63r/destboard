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
        imwidth, imheight = img.size
        if(imwidth == self.width and imheight == self.height):
            img = img.convert('1')
        elif(imwidth == self.height and imheight == self.width):
            # image has correct dimensions, but needs to be rotated
            img = img.rotate(90, expand=True).convert('1')
        else:
            logger.warning("Wrong image dimensions: must be " + str(self.width) + "x" + str(self.height))
            # return a blank buffer
            return [0x00] * (int(self.width/8) * self.height)

        buf = bytearray(img.tobytes('raw'))
        # The bytes need to be inverted, because in the PIL world 0=black and 1=white, but
        # in the e-paper world 0=white and 1=black.
        for i in range(len(buf)):
            buf[i] ^= 0xFF
        return buf

    def display(self, image):
        pass

    def Clear(self):
        pass

    def sleep(self):
        pass

### END OF FILE ###

