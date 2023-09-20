import timeit

import cv2
# import numpy as np
import serial
import pt_ctrl


cam = cv2.VideoCapture(0)

sp = serial.Serial('/dev/tty.usbmodem1401', 9600, timeout=1)

# 가중치 파일 경로
cascade_filename = '/Users/pangumk/PycharmProjects/allaboutidea/AIOT/facial_detect/haarcascade_frontalface_alt.xml'

# 모델 불러 오기
cascade = cv2.CascadeClassifier(cascade_filename)

def main(args=None):
    pos_x = 90
    pos_y = 90

    margin = 20

    cam_width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
    cam_height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

    cam_center_x = cam_width / 2
    cam_center_y = cam_height / 2

    print(cam_width, cam_height)
    print(cam_center_x, cam_center_y)

    if not cam.isOpened():
        print("Could not open webcam")
        exit()

    while cam.isOpened():
        status, img = cam.read()

        img = cv2.flip(img, 1)  # 좌우 반전

        start_t = timeit.default_timer()

        # 영상 압축
        img = cv2.resize(img, dsize=None, fx=1.0, fy=1.0)
        # 그레이 스케일 변환
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # cascade 얼굴 탐지 알고리즘
        results = cascade.detectMultiScale(gray,  # 입력 이미지
                                           scaleFactor=1.1,  # 이미지 피라미드 스케일 factor
                                           minNeighbors=5,  # 인접 객체 최소 거리 픽셀
                                           minSize=(20, 20)  # 탐지 객체 최소 크기
                                           )

        for box in results:
            x, y, w, h = box
            print("center_x = %s, center_y = %s" % ((x + w // 2), (y + h // 2)))
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), thickness=2)
            center_x = x + w // 2
            center_y = y + h // 2
            print("center: ( %s, %s )" % (center_x, center_y))
            if (center_x > (cam_center_x - margin)) and (center_x < (cam_center_x + margin)) and (
                    center_y > (cam_center_y - margin)) and (center_y < (cam_center_y + margin)):
                print("stop")
            else:
                if center_x < cam_center_x - margin:
                    print("pan right : ", end=' ')
                    print(cam_center_x - center_x)
                    if pos_x - 1 >= 0:
                        pos_x = pos_x - 1
                    else:
                        pos_x = 0

                elif center_x > cam_center_x + margin:
                    print("pan left : ", end=' ')
                    print(center_x - cam_center_x)
                    if pos_x + 1 <= 180:
                        pos_x = pos_x + 1
                    else:
                        pos_x = 180

                pt_ctrl.send_pan(pos_x)

                if center_y < cam_center_y - margin:
                    print("til up : ", end=' ')
                    print(cam_center_y - center_y)
                    if pos_y - 1 >= 0:
                        pos_y = pos_y - 1
                    else:
                        pos_y = 0

                elif center_y > cam_center_y + margin:
                    print("til down : ", end=' ')
                    print(center_y - cam_center_y)
                    if pos_y + 1 <= 180:
                        pos_y = pos_y + 1
                    else:
                        pos_y = 180

                pt_ctrl.send_tilt(pos_y)

        terminate_t = timeit.default_timer()
        FPS = 'fps' + str(int(1. / (terminate_t - start_t)))
        cv2.putText(img, FPS, (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1)

    # 영상 출력
        cv2.imshow('result', img)

    # cv2.imshow('VideoFrame', frame_flipped)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
