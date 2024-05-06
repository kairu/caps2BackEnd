from paddleocr import PaddleOCR
import cv2
# from PIL import Image
import numpy as np

def process_ocr(img_path, soa_id, amount):
    # Load the image
    image = cv2.imread(img_path)

    # Preprocess the image
    preprocessed_images = preprocess_image(image)

    # Perform OCR on original and preprocessed images
    ocr_results = perform_ocr_on_images(img_path, preprocessed_images)

    # Calculate average confidence score for each preprocessing technique
    confidences_dict = calculate_confidences(ocr_results)

    # Sort the dictionary of confidence scores in descending order
    sorted_confidences = sorted(confidences_dict.items(), key=lambda x: x[1], reverse=True)

    # Get the best OCR result based on the highest confidence score
    best_result = get_best_ocr_result(ocr_results, sorted_confidences)

    # Check if all header texts are found in the best OCR result
    all_headers_found = check_header_texts(best_result)

    # Process the best OCR result if all header texts are found
    if all_headers_found:
        return process_best_ocr_result(best_result, soa_id, amount)
    else:
        return False

def preprocess_image(image):
    # Convert to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian Blur
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

    # Apply Median Filter
    median_blurred_image = cv2.medianBlur(gray_image, 5)

    # Apply Bilateral Filter
    bilateral_filtered_image = cv2.bilateralFilter(gray_image, 9, 75, 75)

    # Image Binarization using Adaptive Thresholding
    binary_image = cv2.adaptiveThreshold(blurred_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    deskewed_image = deskew(binary_image)

    return [gray_image, blurred_image, median_blurred_image, bilateral_filtered_image, binary_image, deskewed_image]

def perform_ocr_on_images(img_path, preprocessed_images):
    ocr_results = []

    # Perform OCR on original image
    original_texts, original_confidences, original_result = perform_ocr(img_path)
    ocr_results.append({"name": "Original", "texts": original_texts, "confidences": original_confidences, "result": original_result})

    # Perform OCR on preprocessed images
    for image, name in zip(preprocessed_images, ["Grayscale", "Gaussian Blur", "Median Blur", "Bilateral Filter", "Binary Image", "Deskewed Image"]):
        texts, confidences, result = perform_ocr(image)
        ocr_results.append({"name": name, "texts": texts, "confidences": confidences, "result": result})

    return ocr_results

def calculate_confidences(ocr_results):
    confidences_dict = {}
    for result in ocr_results:
        name = result["name"]
        confidences = result["confidences"]
        confidences_dict[name] = sum(confidences) / len(confidences)
    return confidences_dict

def get_best_ocr_result(ocr_results, sorted_confidences):
    max_confidence_method, _ = sorted_confidences[0]
    for result in ocr_results:
        if result["name"] == max_confidence_method:
            return result["result"]

def check_header_texts(best_result):
    header_texts = ["Avida Towers", "New Manila", "AMOUNT", "O.R.", "Bonny Serrano Ave.", "atnmcc@gmail.com", "billing.atnmcc@gmail.com", "007-354-043-00000", "7799-2395", "0999-227-9193"]
    header_texts = [text.lower() for text in header_texts]

    all_headers_found = 0

    for idx in range(len(best_result)):
        res = best_result[idx]
        for line in res:
            text = line[1][0].lower()
            for header_text in header_texts:
                if header_text in text:
                    all_headers_found += 1
    
    return all_headers_found == len(header_texts)

def process_best_ocr_result(best_result, soa_id, amount):
    soa_id_found = False
    amount_found = False
    for idx in range(len(best_result)):
        res = best_result[idx]
        for line in res:
            text = line[1][0]
            if soa_id in text:
                soa_id_found = True
            if amount in text:
                amount_found = True
            
    if soa_id_found and amount_found:
        return True
    else:
        return False

# Skew Correction
def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

# Define a function to perform OCR on an image and return the detected text
def perform_ocr(image):
    if 'ocr' not in globals():
        global ocr
        ocr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=False)
    result = ocr.ocr(image, cls=True)
    texts = []
    confidences = []
    for line in result:
        text_line = ''
        line_confidences = []
        for word in line:
            text_line += word[1][0]
            line_confidences.append(word[1][1])
        texts.append(text_line)
        confidences.append(sum(line_confidences) / len(line_confidences))
    return texts, confidences, result
