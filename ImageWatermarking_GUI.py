from tkinter import Tk, Label, Button, filedialog, Canvas, NW, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageTk

import os


class WatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Watermarker")
        self.root.geometry("800x600")

        self.input_path = None
        self.logo_path = None

        self.label = Label(root, text="Drag and drop an image file here", font=("Arial", 14))
        self.label.pack(pady=10)

        self.drop_area = Label(root, relief="groove", width=80, height=10)
        self.drop_area.pack(pady=10)
        self.drop_area.drop_target_register(DND_FILES)
        self.drop_area.dnd_bind('<<Drop>>', self.on_drop)

        self.logo_button = Button(root, text="Select Logo", command=self.select_logo)
        self.logo_button.pack(pady=10)

        self.watermark_button = Button(root, text="Apply Watermark", command=self.apply_watermark)
        self.watermark_button.pack(pady=10)

        self.preview_canvas = Canvas(root, width=600, height=300)
        self.preview_canvas.pack(pady=10)

    def on_drop(self, event):
        self.input_path = event.data.strip('{}')
        self.label.config(text=f"Selected: {os.path.basename(self.input_path)}")
        self.preview_image(self.input_path)

    def select_logo(self):
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg")])
        if path:
            self.logo_path = path
            messagebox.showinfo("Logo Selected", f"Logo: {os.path.basename(path)}")

    def apply_watermark(self):
        if not self.input_path or not self.logo_path:
            messagebox.showerror("Error", "Please select both base image and logo.")
            return

        output_path = os.path.join(os.path.dirname(self.input_path), "watermarked_output.jpg")
        self.add_image_watermark(self.input_path, self.logo_path, output_path)
        self.preview_image(output_path)
        messagebox.showinfo("Done", f"Watermarked image saved as {output_path}")

    def preview_image(self, path):
        img = Image.open(path)
        img.thumbnail((600, 300))
        img = ImageTk.PhotoImage(img)
        self.preview_canvas.delete("all")
        self.preview_canvas.create_image(0, 0, anchor=NW, image=img)
        self.preview_canvas.image = img  # Keep reference

    def add_image_watermark(self, input_image_path, logo_image_path, output_image_path, position="bottom_right", scale=0.2, margin=10):
        base_image = Image.open(input_image_path).convert("RGBA")
        logo = Image.open(logo_image_path).convert("RGBA")

        base_width, base_height = base_image.size
        logo_width = int(base_width * scale)
        logo_ratio = logo_width / float(logo.size[0])
        logo_height = int(float(logo.size[1]) * float(logo_ratio))
        logo = logo.resize((logo_width, logo_height), Image.Resampling.LANCZOS)

        if position == "bottom_right":
            x = base_width - logo_width - margin
            y = base_height - logo_height - margin
        else:
            x = margin
            y = margin

        base_image.paste(logo, (x, y), logo)
        base_image.convert("RGB").save(output_image_path, "JPEG")


if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = WatermarkApp(root)
    root.mainloop()
