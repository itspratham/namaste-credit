import os
import io
from PIL import Image
import pytesseract
from wand.image import Image as wi
import pandas as pd

pdf_path = "51.pdf"


def Get_text_from_image(pdf_path):
    pdf = wi(filename=pdf_path, resolution=300)
    pdfImg = pdf.convert('jpeg')
    imgBlobs = []
    extracted_text = []
    for img in pdfImg.sequence:
        page = wi(image=img)
        imgBlobs.append(page.make_blob('jpeg'))

    for imgBlob in imgBlobs:
        im = Image.open(io.BytesIO(imgBlob))
        text = pytesseract.image_to_string(im, lang='eng')
        extracted_text.append(text)

    return extracted_text


trr = Get_text_from_image(pdf_path)
d = ''.join(trr)
f = open('51.txt', "w")

f.write(d)

g = open("51.txt", "r")
import re

pattern1 = re.compile(r'(\d+/\d+/\d+).*')

a_list = []
d = g.readlines()
for i in d:
    dd = []
    if pattern1.match(i):
        f = i.split(' ')
        a_list.append(f)

special_char = [":", "]", "{", "_", "|"]

for i in range(len(a_list)):
    for g in range(len(a_list[i])):
        if a_list[i][g] in special_char:
            a_list[i][g] = ""

b_list = []
for i in range(len(a_list)):
    if len(a_list[i]) == 4:
        d = [a_list[i][0].strip(), ' '.join(a_list[i][1:-2]), '', a_list[i][-1].strip()]
        b_list.append(d)
    elif len(a_list[i]) > 3:
        d = [a_list[i][0].strip(), ' '.join(a_list[i][1:-2]).lstrip(), a_list[i][-2].strip(), a_list[i][-1].strip()]
        b_list.append(d)

df = pd.DataFrame(b_list, columns=["Date", "Description", "Credit/Debit", "Balance"])

f = df.to_csv("51.csv")
