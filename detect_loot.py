import pytesseract
import pyautogui
from PIL import Image
import time
from imutils.object_detection import non_max_suppression
import numpy as np
import cv2
from decode_predictions import decode_predictions


def detect_loot():
    loot_key_config = r'--oem 1 --psm 8 --dpi 300'

    loop_count = 0
    while True:
        loop_count += 1
        # time.sleep(.5)
        print("checking" + ("." * (loop_count % 4)))

        # For loot crates or when looting bodies, the "LOOT" keyword appears in similar positions, but not exactly the same. Therefore, we capture a screenshot
        # of the region that contains both keywords, and check the regions individually. Since you can only be in one screen or the other, we can use this to
        # direct how we want to scan the items, as their locations differ when looting a crate or a body.
        loot_key_region_full = cv2.cvtColor(
            np.array(pyautogui.screenshot(region=(2114, 68, 144, 28))), cv2.COLOR_RGB2BGR)

        loot_key_region_crate = loot_key_region_full[0:28, -
                                                     77:loot_key_region_full.shape[1]]
        loot_key_region_body = loot_key_region_full[0:28, 0:77]

        # print("saving images")
        # cv2.imwrite("loot_key_region_crate.png", loot_key_region_crate)
        # cv2.imwrite("loot_key_region_body.png", loot_key_region_body)

        # time.sleep(5)

        if pytesseract.image_to_string(loot_key_region_body, config=loot_key_config) == "LOOT":
            print("looting a body, checking prices")

        if pytesseract.image_to_string(loot_key_region_crate, config=loot_key_config) == "LOOT":
            print("looting a crate, checking prices")

            # 640 x 640 screenshot saved to memory

            items = get_crate_loot(cv2.cvtColor(
                np.array(pyautogui.screenshot(
                    region=(2126, 104, 640, 640))), cv2.COLOR_RGB2BGR))

            print(items)

            # item_list=list(filter(('').__ne__, items.split('\n')))
            # print(item_list)

            # for item in item_list:
            #     if item in prices:
            #         print("%s: %d rubles" % (item, prices[item]))


def get_crate_loot(loot_image):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    east = 'frozen_east_text_detection.pb'
    min_confidence = 0.5

    loot_screen_config = r'--psm 11 --dpi 300'

    img = loot_image
    orig = img.copy()

    (origH, origW) = img.shape[:2]

    # percent by which the image is resized
    # scale_percent = 100

    # # calculate the 50 percent of original dimensions
    # width = int(img.shape[1] * scale_percent / 100)
    # height = int(img.shape[0] * scale_percent / 100)

    # # dsize
    # dsize = (width, height)

    # # resize image
    # img = cv2.resize(img, dsize)

    (H, W) = img.shape[:2]

    # The following two layer need to pulled from EAST model for achieving this.
    layerNames = [
        "feature_fusion/Conv_7/Sigmoid",
        "feature_fusion/concat_3"]

    # load the pre-trained EAST model for text detection
    net = cv2.dnn.readNet(east)

    # construct a blob from the image and then perform a forward pass of
    # the model to obtain the two output layer sets
    blob = cv2.dnn.blobFromImage(img, 1.0, (W, H),
                                 (123.68, 116.78, 103.94), swapRB=True, crop=False)
    net.setInput(blob)
    (scores, geometry) = net.forward(layerNames)

    (rects, confidences) = decode_predictions(scores, geometry)
    boxes = non_max_suppression(np.array(rects), probs=confidences)

    # initialize the list of results
    results = []

    # loop over the bounding boxes, extracting the item names
    for (startX, startY, endX, endY) in boxes:
        # in order to obtain a better OCR of the text we can potentially
        # apply a bit of padding surrounding the bounding box -- here we
        # are computing the deltas in both the x and y directions
        dX = int((endX - startX) * 0)
        dY = int((endY - startY) * .1)
        # apply padding to each side of the bounding box, respectively
        startX = max(0, startX - dX)
        startY = max(0, startY - dY)
        endX = min(origW, endX + (dX * 2))
        endY = min(origH, endY + (dY * 2))

        # extract the actual padded ROI
        roi = orig[startY:endY, startX:endX]

        # in order to apply Tesseract v4 to OCR text we must supply
        # (1) a language, (2) an OEM flag of 4, indicating that the we
        # wish to use the LSTM neural net model for OCR, and finally
        # (3) an OEM value, in this case, 7 which implies that we are
        # treating the ROI as a single line of text
        config = ("-l eng --oem 1 --psm 13 --dpi 500")
        text = pytesseract.image_to_string(roi, config=config)

        # Append item name to results
        results.append(((startX, startY, endX, endY), text))

    # sort the results bounding box coordinates from top to bottom
    results = sorted(results, key=lambda r: r[0][1])
    # loop over the results
    for ((startX, startY, endX, endY), text) in results:
        # display the text OCR'd by Tesseract
        print("OCR TEXT")
        print("========")
        print("{}\n".format(text))
        # strip out non-ASCII text so we can draw the text on the image
        # using OpenCV, then draw the text and a bounding box surrounding
        # the text region of the input image
        text = "".join([c if ord(c) < 128 else "" for c in text]).strip()
        output = orig.copy()
        cv2.rectangle(output, (startX, startY), (endX, endY),
                      (0, 0, 255), 2)
        cv2.putText(output, text, (startX, startY - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
        # show the output image
        cv2.imshow("Text Detection", output)
        cv2.waitKey(0)

    return results
