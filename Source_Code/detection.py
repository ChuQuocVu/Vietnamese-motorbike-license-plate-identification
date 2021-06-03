from cv2 import cv2
import numpy as np
from train import get_model

my_model = get_model()
checkpoint = my_model.load_weights(r"E:\Pycharm\NhanDangBienSoXe\Model\weights--17--1.00.hdf5")

img = cv2.imread(r"E:\Pycharm\NhanDangBienSoXe\TestImage\0251_07090_b.jpg", 1)
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, img_thre = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)

contours, _ = cv2.findContours(img_thre, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    ratio = float(w)/float(h)
    area = w*h

    if 4000 <= area <= 5000:
        # cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0))
        img_crop = img[y:y+h, x:x+w]
        img_resize = cv2.resize(img_crop, (500, 500))
        # input_image = Image.open(r"E:\Pycharm\NhanDangBienSoXe\Cropped_Image\Bien1_crop.jpg")
        # img_enchange = ImageEnhance.Sharpness(input_image)
        # out = img_enchange.enhance(1.7)
        # out.save(r"E:\Pycharm\NhanDangBienSoXe\Cropped_Image\Bien1_crop_enchange.jpg")
        cv2.imwrite(r"E:\Pycharm\NhanDangBienSoXe\Cropped_Image\Bien2_crop.jpg", img_crop)













labels = ["0", "1", "A", "B", "C", "D", "E", "F",
          "G", "H", "K", "L", "2", "M", "N", "P",
          "R", "S", "T", "U", "V", "X", "Y", "3",
          "Z", "4", "5", "6", "7", "8", "9"]


roi = cv2.imread(r"E:\Pycharm\NhanDangBienSoXe\Cropped_Image\Bien2_crop.jpg", 1)
roi = cv2.resize(roi, dsize=(500, 500))
roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
ret, frame = cv2.threshold(roi_gray, 127, 255, cv2.THRESH_BINARY)
contours, _ = cv2.findContours(frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

h, w = roi.shape[:2]


def convert(candidates):
    first_line = []
    second_line = []

    for candidate, coordinate in candidates:
        if coordinate[0] < 100:
            first_line.append((candidate, coordinate[1]))
        elif coordinate[0] > 100:
            second_line.append((candidate, coordinate[1]))

    def take_second(s):
        return s[1]

    first_line = sorted(first_line, reverse=False, key=take_second)
    second_line = sorted(second_line, reverse=False, key=take_second)

    if len(second_line) == 0:
        license_plate = "".join([str(ele[0]) for ele in first_line])
    else:
        license_plate = "".join([str(ele[0]) for ele in first_line]) + "-" + "".join(
            [str(ele[0]) for ele in second_line])

    return license_plate, first_line


characters = []
coordinates = []
candidates = []
result_idx = []

for c in contours:
    x, y, w, h = cv2.boundingRect(c)

    aspect_ratio = w/float(h)
    solidity = cv2.contourArea(c)/float(w*h)

    if w < h and (0.1 <= aspect_ratio <= 0.5) and h >= 150:
        img = roi[y-20:y + h + 20, x-10:x + w]
        # cv2.rectangle(roi, (x - 15, y - 15), (x + w + 15, y + h + 15), (0, 255, 0))
        # cv2.imshow("Frame", img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        image_test = cv2.resize(img, dsize=(128, 128))
        image_test = np.expand_dims(image_test, axis=0)

        predict = my_model.predict(image_test)
        idx = np.argmax(predict[0])
        print("Number: ", labels[idx], predict[0])
        print(np.max(predict[0], axis=0))

        if np.max(predict[0]) >= 0.8:
            character = labels[idx]
            characters.append(character)
            result_idx.append(idx)
            coordinates.append((y, x))

for i in range(len(result_idx)):
    candidates.append((characters[i], coordinates[i]))


string, line = convert(candidates)

print("Biển số : ", string)


