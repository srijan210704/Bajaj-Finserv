import pytesseract
from PIL import Image
import os
import re

def extract_lab_tests(image_path):
    """
    Extract lab test details from the given image.
    """
    image = Image.open(image_path)
    
    # OCR to extract text from the image
    extracted_text = pytesseract.image_to_string(image)

    # Parse the extracted text for lab test details
    results = []
    lines = [line.strip() for line in extracted_text.split('\n') if line.strip()]

    # Regex pattern to extract: Test Name, Value, Reference Range
    pattern = re.compile(r"([A-Za-z\s]+)\s+([0-9.]+)\s+\(?([0-9.-]+\s*-?\s*[0-9.-]+)\)?")

    for line in lines:
        match = pattern.search(line)
        if match:
            test_name = match.group(1).strip()
            value = float(match.group(2).strip())
            ref_range = match.group(3).strip()

            try:
                # Parse reference range and compare the value
                lower, upper = map(float, ref_range.split('-'))
                lab_test_out_of_range = not (lower <= value <= upper)
            except:
                lower, upper = None, None
                lab_test_out_of_range = None

            # Store the extracted data
            results.append({
                "lab_test_name": test_name,
                "lab_test_value": value,
                "bio_reference_range": ref_range,
                "lab_test_out_of_range": lab_test_out_of_range
            })

    return results

def process_images_in_folder(folder_path):
    """
    Process all images in the provided folder and extract lab test details.
    """
    all_results = {}

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(folder_path, filename)
            lab_tests = extract_lab_tests(image_path)
            all_results[filename] = lab_tests

    return all_results
