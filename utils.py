import cv2
import pytesseract
import numpy as np



def fourPointsTransform(frame, vertices):
    """Extracts and transforms roi of frame defined by vertices into a rectangle."""
    # Get vertices of bounding box 
    vertices = np.asarray(vertices).astype(np.float32)
    outputSize = (100, 32)
    targetVertices = np.array([
        [0, outputSize[1] - 1],
        [0, 0],
        [outputSize[0] - 1, 0],
        [outputSize[0] - 1, outputSize[1] - 1]], dtype="float32")
    # Apply perspective transform
    rotationMatrix = cv2.getPerspectiveTransform(vertices, targetVertices)
    result = cv2.warpPerspective(frame, rotationMatrix, outputSize)
    return result


def preprocess_for_ocr(img, points):
    x1, y1, x2, y2 = map(int, points)

    img = img.copy().astype(np.uint8)

    img_g = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    img = img[y1-15:y2+15, x1-15:x2+15]

    
    textDetector = cv2.dnn_TextDetectionModel_DB("./resources/DB_TD500_resnet18.onnx")
    img = cv2.resize( img, (640, 640), interpolation = cv2.INTER_CUBIC)
    inputSize = (640, 640)

    binThresh = 0.3
    polyThresh = 0.5

    mean = (122.67891434, 116.66876762, 104.00698793)

    textDetector.setBinaryThreshold(binThresh).setPolygonThreshold(polyThresh)
    textDetector.setInputParams(1.0/255, inputSize, mean, True)
    boxes, _ = textDetector.detect(img) 
    img = fourPointsTransform(img, boxes[0])

    img = img[:, 5:]
    img = cv2.resize( img, (400,200), interpolation = cv2.INTER_CUBIC)
    gray =cv2.cvtColor(img , cv2.COLOR_RGB2GRAY)

    # blur
    blur = cv2.GaussianBlur(gray, (0,0), sigmaX=33, sigmaY=33)

    # divide
    divide = cv2.divide(gray, blur, scale=255)

    # otsu threshold
    thresh = cv2.threshold(divide, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]

    # apply morphology
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    kernel = np.ones((7,7),np.uint8)
    img = cv2.erode(morph,kernel,iterations = 1)
    img = cv2.resize( img, (120,30), interpolation = cv2.INTER_CUBIC)


    license_text = pytesseract.image_to_string(img, lang ='eng', config ='--oem 3 --psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') 

    print("TEXT:", license_text)
    return license_text, img    
