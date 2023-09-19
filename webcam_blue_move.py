import cv2
import numpy as np
import serial
import pt_ctrl

sp = serial.Serial('/dev/tty.usbmodem1201', 9600, timeout=1)

pos_x = 90
pos_y = 90

_pos_x = 90
_pos_y = 90

margin = 20

webcam = cv2.VideoCapture(0)

webcam_width = int(webcam.get(cv2.CAP_PROP_FRAME_WIDTH))
webcam_height = int(webcam.get(cv2.CAP_PROP_FRAME_HEIGHT))

cam_center_x = webcam_width / 2
cam_center_y = webcam_height / 2

print(webcam_width, webcam_height)
print(cam_center_x, cam_center_y)

if not webcam.isOpened():
    print("Could not open webcam")
    exit()

while webcam.isOpened():
    status, frame = webcam.read()
    if not status:
        break

    frame_flipped = cv2.flip(frame, 1)  # 좌우 반전

    hsv = cv2.cvtColor(frame_flipped, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([100, 100, 120])
    upper_blue = np.array([150, 255, 255])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    res = cv2.bitwise_and(frame_flipped, frame_flipped, mask=mask)

    gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    _, bin = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    largest_contour = None
    largest_area = 0

    COLOR = (0, 255, 0)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > largest_area:
            largest_area = area
            largest_contour = cnt

    if largest_contour is not None:
        if largest_area > 500:
            x, y, width, height = cv2.boundingRect(largest_contour)
            cv2.rectangle(frame_flipped, (x, y), (x + width, y + height), COLOR, 2)
            center_x = x + width // 2
            center_y = y + height // 2
            print("center: ( %s, %s )" % (center_x, center_y))
            if (center_x > (cam_center_x - margin)) and (center_x < (cam_center_x + margin)) and (center_y > (cam_center_y - margin)) and (center_y < (cam_center_y + margin)):
                print("stop")
            else:
                if center_x < cam_center_x - margin:
                    print("pan right : ", end=' ')
                    print(cam_center_x - center_x)
                    if pos_x - 1 >= 0:
                        pos_x = pos_x - 1
                        _pos_x = pos_x
                    else:
                        pos_x = 0
                        _pos_x = pos_x

                elif center_x > cam_center_x + margin:
                    print("pan left : ", end=' ')
                    print(center_x - cam_center_x)
                    if pos_x + 1 <= 180:
                        pos_x = pos_x + 1
                        _pos_x = pos_x
                    else:
                        pos_x = 180
                        _pos_x = pos_x

                pt_ctrl.send_pan(pos_x)

                if center_y < cam_center_y - margin:
                    print("til up : ", end=' ')
                    print(cam_center_y - center_y)
                    if pos_y - 1 >= 0:
                        pos_y = pos_y - 1
                        _pos_y = pos_y
                    else:
                        pos_y = 0
                        _pos_y = pos_y

                elif center_x > cam_center_x + margin:
                    print("til down : ", end=' ')
                    print(center_y - cam_center_y)
                    if pos_y + 1 <= 180:
                        pos_y = pos_y + 1
                        _pos_y = pos_y
                    else:
                        pos_y = 180
                        _pos_y = pos_y

                pt_ctrl.send_tilt(pos_y)

    cv2.imshow('VideoFrame', frame_flipped)

    k = cv2.waitKey(5) & 0xFF

    if k == 27:
        break

webcam.release()
cv2.destroyAllWindows()
