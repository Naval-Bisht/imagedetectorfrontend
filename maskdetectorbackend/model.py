# import os
# import cv2
# import numpy as np
# import tensorflow as tf
# from datetime import datetime
# import matplotlib.pyplot as plt
# 
# def preprocess_image(image_path, target_shape=(64, 64)):
    # """Preprocess a single image for U-Net prediction."""
    # img = cv2.imread(image_path)
    # if img is None:
        # raise ValueError(f"❌ Failed to load image: {image_path}")
#     
    # gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # resized_img = cv2.resize(gray_img, target_shape, interpolation=cv2.INTER_AREA)
#     
    # normalized_img = resized_img / 255.0
    # model_input = np.expand_dims(normalized_img, axis=(0, -1))  # Shape: (1, 64, 64, 1)
    # return model_input, resized_img
# 
# def predict_and_save(image_path, model_path, output_base_dir):
    # """Predict mask using U-Net model and save the output."""
    # # Create an "output" folder in the current directory (output_base_dir)
    # output_dir = os.path.join(output_base_dir, "output")
    # os.makedirs(output_dir, exist_ok=True)
# 
    # # Check if model file exists
    # if not os.path.exists(model_path):
        # raise FileNotFoundError(f"❌ Model file not found at: {model_path}")
# 
    # # Load model
    # try:
        # model = tf.keras.models.load_model(model_path)
        # print(f"✅ Loaded U-Net model from: {model_path}")
    # except Exception as e:
        # raise Exception(f"❌ Error loading model: {str(e)}")
# 
    # # Preprocess image
    # model_input, resized_img = preprocess_image(image_path)
# 
    # # Predict mask
    # prediction = model.predict(model_input, verbose=0)
    # predicted_mask = prediction[0]
    # predicted_mask = (predicted_mask * 255).astype(np.uint8).squeeze()
# 
    # # Save predicted mask as output.jpg in the "output" folder
    # output_path = os.path.join(output_dir, "output.jpg")
    # cv2.imwrite(output_path, predicted_mask)
    # print(f"✅ Predicted mask saved at: {output_path}")
# 
    # return output_path, resized_img, predicted_mask
# 
# if __name__ == "__main__":
    # # Get the image name from user input
    # image_name = input("Enter the image name (e.g., 000010_1.jpg): ")
# 
    # # Define paths
    # current_dir = os.getcwd()
    # image_path = os.path.join(current_dir,'images', image_name)  # Use the user input for the image path
    # model_path = os.path.join(current_dir, "unet_model.h5")  # Replace with your model file
    # output_base_dir = current_dir  # Current directory will be the base for output
# 
    # # Debug print
    # print(f"📂 Current Directory: {current_dir}")
    # print(f"🔍 Checking for model at: {model_path}")
    # print(f"📸 Checking for image at: {image_path}")
# 
    # # Optional: List files in current dir
    # print("📃 Files in current directory:", os.listdir(current_dir))
# 
    # try:
        # output_path, input_image, predicted_mask = predict_and_save(image_path, model_path, output_base_dir)
# 
        # # Display results
        # plt.figure(figsize=(8, 4))
        # plt.subplot(1, 2, 1)
        # plt.imshow(input_image, cmap='gray')
        # plt.title("Input Image")
        # plt.axis("off")
# 
# 
        # plt.subplot(1, 2, 2)
        # plt.imshow(predicted_mask, cmap='gray')
# 
#         
        # plt.title("Predicted Mask")
        # plt.axis("off")
# 
        # plt.tight_layout()
        # plt.show()
# 
    # except Exception as e:
        # print(f"🚫 Error: {str(e)}")
# 