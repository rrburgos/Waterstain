from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox, filedialog
from PIL import Image,ImageTk,ImageDraw,ImageFont

class ImageFrame(Label):

    def __init__(self,parent, watermark):

        super().__init__(parent) #Inheret from Label Class
        self.watermark = watermark #To store the watermark object that is passed
        self.image = Image.new(size=(640,480),mode="RGBA", color="gray")
        self.tkimg = ImageTk.PhotoImage(self.image)
        self.configure(image=self.tkimg)
        self.original_img_copy = None #Image copy is empty upon creation.


    def configure_tkimg(self):
        self.tkimg = ImageTk.PhotoImage(self.image)
        self.configure(image=self.tkimg)

    def apply_watermark_txt_ln(self):
        """Function used to apply a single instance of watermark text.
        This function overwrites the previous watermark."""
        self.image = self.original_img_copy
        self.configure_tkimg()
        #Create Blank Image for the text, text is initially transparent
        txt = Image.new(size=self.image.size,
                        mode='RGBA',
                        color=(255,255,255,0))
        #Get TrueType font from Windows System
        font = ImageFont.truetype(font='C:/Windows/Fonts/ARIAL.TTF',size=self.watermark.font_size)
        #Get drawing context
        d = ImageDraw.Draw(txt)
        d.text(xy=(self.watermark.x,self.watermark.y),
               text=self.watermark.text,
               font=font,
               fill=self.watermark.col_op)
        composite = Image.alpha_composite(self.image,txt)
        self.image = composite
        self.configure_tkimg()

    def apply_watermark_pattern(self):
        """Function used to apply simple pattern. Location is
        preset and can not be adjusted with arrows"""
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
        #Gets the Dimensions of the Text
        txt_box = ImageDraw.Draw(txt).textbbox(xy=(self.watermark.x, self.watermark.y),
                                              text=self.watermark.text,
                                              font=font)
        text_height = (txt_box[3] - txt_box[1])
        text_width = (txt_box[2] - txt_box[0])
        for height in range(0, self.image.height, text_height):
            for width in range(0, self.image.width, text_width):
                # draw text, half opacity
                d.text((width, height), self.watermark.text, font=font, fill=self.watermark.col_op)
        composite = Image.alpha_composite(self.image, txt)
        self.image = composite
        self.configure_tkimg()

    def load_image(self,path):
        try:
            #Open image and convert to RGBA
            img_loaded = Image.open(path).convert('RGBA')
            #Get the original dimensions of the loaded image
            original_width, original_height = img_loaded.size
            #Calculate the aspect ratio
            if original_width == 0:  # Avoid division by zero
                messagebox.showerror(message="Error: Image width is zero.",title='Invalid Image Size')
                return
            aspect_ratio = original_height / original_width
            #Resize the loaded image using the new dimensions
            self.image = img_loaded.resize((640, int(640 * aspect_ratio)), Image.Resampling.LANCZOS)
            #Create a Copy of the Original. ONLY done when load_image() is run.
            self.original_img_copy = self.image
            #Create the Tkinter PhotoImage and update the label
            self.configure_tkimg()

        except FileNotFoundError:
            messagebox.showerror(message=f"Error: File not found at {path}",title='FileNotFound')
        except Exception as e:
            messagebox.showerror(message=f"Error loading image: {e}", title="Load Error")

    def save(self):
        file_path = filedialog.asksaveasfilename(confirmoverwrite=True,
                                         defaultextension="png",
                                         filetypes=[("jpeg", ".jpg"),
                                                    ("png", ".png"),
                                                    ("bitmap", "bmp"),
                                                    ("gif", ".gif")])
        if file_path is not None:  # if dialog not closed with "cancel".
            self.image.save(fp=file_path)


class ApplyPatternWidget(Frame):
    def __init__(self,parent,ap_cbf):
        super().__init__(parent)
        self.description_label = Label(self,text='Applies a simple pattern.')
        self.description_label.grid(column=0,row=0)
        self.pattern_button = Button(self,text="Apply Pattern",command=ap_cbf,state='disabled')
        self.pattern_button.grid(column=0,row=1)

    def enable_apply(self):
        self.pattern_button.configure(state="normal")



class SlidersWidget(Frame):
    def __init__(self,parent,op_cbf,size_cbf):
        """Creates a frame with Opacity and Font Size Sliders"""
        super().__init__(parent)
        self.opacity_label = Label(self,text='Opacity')
        self.opacity_label.grid(column=0,row=0)
        self.opacity_slider = Scale(self,orient='horizontal',
                                    length=270,
                                    from_=0,
                                    to=255,
                                    command=op_cbf)
        self.opacity_slider.grid(column=0,row=1)
        self.size_label = Label(self,text='Font Size')
        self.size_label.grid(column=0,row=2)
        self.size_slider = Scale(self,orient='horizontal',
                                 length=270,
                                 from_=20,
                                 to=250,
                                 command=size_cbf)
        self.size_slider.grid(column=0,row=3)


class TextEntryWidget(Frame):
    def __init__(self,parent,apply_cbf,color_cbf):
        """Creates a frame with a Text Entry, Apply Button and Text Color Button.
        User Must provide function for apply and color buttons"""
        super().__init__(parent)

        self.label = Label(self,text="Text:",anchor="w")
        self.label.grid(column=0,row=0)
        self.mark_text = StringVar()
        self.txt_entry = Entry(self, textvariable=self.mark_text, width=25)
        self.txt_entry.grid(column=1, row=0)
        self.apply_button = Button(self,text="Apply",command=apply_cbf,state="disabled")
        self.apply_button.grid(column=2,row=0)
        self.color_button = Button(self,text="Color",command=color_cbf)
        self.color_button.grid(column=3,row=0)

    def enable_apply(self):
        self.apply_button.configure(state="normal")


class OpenSaveWidget(Frame):
    def __init__(self, parent, open_cbf, save_cbf):
        """Creates a frame with Open and Save Widgets
        User Must Provide an Open and Save Function"""
        super().__init__(parent)
        self.open_button = Button(self, text="Load", command=open_cbf)
        self.open_button.grid(column=0, row=0)
        self.save_button = Button(self, text="Save", command=save_cbf, state="disabled")
        self.save_button.grid(column=1, row=0)

    def enable_save(self):
        self.save_button.configure(state="normal")


class Watermark:
    def __init__(self,parent):
        """Creates a Watermark Object containing
        all the data for the Pillow ImageDraw Feature"""
        self.parent = parent
        self.font_size = 45
        self.opacity = 100
        self.color = (255,255,255)
        self.col_op = (self.color[0],self.color[1],self.color[2],self.opacity)
        #TODO Incorporate Rotation
        #self.angle = 0
        self.x = 50
        self.y = 50
        self.text = ""



