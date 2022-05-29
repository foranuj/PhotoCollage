from fonts.FontSettings import TITLE_FONT_ECZAR

IMAGE_WITH_BLEED_SIZE = (2625, 3375)


class Options:
    def __init__(self, has_title: bool = True):
        self.border_w = 0.01
        self.border_c = "black"
        # Dimensions for Book trim size, US Letter, 8.5 x 11 inches at 300 ppi
        # Making the width the same, and height of right page is smaller than left by 100 pixels
        # for adding the label
        if not has_title:
            self.out_h = 3225
        else:
            _, h = TITLE_FONT_ECZAR.getsize("A")
            self.out_h = 3225 - h
        self.out_w = 2475
