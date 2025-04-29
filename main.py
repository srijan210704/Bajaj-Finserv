from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from lab_test_extractor import process_images_in_folder

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Lab Report API"}

@app.post("/process-all-lab-tests")
async def process_all_lab_tests():
    """
    Process all images in the lbmaske folder and return extracted lab test data.
    """
    try:
        folder_path = "lbmaske"  # Folder where images are stored
        print(f"Processing images in folder: {folder_path}")  # Logging the folder path
        
        lab_tests = process_images_in_folder(folder_path)
        print(f"Extracted lab tests: {lab_tests}")  # Log extracted lab tests

        return JSONResponse(content={
            "is_success": True,
            "lab_tests": lab_tests
        })
    except Exception as e:
        print(f"Error: {str(e)}")  # Log any error that occurs
        return JSONResponse(content={
            "is_success": False,
            "error_message": str(e)
        })
