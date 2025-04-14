import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw, ImageFont


class WatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Watermark App")
        self.root.geometry("400x300")

        # Variables
        self.image_path = None
        self.watermark_text = tk.StringVar(value="Your Watermark")

        # GUI Elements
        self.create_widgets()

    def create_widgets(self):
        # Upload Button
        upload_btn = tk.Button(self.root, text="Upload Image", command=self.upload_image)
        upload_btn.pack(pady=20)

        # Watermark Text Entry
        tk.Label(self.root, text="Watermark Text:").pack()
        text_entry = tk.Entry(self.root, textvariable=self.watermark_text, width=30)
        text_entry.pack(pady=10)

        # Apply Watermark Button
        apply_btn = tk.Button(self.root, text="Apply Watermark", command=self.apply_watermark)
        apply_btn.pack(pady=20)

        # Status Label
        self.status = tk.Label(self.root, text="")
        self.status.pack(pady=10)

    def upload_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp")]
        )
        if file_path:
            self.image_path = file_path
            self.status.config(text="Image uploaded successfully!")

    def apply_watermark(self):
        if not self.image_path:
            messagebox.showerror("Error", "Please upload an image first!")
            return

        try:
            # Open the image
            image = Image.open(self.image_path).convert("RGBA")

            # Create a transparent layer for the watermark
            watermark = Image.new("RGBA", image.size, (0, 0, 0, 0))
            draw = ImageDraw.Draw(watermark)

            # Set font (using default font, size 36)
            try:
                font = ImageFont.truetype("arial.ttf", 36)
            except:
                font = ImageFont.load_default()

            # Get text size
            text = self.watermark_text.get()
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            # Position the watermark (center of image)
            width, height = image.size
            x = (width - text_width) // 2
            y = (height - text_height) // 2

            # Draw the watermark (white text with semi-transparent black background)
            draw.rectangle(
                [x - 10, y - 10, x + text_width + 10, y + text_height + 10],
                fill=(0, 0, 0, 128)
            )
            draw.text((x, y), text, font=font, fill=(255, 255, 255, 255))

            # Combine original image with watermark
            watermarked = Image.alpha_composite(image, watermark)

            # Convert back to RGB and save
            watermarked_rgb = watermarked.convert("RGB")
            save_path = filedialog.asksaveasfilename(
                defaultextension=".jpg",
                filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png")]
            )
            if save_path:
                watermarked_rgb.save(save_path)
                self.status.config(text="Watermark applied and saved!")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = WatermarkApp(root)
    root.mainloop()