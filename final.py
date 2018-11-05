import math
import numpy as np
from tkinter import *
from tkinter import Tk
import cv2
import pygame


k = cv2.waitKey(20)
root = Tk()


def main():
    pygame.init()
    font = cv2.FONT_HERSHEY_TRIPLEX
    print_color = (255, 0, 0)
    print_position = (50, 50)
    camera = cv2.VideoCapture(0)

    while camera.isOpened():

        _, img = camera.read()
        value = (35, 35)
        ing_Select = img[50:280, 50:280]
        grey = cv2.cvtColor(ing_Select, cv2.COLOR_BGR2GRAY)
        capture_image = cv2.imread(" ", 0)
        cv2.rectangle(img, (50, 50), (280, 280), (128, 0, 0), 1)
        blurred = cv2.GaussianBlur(grey, value, 0)
        cv_thresh = cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
        _, threshold = cv2.threshold(blurred, 127, 255, cv_thresh)
        _, threshold_1 = cv2.threshold(capture_image, 127, 255, cv_thresh)
        val, contours, hierarchy = cv2.findContours(threshold.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        counter = max(contours, key=lambda p1: cv2.contourArea(p1))
        p1, p2, dim_1, hei_1 = cv2.boundingRect(counter)
        border = (p1 + dim_1, p2 + hei_1)
        cv2.rectangle(ing_Select, (p1, p2), border, (255, 0, 0), 1)
        shape_border = cv2.convexHull(counter)
        shape_drawing = np.zeros(ing_Select.shape, np.uint8)

        cv2.drawContours(shape_drawing, [counter], 0, (255, 255, 0), 0)
        cv2.drawContours(shape_drawing, [shape_border], 0, (0, 255, 255), 0)

        shape_border = cv2.convexHull(counter, returnPoints=False)
        defects = cv2.convexityDefects(counter, shape_border)

        count_defects = 0
        cv2.drawContours(threshold, contours, -1, (255, 0, 0), 4)
        try:
            for i in range(defects.shape[0]):
                val_1, val_2, val_3, d = defects[i, 0]
                initial_point = tuple(counter[val_1][0])
                final_point = tuple(counter[val_2][0])
                dist_point = tuple(counter[val_3][0])

                a = math.sqrt(
                    int(pow(final_point[0] - initial_point[0], 2)) + int(pow((final_point[1] - initial_point[1]), 2)))
                b = math.sqrt(
                    int(pow((dist_point[0] - initial_point[0]), 2)) + int(pow((dist_point[1] - initial_point[1]), 2)))
                c = math.sqrt(
                    int(pow((final_point[0] - dist_point[0]), 2)) + int(pow((final_point[1] - dist_point[1]), 2)))
                ang = ((int(pow(b, 2)) + (int(pow(c, 2))) - int(pow(a, 2))) / (2 * b * c))
                angle = math.acos(ang)
                angle = angle * 60
                cv2.circle(ing_Select, dist_point, 4, [0, 0, 255], -2)
                if angle <= 90:
                    count_defects += 1
                cv2.line(ing_Select, initial_point, final_point, [255, 255, 0], 3)
        except AttributeError:
            pass
        perimeter = cv2.arcLength(counter, True)
        area = cv2.contourArea(counter)

        (p1, p2), radius = cv2.minEnclosingCircle(counter)
        center = (int(p1), int(p2))
        radius = int(radius)
        cv2.circle(ing_Select, center, radius, (255, 0, 0), 1)

        perimerter = math.pi * radius * radius

        convee_hull = cv2.convexHull(counter)
        convex_hullare = cv2.contourArea(convee_hull)
        thickness = float(area) / convex_hullare

        AR = float(dim_1) / hei_1

        (p1, p2), (MA, ma), angle_defects = cv2.fitEllipse(counter)
        if perimerter - area < 5000:
            cv2.putText(img, "Predicted Letter is:   A", print_position, font, 1, print_color, 2, cv2.LINE_AA)
        elif count_defects == 1:
            if angle_defects < 10:
                cv2.putText(img, "Predicted Letter is:   V", print_position, font, 1, print_color, 2, cv2.LINE_AA)
            elif 20 < angle_defects < 35:
                cv2.putText(img, "Predicted Letter is:    L", print_position, font, 1, print_color, 2, cv2.LINE_AA)
            elif 40 < angle_defects < 66:
                cv2.putText(img, "Predicted Letter is:    C", print_position, font, 1, print_color, 2, cv2.LINE_AA)
            else:
                cv2.putText(img, "Predicted Letter is:   Y", print_position, font, 1, print_color, 2, cv2.LINE_AA)
        elif count_defects == 2:
            if angle_defects < 100:
                cv2.putText(img, "Predicted Letter is:   W", print_position, font, 1, print_color, 2, cv2.LINE_AA)
            else:
                cv2.putText(img, "Predicted Letter is:   F", print_position, font, 1, print_color, 2, cv2.LINE_AA)
        elif count_defects == 4:
            cv2.putText(img, "ASL Recognition", print_position, font, 1, print_color, 2, cv2.LINE_AA)
        else:
            if area > 12000:
                cv2.putText(img, "Predicted Letter is:   B", print_position, font, 1, print_color, 2, cv2.LINE_AA)
            else:
                if thickness < 0.85:
                    if AR < 1:
                        if angle_defects < 20:
                            cv2.putText(img, "Predicted Letter is:   D", print_position, font, 1, print_color, 2,
                                        cv2.LINE_AA)
                        elif angle_defects < 168:
                            cv2.putText(img, "Predicted Letter is:   J", print_position, font, 1, print_color, 2,
                                        cv2.LINE_AA)
                        elif 169 < angle_defects < 180:
                            cv2.putText(img, "Predicted Letter is:   I", print_position, font, 1, print_color, 2,
                                        cv2.LINE_AA)
                    elif AR > 1.01:
                        cv2.putText(img, "Predicted Letter is:   Y", print_position, font, 1, print_color, 2,
                                    cv2.LINE_AA)
                else:
                    if 30 < angle_defects < 100:
                        cv2.putText(img, "Predicted Letter is:   H", print_position, font, 1, print_color, 2,
                                    cv2.LINE_AA)
                    elif angle_defects > 120:
                        cv2.putText(img, "Predicted Letter is:   I", print_position, font, 1, print_color, 2,
                                    cv2.LINE_AA)
                    else:
                        cv2.putText(img, "Predicted Letter is:   U", print_position, font, 1, print_color, 2,
                                    cv2.LINE_AA)
        cv2.imshow('Predicted Gesture: ', img)
        cv2.imshow('Binary Image', threshold)
        cv2.imshow('Expected Defects:', ing_Select)
        cv2.imshow('Defined Contours: ', shape_drawing)

        # print ('Radius: ', math.pi * (int(pow(radius, 2))), "Area: ", area)
        # print ("Perimeter of contour: ", perimeter)
        # print ("The aspect ratio is:", AR)
        # print ("Convexity Defects: ", count_defects)
        # print ("the angle is:", angle_defects)
        # print ("The area of effective circle is ", perimerter - area)
        k = cv2.waitKey(10)

        if k == 27 or k == ord('q'):
            break


def numbers():
    camera = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_TRIPLEX
    print_color = (255, 0, 0)
    print_position = (50, 50)
    while camera.isOpened():
        _, img = camera.read()
        value = (35, 35)
        defects = 0
        cv2.rectangle(img, (300, 300), (100, 100), (255, 0, 0), 0)
        ing_Select = img[100:300, 100:300]
        grey = cv2.cvtColor(ing_Select, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(grey, value, 0)
        cv_val = cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
        _, threshold = cv2.threshold(blurred, 127, 255, cv_val)
        cv2.imshow('Threshold', threshold)
        (vaal, _, _) = cv2.__version__.split('.')
        if vaal == '2':
            contours, hierarchy = cv2.findContours(threshold.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        elif vaal == '3':
            image, contours, hierarchy = cv2.findContours(threshold.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        counter = max(contours, key=lambda p1: cv2.contourArea(p1))
        p1, p2, dim_1, hei_1 = cv2.boundingRect(counter)
        cv2.rectangle(ing_Select, (p1, p2), (p1 + dim_1, p2 + hei_1), (255, 0, 0), 0)
        shape_border = cv2.convexHull(counter)
        shape_drawing = np.zeros(ing_Select.shape, np.uint8)
        cv2.drawContours(shape_drawing, [counter], 0, (255, 0, 0), 0)
        cv2.drawContours(shape_drawing, [shape_border], 0, (255, 0, 0), 0)
        shape_border = cv2.convexHull(counter, returnPoints=False)
        numbers = cv2.convexityDefects(counter, shape_border)
        cv2.drawContours(threshold, contours, -1, (255, 0, 0), 3)
        for i in range(numbers.shape[0]):
            val_1, val_2, f, d = numbers[i, 0]
            initial_point = tuple(counter[val_1][0])
            final_point = tuple(counter[val_2][0])
            dist_point = tuple(counter[f][0])
            a = math.sqrt(
                int(pow((final_point[0] - initial_point[0]), 2)) + int(pow((final_point[1] - initial_point[1]), 2)))
            b = math.sqrt(
                int(pow(dist_point[0] - initial_point[0], 2)) + int(pow((dist_point[1] - initial_point[1]), 2)))
            c = math.sqrt(int(pow((final_point[0] - dist_point[0]), 2)) + int(pow((final_point[1] - dist_point[1]), 2)))
            ang = ((int(pow(b, 2)) + int(pow(c, 2)) - int(pow(a, 2))) / (2 * b * c))
            angle = math.acos(ang)
            angle = angle * 60
            if angle <= 90:
                defects += 1
                cv2.circle(ing_Select, dist_point, 1, (255, 0, 0), -2)
            cv2.line(ing_Select, initial_point, final_point, (255, 0, 0), 2)
        if defects == 1:
            cv2.putText(img, "Two", print_position, font, 1, print_color, 2, cv2.LINE_AA)
        elif defects == 2:
            cv2.putText(img, "Three", print_position, font, 1, print_color, 2, cv2.LINE_AA)
        elif defects == 3:
            cv2.putText(img, "Four", print_position, font, 1, print_color, 2, cv2.LINE_AA)
        elif defects == 4:
            cv2.putText(img, "Five", print_position, font, 1, print_color, 2, cv2.LINE_AA)
        elif defects == 0:
            cv2.putText(img, "One", print_position, font, 1, print_color, 2, cv2.LINE_AA)
        elif defects < 0:
            cv2.putText(img, "Default", print_position, font, 1, print_color, 2, cv2.LINE_AA)
        cv2.imshow('Count Numbers', img)
        scorre = np.hstack((shape_drawing, ing_Select))
        cv2.imshow('Contours', scorre)
        # print ('Radius: ', math.pi * (int(pow(radius, 2))), "Area: ", area)
        # print ("Perimeter of contour: ", perimeter)
        # print ("The aspect ratio is:", AR)
        # print ("Convexity Defects: ", count_defects)
        # print ("the angle is:", angle_defects)
        # print ("The area of effective circle is ", perimerter - area)

        k = cv2.waitKey(10)
        if k == 27 or k == ord('q'):
            break


def exit():
    root.destroy()

part_0 = Label(root, text="Welcome to American Sign Langugae gesture recognition. Please follow the instructions")

part_0.config(width=75)
part_0.config(font=("Times New Roman", 25))
part_0.pack()


part_x = Label(root, text="------------------------------------------------------------------------------------")
part_x.config(width=90)
part_x.config(font=("Times New Roman", 25))
part_x.pack()

part_1 = Label(root, text="Click the button below for alphabets")
part_1.config(width=90)
part_1.config(font=("Times New Roman", 25))
part_1.pack()

part_2 = Button(root, text="Alphabets", command=main, bg="gold1")
part_2.config(font=("Times New Roman", 30, "bold"))
part_2.pack()

part_3 = Label(root, text="Click the button below for numbers")
part_3.config(width=90)
part_3.config(font=("Times New Roman", 25))
part_3.pack()

part_4 = Button(root, text="Numbers", command=numbers, bg="pink")
part_4.config(font=("Times New Roman", 30, "bold"))
part_4.pack()

part_5 = Label(root, text="Press Esc and then click exit.")
part_5.config(width=90)
part_5.config(font=("Times New Roman", 25))
part_5.pack()

part_6 = Button(root, text="Exit", command=exit, bg="salmon")
part_6.config(font=("Times New Roman", 30, "bold"))
part_6.pack()

root.mainloop()
