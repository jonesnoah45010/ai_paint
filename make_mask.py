
import cv2
import numpy as np
from PIL import Image
import io



def generate_mask_in_memory(image_io, coordinates):
    """
    Creates a grayscale mask image with a specified editable region and converts it to a transparent PNG.
    
    Args:
        image_io (BytesIO): Input image as a BytesIO object.
        coordinates (tuple): Four (x, y) coordinates defining a rectangular region.
    
    Returns:
        BytesIO: Transparent mask image as a PNG in memory.
    """
    image = Image.open(image_io).convert('RGBA')
    image_np = np.array(image)
    height, width = image_np.shape[:2]
    
    # Create a black mask (all pixels initially set to 0)
    mask = np.zeros((height, width), dtype=np.uint8)
    
    # Define the editable region (white area)
    (x1, y1), (x2, y2), (x3, y3), (x4, y4) = coordinates
    pts = np.array([[x1, y1], [x2, y2], [x3, y3], [x4, y4]], dtype=np.int32)
    cv2.fillPoly(mask, [pts], 255)  # Fill the selected area with white (editable)
    
    # Convert the grayscale mask to an RGBA image with transparency
    transparent_mask = Image.new("RGBA", (width, height))
    for x in range(width):
        for y in range(height):
            pixel = mask[y, x]
            alpha = 0 if pixel >= 128 else 255  # White -> Transparent, Black -> Opaque
            transparent_mask.putpixel((x, y), (0, 0, 0, alpha))
    
    # Save to a BytesIO object
    img_io = io.BytesIO()
    transparent_mask.save(img_io, format='PNG')
    img_io.seek(0)
    return img_io





def generate_mask(image_path, output_path, coordinates):
    """
    Creates a grayscale mask image with a specified editable region and converts it to a transparent PNG.
    
    Args:
        image_path (str): Path to the source image (must be PNG).
        output_path (str): Path to save the final transparent mask.
        coordinates (tuple): Four (x, y) coordinates defining a rectangular region.
    """
    # Load the source image to get dimensions
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    height, width = image.shape[:2]

    # Create a black mask (all pixels initially set to 0)
    mask = np.zeros((height, width), dtype=np.uint8)

    # Define the editable region (white area)
    (x1, y1), (x2, y2), (x3, y3), (x4, y4) = coordinates
    pts = np.array([[x1, y1], [x2, y2], [x3, y3], [x4, y4]], dtype=np.int32)
    cv2.fillPoly(mask, [pts], 255)  # Fill the selected area with white (editable)

    # Convert the grayscale mask to an RGBA image with transparency
    transparent_mask = Image.new("RGBA", (width, height))
    for x in range(width):
        for y in range(height):
            pixel = mask[y, x]
            alpha = 0 if pixel >= 128 else 255  # White -> Transparent, Black -> Opaque
            transparent_mask.putpixel((x, y), (0, 0, 0, alpha))

    # Save the transparent mask as a PNG
    transparent_mask.save(output_path, "PNG")
    print(f"Transparent mask saved as: {output_path}")










if __name__ == "__main__":

    image_path = "shpwedms.png"  # Ensure this is a valid PNG image
    output_path = "shpwedms_mask.png"
    coordinates = [(420, 25), (620, 25), (620, 300), (420, 300)]  # Define the area to edit
    generate_mask(image_path, output_path, coordinates)

































