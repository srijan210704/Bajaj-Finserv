import pytesseract
from PIL import Image
import os
import concurrent.futures


folder_path = r"C:\Users\Srijan\Downloads\lab_reports_samples\lbmaske"
 

def process_single_image(image_path):
    """
    Process a single image and extract text using Tesseract OCR.
    """
    image = Image.open(image_path)

    return pytesseract.image_to_string(image)

def process_all_images_in_folder_parallel(folder_path):
    """
    Process all images in the given folder using parallel processing.
    """
    results = {}


    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []


        for filename in os.listdir(folder_path):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):  # Process only image files
                image_path = os.path.join(folder_path, filename)

                futures.append(executor.submit(process_single_image, image_path))

        for i, future in enumerate(concurrent.futures.as_completed(futures)):
            filename = os.listdir(folder_path)[i]  
            results[filename] = future.result()  

    return results

# Call the function to process all images in the folder and get the extracted text
all_extracted_text = process_all_images_in_folder_parallel(folder_path)

# Print the extracted text for each image (or save to a file as needed)
for image_name, text in all_extracted_text.items():
    print(f"Extracted text from {image_name}:\n{text}\n")

# Optionally, save the extracted text to a JSON file
import json
with open("extracted_text.json", "w") as f:
    json.dump(all_extracted_text, f, indent=4)
