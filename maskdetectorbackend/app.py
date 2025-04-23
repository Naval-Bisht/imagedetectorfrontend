from flask import Flask, request, jsonify, send_file
import os
import cv2
import numpy as np
import tensorflow as tf
from flask_cors import CORS
import uuid
import base64
import mysql.connector
from mysql.connector import Error
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Allow all origins
CORS(app, resources={r"/predict": {"origins": "http://localhost:3000"}})

# MySQL configuration
db_config = {
    'host': 'localhost',
    'user': 'naval',
    'password': 'password',  # Replace with your MySQL user password
    'database': 'image_processing'
}

def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

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
    connection = None
    try:
        # Check if an image file is included in the request
        if 'image_name' not in request.files:
            return jsonify({'status': 'error', 'message': 'No image file provided'}), 400

        file = request.files['image_name']
        if file.filename == '':
            return jsonify({'status': 'error', 'message': 'No file selected'}), 400

        # Create directories
        current_dir = os.getcwd()
        upload_dir = os.path.join(current_dir, 'uploads')
        output_dir = os.path.join(current_dir, 'output')
        os.makedirs(upload_dir, exist_ok=True)
        os.makedirs(output_dir, exist_ok=True)

        # Generate unique filenames
        unique_id = uuid.uuid4().hex
        original_filename = f"original_{unique_id}_{file.filename}"
        processed_filename = f"output_{unique_id}_{file.filename}"
        original_path = os.path.join(upload_dir, original_filename)
        output_path = os.path.join(output_dir, processed_filename)

        # Save the original image
        file.save(original_path)

        # Load model
        model_path = os.path.join(current_dir, 'unet_model.h5')
        model = tf.keras.models.load_model(model_path)

        # Preprocess and predict
        model_input = preprocess_image(original_path)
        prediction = model.predict(model_input, verbose=0)
        predicted_mask = prediction[0]
        predicted_mask = (predicted_mask * 255).astype(np.uint8).squeeze()

        # Save predicted mask
        cv2.imwrite(output_path, predicted_mask)

        # Read the predicted mask and encode as base64
        with open(output_path, 'rb') as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

        # Save metadata to MySQL
        connection = get_db_connection()
        if connection is None:
            return jsonify({'status': 'error', 'message': 'Database connection failed'}), 500

        cursor = connection.cursor()
        query = """
        INSERT INTO process (original_filename, processed_filename, time, status)
        VALUES (%s, %s, %s, %s)
        """
        values = (original_filename, processed_filename, datetime.now(), 'success')
        cursor.execute(query, values)
        connection.commit()
        record_id = cursor.lastrowid

        cursor.close()

        # Return success response with base64-encoded image and record ID
        return jsonify({
            'status': 'success',
            'record_id': record_id,
            'original_filename': original_filename,
            'output_filename': processed_filename,
            'image_base64': f'data:image/jpeg;base64,{encoded_image}'
        }), 200

    except Exception as e:
        # Log error to MySQL
        if connection is None:
            connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            query = """
            INSERT INTO process (original_filename, processed_filename, time, status)
            VALUES (%s, %s, %s, %s)
            """
            values = (original_filename if 'original_filename' in locals() else 'unknown',
                      processed_filename if 'processed_filename' in locals() else 'unknown',
                      datetime.now(), 'failed')
            cursor.execute(query, values)
            connection.commit()
            cursor.close()

        return jsonify({'status': 'error', 'message': str(e)}), 500

    finally:
        if connection and connection.is_connected():
            connection.close()

@app.route('/result', methods=['GET'])
def result():
    connection = None
    try:
        connection = get_db_connection()
        if connection is None:
            return jsonify({'status': 'error', 'message': 'Database connection failed'}), 500

        cursor = connection.cursor(dictionary=True)
        query = "SELECT id, original_filename, processed_filename, time, status FROM process"
        cursor.execute(query)
        records = cursor.fetchall()

        cursor.close()
        return jsonify({
            'status': 'success',
            'records': records
        }), 200

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

    finally:
        if connection and connection.is_connected():
            connection.close()

@app.route('/image/<int:id>', methods=['GET'])
def getImage(id):
    connection = None
    try:
        connection = get_db_connection()
        if connection is None:
            return jsonify({'status': 'error', 'message': 'Database connection failed'}), 500

        cursor = connection.cursor(dictionary=True)
        query = "SELECT original_filename, processed_filename FROM process WHERE id = %s"
        cursor.execute(query, (id,))
        record = cursor.fetchone()

        if not record:
            return jsonify({'status': 'error', 'message': 'Record not found'}), 404

        current_dir = os.getcwd()
        original_path = os.path.join(current_dir, 'uploads', record['original_filename'])
        processed_path = os.path.join(current_dir, 'output', record['processed_filename'])

        # Check if files exist
        if not os.path.exists(original_path) or not os.path.exists(processed_path):
            return jsonify({'status': 'error', 'message': 'Image files not found'}), 404

        # Read and encode images as base64
        with open(original_path, 'rb') as orig_file:
            original_base64 = base64.b64encode(orig_file.read()).decode('utf-8')
        with open(processed_path, 'rb') as proc_file:
            processed_base64 = base64.b64encode(proc_file.read()).decode('utf-8')

        cursor.close()
        return jsonify({
            'status': 'success',
            'original_image': f'data:image/jpeg;base64,{original_base64}',
            'processed_image': f'data:image/jpeg;base64,{processed_base64}',
            'original_filename': record['original_filename'],
            'processed_filename': record['processed_filename']
        }), 200

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

    finally:
        if connection and connection.is_connected():
            connection.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)