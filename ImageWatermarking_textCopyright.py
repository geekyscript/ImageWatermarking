from PIL import Image, ImageDraw, ImageFont


def add_watermark(input_image_path, output_image_path, watermark_text, position="bottom_right", opacity=128):
    # Load image
    base_image = Image.open(input_image_path).convert("RGBA")

    # Make a blank transparent image
    txt_layer = Image.new("RGBA", base_image.size, (255, 255, 255, 0))
    width, height = base_image.size

    # Choose font and size
    font_size = int(min(width, height) / 20)
    font = ImageFont.truetype("arial.ttf", font_size)

    # Create drawing context
    draw = ImageDraw.Draw(txt_layer)

    # Calculate text size
    bbox = draw.textbbox((0, 0), watermark_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Set position
    if position == "bottom_right":
        x = width - text_width - 20
        y = height - text_height - 20
    elif position == "top_left":
        x = 20
        y = 20
    elif position == "center":
        x = (width - text_width) // 2
        y = (height - text_height) // 2
    else:
        raise ValueError("Invalid position. Choose 'bottom_right', 'top_left', or 'center'.")

    # Add text to transparent layer
    draw.text((x, y), watermark_text, fill=(255, 255, 255, opacity), font=font)

    # Combine base image with watermark
    watermarked = Image.alpha_composite(base_image, txt_layer)

    # Save result
    watermarked.convert("RGB").save(output_image_path, "JPEG")
    print(f"Watermarked image saved as {output_image_path}")


# Example usage
add_watermark("image3.jpg", "output_textCopyright3.jpg", "©GS 2025", position="bottom_right", opacity=150)
