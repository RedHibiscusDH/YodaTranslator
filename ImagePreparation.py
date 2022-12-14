import cv2

def clear_contours(start_img, res_img):
    image = cv2.imread(start_img)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    minblack = 180
    maxblack = 255
    ret, thresh = cv2.threshold(image, minblack, maxblack, cv2.THRESH_BINARY_INV)
    thresh = cv2.GaussianBlur(thresh, (3, 3), 0)

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours( image, contours, contourIdx = -1, color = (255, 255, 255), thickness = -1, lineType = cv2.LINE_AA, hierarchy = hierarchy,  maxLevel = 2)
    cv2.drawContours( image, contours, contourIdx = -1, color = (255, 255, 255), thickness = 1, lineType = cv2.LINE_AA, hierarchy = hierarchy,  maxLevel = 2)
    ret, image = cv2.threshold(image, minblack, maxblack, cv2.THRESH_BINARY)
    cv2.imwrite(res_img, image)
