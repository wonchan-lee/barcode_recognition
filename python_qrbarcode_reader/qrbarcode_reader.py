import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
from playsound import playsound

used_codes = []
data_list = []

try:
    f = open("qrbarcode_data.txt", "r", encoding="utf8")
    data_list = f.readlines()
except FileNotFoundError:
    pass
else:
    f.close()

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

for i in data_list:
    used_codes.append(i.rstrip('\n'))

while True:
    success, frame = cap.read()

    for code in pyzbar.decode(frame):
        x, y, w, h = code.rect
        my_code = code.data.decode('utf-8')
        frame=cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        frame=cv2.putText(frame, my_code, (x , y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        cv2.imwrite('qrbarcode_image.png', frame)
        if my_code not in used_codes:
            print("인식 성공 : ", my_code)
            playsound("qrbarcode_beep.mp3")
            used_codes.append(my_code)

            f2 = open("qrbarcode_data.txt", "a", encoding="utf8")
            f2.write(my_code+'\n')
            f2.close()
        elif my_code in used_codes:
            print("이미 인식된 코드 입니다.!!!")
            playsound("qrbarcode_beep.mp3")
        else:
            pass

    cv2.imshow('Camera - Lets scan barcode!', frame)

    cv2.waitKey(1)

