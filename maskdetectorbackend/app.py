from flask import Flask, request, jsonify
import os
import cv2
import numpy as np
import tensorflow as tf

app = Flask(__name__)

def preprocess_image(image_path, target_shape=(64, 64)):
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Failed to load image: {image_path}")
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    resized_img = cv2.resize(gray_img, target_shape, interpolation=cv2.INTER_AREA)
    normalized_img = resized_img / 255.0
    model_input = np.expand_dims(normalized_img, axis=(0, -1))
    return model_input

@app.route('/predict', methods=['POST'])
def predict():
    image_name = request.json.get('image_name')
    current_dir = os.getcwd()
    image_path = os.path.join(current_dir, 'images', image_name)
    model_path = os.path.join(current_dir, 'unet_model.h5')
    output_dir = os.path.join(current_dir, 'output')
    os.makedirs(output_dir, exist_ok=True)

    try:
        model = tf.keras.models.load_model(model_path)
        model_input = preprocess_image(image_path)
        prediction = model.predict(model_input, verbose=0)
        predicted_mask = prediction[0]
        predicted_mask = (predicted_mask * 255).astype(np.uint8).squeeze()
        output_path = os.path.join(output_dir, 'output.jpg')
        cv2.imwrite(output_path, predicted_mask)
        return jsonify({'status': 'success', 'output': output_path})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)