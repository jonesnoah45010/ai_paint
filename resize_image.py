from PIL import Image

def resize_and_pad(image_path, output_path, target_size=(1024, 1024), is_mask=False):
    """
    Resizes an image to fit within a target size while maintaining aspect ratio
    and adding padding to make it a square.

    Args:
        image_path (str): Path to the input image.
        output_path (str): Path to save the resized and padded image.
        target_size (tuple): Target (width, height), default is (1024, 1024).
        is_mask (bool): If True, uses black padding (for masks). Otherwise, transparent.
    """
    # Open the image
    img = Image.open(image_path)

    # Resize while maintaining aspect ratio
    img.thumbnail((target_size[0], target_size[1]), Image.LANCZOS)

    # Create a new blank image with the target size
    if is_mask:
        new_img = Image.new("L", target_size, 0)  # Black background for masks
    else:
        new_img = Image.new("RGBA", target_size, (0, 0, 0, 0))  # Transparent background for source images

    # Calculate center position for pasting
    paste_x = (target_size[0] - img.size[0]) // 2
    paste_y = (target_size[1] - img.size[1]) // 2

    # Paste resized image onto the blank image
    new_img.paste(img, (paste_x, paste_y))

    # Save the new image
    new_img.save(output_path)
    print(f"Saved resized image: {output_path}")




def stretch_image(image_path, output_path, target_size=(1024, 1024), is_mask=False):
    """
    Stretches an image to exactly match the target dimensions.
    If is_mask=True, the output is converted to black and white (grayscale).

    Args:
        image_path (str): Path to the input image.
        output_path (str): Path to save the stretched image.
        target_size (tuple): Target (width, height), default is (1024, 1024).
        is_mask (bool): If True, converts the image to black and white (grayscale).
    """
    # Open the image
    img = Image.open(image_path)

    # Resize the image (stretching to fit the new size)
    stretched_img = img.resize(target_size, Image.LANCZOS)

    # If it's a mask, convert to black & white (grayscale)
    if is_mask:
        stretched_img = stretched_img.convert("L")  # Convert to grayscale (0-255)

    # Save the new stretched image
    stretched_img.save(output_path)
    print(f"Saved {'mask' if is_mask else 'image'}: {output_path}")




if __name__ == "__main__":

    stretch_image("shpwedms.png", "shpwedms_stretched.png")
    stretch_image("shpwedms_mask.png", "shpwedms_mask_stretched.png", is_mask=True) 
























