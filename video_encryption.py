import cv2
import random
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# Gives an uncompressed version of the video:
def rewrite(video):
    cap = cv2.VideoCapture(video)
    out = cv2.VideoWriter(
        'Video_Rewrite.avi',
        # Compression method
        cv2.VideoWriter_fourcc('F','F','V','1'),
        cap.get(cv2.CAP_PROP_FPS),
        (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
         int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    )
    print("Replicating el video")
    while cap.isOpened():
        ret, img = cap.read()
        if not ret:
            break
        out.write(img)
    cap.release()
    out.release()

#Encrypts the video frame by frame
def EncryptVideo(video):
    cap = cv2.VideoCapture(video)
    print(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
    print(int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    out = cv2.VideoWriter(
        'Encrypted_Video.avi',
        #Compression method
        cv2.VideoWriter_fourcc('F','F','V','1'),
        cap.get(cv2.CAP_PROP_FPS),
        (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    )
    print("Do video encryption")

    # Goes frame-by-frame running EncryptFrame
    while cap.isOpened():
        ret, img = cap.read()
        if not ret:
            break
        img = EncryptFrame(img)
        out.write(img)
    cap.release()
    out.release()   

#Encrypts individual frams
def EncryptFrame(frame):
    print("Encrypt frame")

    #Facial recognition setup
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    #marking a pixel every time there's a face
    for (x,y,w,h) in faces:
        # print(int(y + h / 2), int(x + w / 2), frame[int(y + h / 2)][int(x + w / 2)])
        frame[int(y + h / 2)][int(x + w / 2)] = [255, 0, 0]

    return frame


#Changes a pixel in each corner of each frame
def WatermarkFrame(frame):
    print(len(frame), len(frame[0]))
    #step 1
    maxRows = len(frame)
    maxCols = len(frame[0])
    col = random.randint(1,maxCols)
    row = random.randint(1,maxRows)
    scale = 1
    changed = 0
    if col>255 or row > 255:
        changed += 1
        if col>row:
            col += col % (int(maxCols/ 255))
            row += row % (int(maxCols/255))
            frame[row][col] = [255, 0, 0]
            col = col/(maxCols/255)
            row = row/(maxCols/255)
            scale = int(maxCols/255) + 1
        elif row>col:
            row += row%(int(maxRows)/255)
            col += col % (int(maxRows/255))
            frame[row][col] = [255, 0, 0]
            row = row/(maxRows/255)
            col = col/(maxRows/255)
            scale = int(maxRows/255)+1
        # else:
        #     col += col%(int(frame.length/255))
        #     row += row%(int(frame[0].length/255))
        #     scale = col/(frame[0].length/255)
    if changed == 0:
        frame[row][col] = [255, 0, 0]

    frame[col/scale][row/scale] = [row,col,scale]
    frame[len(frame) - 1][0] = [255, 0, 0]
    frame[0][len(frame[0]) - 1] = [255, 0, 0]
    frame[len(frame) - 1][len(frame[0]) - 1] = [255, 0, 0]

#Verify function
def VerifyVideo(video):
    cap = cv2.VideoCapture(video)
    print(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
    print(int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    print("Do video verification")

    isFrameVerified = True
    while cap.isOpened():
        ret, img = cap.read()
        # if not ret or not isFrameVerified:
        if not ret:
            break
        isFrameVerified = VerifyFrame(img)

    cap.release()
    return isFrameVerified

#Checks each frame
def VerifyFrame(frame):
    # print("Verify frame")
    return VerifyWatermark(frame)  and VerifyFace(frame)

#Verifies face-pixels
def VerifyFace(frame):
    #facial recognition setup
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    #analyzes pixel on face
    for (x, y, w, h) in faces:
        print(int(y + h / 2), int(x + w / 2), frame[int(y + h / 2)][int(x + w / 2)])
        if not (frame[int(y + h / 2)][int(x + w / 2)] == [255, 0, 0]).all():
            return False
    return True

#Checks if watermarks are there
def VerifyWatermark(frame):
    print("Watermark")
    print(frame[0][0])
    rowMax = len(frame) - 1
    colMax = len(frame[0]) - 1
    return ((frame[0][0] == [255, 0, 0]).all() and
            (frame[rowMax][0] == [255, 0, 0]).all() and
            (frame[0][colMax] == [255, 0, 0]).all() and
            (frame[rowMax][colMax] == [255, 0, 0]).all())

#Alternative encryption method
def paintFrame(frame):
    print("Encrypt frame")
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.circle(frame, (int(x + w/2), int(y + h/2)), 1, (255,0,0), 5)

#Opens the video (will be large, uncompressed)
def watchVideo(video_file):
    cap = cv2.VideoCapture(video_file)
    while 1:
        ret, img = cap.read()
        if not ret:
            break
        cv2.imshow('Video',img)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
    cap.release()
    cv2.destroyAllWindows()

#What to run when video_encryption is run
if __name__=='__main__':
    rewrite('Videos/Video1.mp4')
    # rewrite('Video_Rewrite.avi')
    # EncryptVideo("Video_Rewrite.mp4")
    EncryptVideo("Video_Rewrite.avi")
    # watchVideo("Videos/Video1.mp4")
    # watchVideo("Encrypted_Video.mp4")
    print(VerifyVideo('Encrypted_Video.avi'))


