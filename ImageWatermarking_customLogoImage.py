from PIL import Image

def add_image_watermark(input_image_path, logo_image_path, output_image_path, position="bottom_right", scale=0.2, margin=10):
    # Open base image and logo
    base_image = Image.open(input_image_path).convert("RGBA")
    logo = Image.open(logo_image_path).convert("RGBA")

    # Resize logo to a fraction of the base image size
    base_width, base_height = base_image.size
    logo_width = int(base_width * scale)
    logo_ratio = logo_width / float(logo.size[0])
    logo_height = int(float(logo.size[1]) * float(logo_ratio))
    logo = logo.resize((logo_width, logo_height), Image.Resampling.LANCZOS)

    # Set position
    if position == "bottom_right":
        x = base_width - logo_width - margin
        y = base_height - logo_height - margin
    elif position == "top_left":
        x = margin
        y = margin
    elif position == "center":
        x = (base_width - logo_width) // 2
        y = (base_height - logo_height) // 2
    else:
        raise ValueError("Invalid position. Choose from 'bottom_right', 'top_left', 'center'.")

    # Paste logo (with transparency)
    base_image.paste(logo, (x, y), logo)

    # Save final image
    base_image.convert("RGB").save(output_image_path, "JPEG")
    print(f"Watermarked image saved as {output_image_path}")

# Example usage
add_image_watermark("image7.png", "logo.png", "output7.jpg", position="bottom_right", scale=0.15)
