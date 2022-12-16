import easyocr
import cv2
from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'D:\\Progarms\\tesseract\\tesseract'

#-------------------------

def draw_blocks(img, blocks):    #отрисовка блок распознаного текста от easyocr
    for i in blocks:
        ax = int(i[0][0][0])
        ay = int(i[0][0][1])
        bx = int(i[0][2][0])
        by = int(i[0][2][1])
        img = cv2.rectangle(img, (ax, ay), (bx, by), (0, 0, 255), 1)
    return img

def draw_paragraphs(img, paragr):    #отрисовка блок распознаного текста от easyocr
    for i in paragr:
        ax = int(i[0][0][0])
        ay = int(i[0][0][1])
        bx = int(i[0][1][0])
        by = int(i[0][1][1])
        img = cv2.rectangle(img, (ax, ay), (bx, by), (255, 0, 0), 1)
    return img

#-------------------------

def recognize_block_of_text(start_file):      #распознавание текста
    reader = easyocr.Reader(["en"], gpu = True)
    return reader.readtext(start_file, paragraph = False)

#-------------------------

def recognize_paragraphes(blocks):
    paragraphs = []                    #структура: [[[XверхЛ, YверхЛ], [XнизП,YнизП]], "текст"]
    for i in blocks:
        hasElement = False             #флаг наличия параграфа
        for j in paragraphs:
            if i[0][0][1] <= j[0][1][1] and (
                ((i[0][0][0] <= j[0][0][0]) and (i[0][2][0] >= j[0][0][0])) or 
                (i[0][0][0]<= j[0][1][0] and i[0][2][0] >= j[0][1][0]) or 
                (i[0][0][0] >= j[0][0][0] and i[0][2][0] <= j[0][1][0])):

                j[0][1][1] = i[0][2][1]
                if i[0][0][0] < j[0][0][0]:
                    j[0][0][0] = i[0][0][0]
                if i[0][2][0] > j[0][1][0]:
                    j[0][1][0] = i[0][2][0]
                j[1] += i[1] + " "
                hasElement = True
                break
        if not hasElement:          #создаем новый параграф
            paragraphs.append([[ [i[0][0][0], i[0][0][1]] , [i[0][2][0], i[0][2][1]] ], i[1]])
    return paragraphs

#-------------------------

def recognize_text(img_file, drBlocks = False, drParagraphs=False):
    blc = recognize_block_of_text(img_file)
    prg = recognize_paragraphes(blc)
    if drBlocks:
        img = cv2.imread(img_file)
        img = draw_blocks(img, blc)
        cv2.imwrite(img_file, img)
    if drParagraphs:
        img = cv2.imread(img_file)
        img = draw_paragraphs(img, prg)
        cv2.imwrite(img_file, img)
    return prg

#-------------------------

def recognize_text_tesseract(img_file, paragrapth):
    im = Image.open(img_file)
    rs = im.crop((paragrapth[0][0][0], paragrapth[0][0][1], paragrapth[0][1][0], paragrapth[0][1][1]))
    rs.save("textRec.jpg")
    return pytesseract.image_to_string('textRec.jpg')

def just_tesseract(img_file):
    return pytesseract.image_to_string(img_file)