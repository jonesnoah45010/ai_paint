from openai import OpenAI
from PIL import Image
import requests
import os
import io
import base64


os.environ["OPENAI_API_KEY"] = "YOUR_KEY_HERE"


client = OpenAI()

def inpaint_image(image_path, mask_path, prompt, output_path="inpainted_image.png"):
    """
    Performs inpainting on an image using DALL-E 2.

    Args:
        image_path: Path to the original image.
        mask_path: Path to the mask image (transparent areas indicate regions to inpaint).
        prompt: Text description of what to generate in the masked area.
        output_path: Path to save the inpainted image.
    """
    try:
        response = client.images.edit(
            model="dall-e-2",
            image=open(image_path, "rb"),
            mask=open(mask_path, "rb"),
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        image_url = response.data[0].url

        inpainted_image = Image.open(requests.get(image_url, stream=True).raw)
        inpainted_image.save(output_path)
        print(f"Inpainted image saved to {output_path}")

    except Exception as e:
         print(f"An error occurred: {e}")






def inpaint_image_in_memory(image_bytes, mask_bytes, prompt):
    try:
        # Ensure BytesIO streams are rewound
        image_bytes.seek(0)
        mask_bytes.seek(0)

        # Add required 'name' attribute to BytesIO so OpenAI sees it as a PNG file
        image_bytes.name = "image.png"
        mask_bytes.name = "mask.png"

        response = client.images.edit(
            model="dall-e-2",
            image=image_bytes,
            mask=mask_bytes,
            prompt=prompt,
            n=1,
            size="1024x1024"
        )

        return response.data[0].url

    except Exception as e:
        print(f"An error occurred: {e}")
        return None






def generate_image_to_file(prompt, output_path="generated_image.png", size="1024x1024"):
    """
    Generates an image based on a prompt using DALL·E and saves it as a file.

    Args:
        prompt: Text description of the desired image.
        output_path: Path to save the generated image.
        size: Image size (default is "1024x1024").

    Returns:
        The file path of the saved image.
    """
    try:
        response = client.images.generate(
            model="dall-e-2",
            prompt=prompt,
            n=1,
            size=size
        )
        image_url = response.data[0].url

        # Download and save the image
        image = Image.open(requests.get(image_url, stream=True).raw)
        image.save(output_path)
        print(f"Generated image saved to {output_path}")
        return output_path

    except Exception as e:
        print(f"An error occurred: {e}")
        return None




def generate_image_in_memory(prompt, size="1024x1024"):
    """
    Generates an image based on a prompt using DALL·E and keeps it in memory.

    Args:
        prompt: Text description of the desired image.
        size: Image size (default is "1024x1024").

    Returns:
        A BytesIO object containing the generated image.
    """
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size=size
        )
        image_url = response.data[0].url

        # Download the image into a BytesIO object
        image_bytes = io.BytesIO()
        image = Image.open(requests.get(image_url, stream=True).raw)
        image.save(image_bytes, format="PNG")
        image_bytes.seek(0)  # Reset the stream position to the beginning

        return image_bytes

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
















if __name__ == "__main__":

    # inpaint_image("shpwedms.png", "shpwedms_mask.png", "give the frog a cowboy hat", "inpainted_image.png")

    # image_path = generate_image_to_file("realistic photo of a frog in overalls sprinting towards the camera")

    # Example usage
    image_path = "shpwedms.png"
    prompt = "Describe what is happening in this image."
    result = analyze_image_with_gpt4v(image_path, prompt)
    print(result)



















