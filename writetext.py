from PIL import Image, ImageDraw, ImageFont

def text_watermark():
    with Image.open("bald.jpg").convert("RGBA") as base:

        # make a blank image for the text, initialized to transparent text color
        txt = Image.new("RGBA", base.size, (255, 255, 255, 0))

        # get a font
        fnt = ImageFont.truetype("C:/Windows/Fonts/ARIAL.TTF", 40)
        # get a drawing context
        d = ImageDraw.Draw(txt)
        #Watermark text = wm_text
        wm_text = input('Enter Watermark Text: ')
        for height in range(0,base.height,55):
            for width in range(0,base.width,100):
                # draw text, half opacity
                d.text((width,height), wm_text, font=fnt, fill=(255, 255, 255, 128))

        out = Image.alpha_composite(base, txt)

        out.show()

def apply_watermark_txt_ln(self):
    """Function used to apply a single instance of watermark text.
    This function overwrites the previous watermark."""
    self.image = self.original_img_copy
    self.configure_tkimg()
    # Create Blank Image for the text, text is initially transparent
    txt = Image.new(size=self.image.size,
                    mode='RGBA',
                    color=(255, 255, 255, 0))
    # Get TrueType font from Windows System
    font = ImageFont.truetype(font='C:/Windows/Fonts/ARIAL.TTF', size=self.watermark.font_size)
    # Get drawing context
    d = ImageDraw.Draw(txt)
    txtbox = ImageDraw.Draw(txt).textbbox(xy=(self.watermark.x,self.watermark.y),
                                          text=self.watermark.text,
                                          font=font)
    for height in range(0, self.image.height, (txtbox[2] - txtbox[0])):
        for width in range(0, self.image.width, (txtbox[3] - txtbox[1])):
            # draw text, half opacity
            d.text((width, height), self.text, font=font, fill=(255, 255, 255, 128))
    composite = Image.alpha_composite(self.image, txt)
    self.image = composite
    self.configure_tkimg()