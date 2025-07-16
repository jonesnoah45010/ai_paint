from flask import Flask, render_template, jsonify, request, send_file
from dalle_api import inpaint_image_in_memory, generate_image_in_memory
from make_mask import generate_mask_in_memory
import io
import json
from PIL import Image
import requests



app = Flask(__name__)




@app.route('/', methods=['GET', 'POST'])
def index():
	return render_template("index.html")



@app.route('/paint', methods=['GET', 'POST'])
def paint():
	return render_template("paint.html")












# curl -X POST "http://127.0.0.1:5002/inpaint" \
#      -H "Content-Type: multipart/form-data" \
#      -F "image=@/path/to/your/image.png" \
#      -F 'coordinates=[[100,100],[200,100],[200,200],[100,200]]' \
#      -F "prompt=A beautiful sunset over the ocean" \
#      --output output.png






@app.route('/inpaint', methods=['POST'])
def inpaint():
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400

        image_file = request.files['image']
        image = Image.open(image_file.stream).convert("RGBA")

        # Convert to PNG and store in BytesIO
        image_png_bytes = io.BytesIO()
        image.save(image_png_bytes, format="PNG")
        image_png_bytes.seek(0)
        image_png_bytes.name = "image.png"  # Crucial for OpenAI API

        # Extract form data
        coordinates_str = request.form.get("coordinates")
        prompt = request.form.get("prompt")
        print(coordinates_str)
        print(prompt)

        if not coordinates_str or not prompt:
            return jsonify({'error': 'Missing coordinates or prompt'}), 400

        try:
            coordinates = json.loads(coordinates_str)
        except json.JSONDecodeError:
            return jsonify({'error': 'Invalid JSON format for coordinates'}), 400

        if not isinstance(coordinates, list) or len(coordinates) != 4:
            return jsonify({'error': 'Invalid coordinates format. Must be a list of four (x, y) tuples'}), 400

        # Generate mask from the PNG image
        mask_bytes = generate_mask_in_memory(image_png_bytes, coordinates)
        mask_bytes.name = "mask.png"  # Crucial for OpenAI API

        # Perform inpainting and get the image URL
        image_url = inpaint_image_in_memory(image_png_bytes, mask_bytes, prompt)
        
        if not image_url:
            return jsonify({'error': 'Failed to generate inpainted image'}), 500

        # Download the image from OpenAI’s response
        response = requests.get(image_url, stream=True)
        if response.status_code != 200:
            return jsonify({'error': 'Failed to download inpainted image'}), 500

        inpainted_image = Image.open(response.raw)

        # Send final image back
        output_bytes = io.BytesIO()
        inpainted_image.save(output_bytes, format="PNG")
        output_bytes.seek(0)
        return send_file(output_bytes, mimetype="image/png")

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'error': str(e)}), 500







# curl -X POST "http://127.0.0.1:5002/generate_image" \
#      -H "Content-Type: application/json" \
#      -d '{"prompt": "A futuristic cityscape at sunset"}' \
#      --output generated_image.png



@app.route("/generate_image", methods=["POST"])
def generate_image():
    """
    API endpoint to generate an image based on a user-provided prompt.
    Expects a JSON payload with a "prompt" key.

    Returns:
        The generated image as a PNG file.
    """
    try:
        data = request.json
        if not data or "prompt" not in data:
            return jsonify({"error": "Missing 'prompt' parameter"}), 400

        prompt = data["prompt"]
        print(prompt)
        size = data.get("size", "1024x1024")  # Optional size parameter

        image_bytes = generate_image_in_memory(prompt, size)
        if not image_bytes:
            return jsonify({"error": "Image generation failed"}), 500

        return send_file(image_bytes, mimetype="image/png")

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500






if __name__ == '__main__':
	# app.run(debug=True,  host='0.0.0.0', port = 5002)
    app.run(debug=False,  host='0.0.0.0', port = 8080)







