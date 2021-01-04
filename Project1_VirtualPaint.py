import cv2
import numpy as np
#membuat virtual paint, menggambar secara virtual
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
cap.set(10, 100)

myColors = [[0,169,188,179,255,255], #warna orange
            [47,113,101,179,255,255], #warna biru
            [1,169,99,179,255,255], #warna merah
            [2,161,144,179,255,255], #warna kuning
            [35,94,102,179,255,255] #warna hijau
            ]

#ini berfungsi untuk memunculkan warna paint sesuai dgn yg di object
myColorsValue = [[51,153,255], #BGR
                 [255,0,0],
                 [0,0,255],
                 [0,255,255],
                 [0,255,0]]

myPoints = [] #x,y, colorId

#fungsi (nilai input)
def findColor(img, myColors, myColorsValue):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    newPoints=[] #ini berfungsi untuk memberikan gambar pertitik
    for color in myColors:
        lower = np.array(color[0:3]) #mengambil 3 pertama sbg nilai min
        upper = np.array(color[3:6]) #mengambil 3 akhir sbg nilai tertinggi
        mask = cv2.inRange(imgHSV, lower, upper) #membuat masking
        x, y = getContours(mask) #kita mengirimkan data mask, ke getContours
        #cv2 circle untuk memunculan titik kecil bulat gambar (target img, memanggil axis x,y, 
        # berapa besar radius warna, warna ygg muncul di radius, terisi atau tidak)
        cv2.circle(imgResult, (x,y), 10, myColorsValue[count], cv2.FILLED)
        #jika nilai x dan y tdk 0, maka memulai yg baru
        if x!= 0 and y!= 0: #disini sy sempat salah, krn menulis 'and' sebagai '&', dimana
            #ini salah karena and menunjukkan (&&) di bahaca C, dan '&' menunjukkan jika selain nilai diminta, maka akan salah
            newPoints.append([x,y,count])
        count +=1
        # cv2.imshow(str(color[0]), mask)
    return newPoints

#code ini diambil dari chapter 8
def getContours(img):
    contours,hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x,y,w,h = 0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:
            #cv2.drawContours(imgResult, cnt, -1,(255,0,0), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
            x, y , w, h = cv2.boundingRect(approx)
    return x+w//2, y #ini mengartikan nanti muncul titik gambarnya di paling atas tengah

def drawOnCanvas(myPoints, myColorsValue):
    for point in myPoints:
        cv2.circle(imgResult, (point[0], point[1]), 10, myColorsValue[point[2]], cv2.FILLED)

while True:
    success, img = cap.read()
    imgResult = img.copy()
    newPoints = findColor(img, myColors, myColorsValue)
    if len(newPoints)!=0:
        for newP in newPoints:
            myPoints.append(newP)
            
    if len(myPoints)!=0:
        drawOnCanvas(myPoints, myColorsValue)
    
    cv2.imshow("Gambar Akhir", imgResult)    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()