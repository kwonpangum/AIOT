import cv2

img = cv2.imread("origin.png")

cv2.imshow("ORIGIN", img)

cv2.waitKey()
cv2.destroyAllWindows()

