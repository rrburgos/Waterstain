from tkinter import *
from tkinter import messagebox,filedialog
from tkinter import colorchooser
from PIL import Image, ImageTk
from widgetmanager import *


def y_up(event):
    if image_frame.original_img_copy:
        watermark.y -= 5
        image_frame.apply_watermark_txt_ln()

def y_down(event):
    if image_frame.original_img_copy:
        watermark.y += 5
        image_frame.apply_watermark_txt_ln()

def x_up(event):
    if image_frame.original_img_copy:
        watermark.x -= 5
        image_frame.apply_watermark_txt_ln()

def x_down(event):
    if image_frame.original_img_copy:
        watermark.x += 5
        image_frame.apply_watermark_txt_ln()

def col_op_update():
    """Updates the tuple with color and opacity value 'col_op'"""
    watermark.col_op = (watermark.color[0],
                        watermark.color[1],
                        watermark.color[2],
                        watermark.opacity)

def update_size(value):
    """Updates the font_size Variable in Watermark obj """
    watermark.font_size =  int(float(value))

def update_opacity(value):
    """Updates the opacity Variable in Watermark obj"""
    watermark.opacity = int(float(value))
    col_op_update()

def update_watermark_text(name,index,mode):
    """Updates Watermark Text when Entry is edited"""
    watermark.text = text_entry.mark_text.get()

def change_color():
    watermark.color = colorchooser.askcolor(title='Select Text Color')[0]
    col_op_update()

def select_image():
    """Function for Open button event. Prompts User to select image"""
    path = filedialog.askopenfilename(filetypes=[("jpeg", ".jpg .jpeg"),
                                                 ("png", ".png"),
                                                 ("bitmap", "bmp"),
                                                 ("gif", ".gif") ])
    if path != "":
        image_frame.load_image(path)

        window.geometry(f"1000x{int(640 * (image_frame.image.height / image_frame.image.width) + 45)}")
        save.enable_save()
        text_entry.enable_apply()
        pattern.enable_apply()

#------TK Window Setup---#
window = Tk()
window.title('WaterStain')
window.geometry("1000x525")
window.config(padx=5,pady=5)
#Stop Window Resize
window.resizable(False, False)

watermark = Watermark(window)

image_frame = ImageFrame(window, watermark)
image_frame.grid(column=0, row=0, rowspan=5, padx=5)

#-----Logo Widget-----#
logo = LogoWidget(window)
logo.grid(column=1,row=0)

#-----Pattern Widget-----#
pattern = ApplyPatternWidget(window,image_frame.apply_watermark_pattern)
pattern.grid(column=1,row=2)

#------Sliders Widget---#
sliders = SlidersWidget(window,op_cbf=update_opacity,size_cbf=update_size)
sliders.grid(column=1,row=3)
    #---Set Starting Position---#
sliders.size_slider.set(watermark.font_size)
sliders.opacity_slider.set(watermark.opacity)

#------Entry Widget----#
text_entry = TextEntryWidget(window, apply_cbf=image_frame.apply_watermark_txt_ln, color_cbf=change_color)
text_entry.grid(column=1, row=4)
text_entry.mark_text.trace_add('write', update_watermark_text) #Runs Update Watermark when Entry is Edited

#------Save Widget----#
save = OpenSaveWidget(window, select_image, image_frame.save)
save.grid(column=1, row=5)

#-----Arrow Key Binding-----#

window.bind("<Up>",y_up)
window.bind("<Down>",y_down)
window.bind("<Left>",x_up)
window.bind("<Right>",x_down)


#---Launch Window----#
window.mainloop()