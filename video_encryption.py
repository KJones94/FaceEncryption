import cv2
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
def rewrite(video):
    cap = cv2.VideoCapture(video)
    out = cv2.VideoWriter(
        'Video_Rewrite.mp4',
        cv2.VideoWriter_fourcc('A','S','L','C'),
        cap.get(cv2.CAP_PROP_FPS),
        (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    )
    print("Replicating el video")
    while cap.isOpened():
        ret, img = cap.read()
        if not ret:
            break
        out.write(img)
    cap.release()
    out.release()

def EncryptVideo(video):
    cap = cv2.VideoCapture(video)
    print(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
    print(int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    out = cv2.VideoWriter(
        'Encrypted_Video.mp4',
        # int(cap.get(cv2.CAP_PROP_FOURCC)),
        cv2.VideoWriter_fourcc('A','S','L','C'),
        cap.get(cv2.CAP_PROP_FPS),
        (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    )
    print("Do video encryption")

    while cap.isOpened():
        ret, img = cap.read()
        if not ret:
            break
        img = EncryptFrame(img)
        out.write(img)
    cap.release()
    out.release()   


def EncryptFrame(frame):
    print("Encrypt frame")
    # frame[0][0] = [255, 0, 0]
    # frame[len(frame) - 1][0] = [255, 0, 0]
    # frame[0][len(frame[0]) - 1] = [255, 0, 0]
    # frame[len(frame) - 1][len(frame[0]) - 1] = [255, 0, 0]
    WatermarkFrame(frame)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        # diff = 10
        #
        # for col in range(int(x+(w/2)-diff), int(x+(w/2)+diff+1)):
        #     for row in range(int(y+h/2-diff),int(y+h/2+diff+1)):
        #         frame[row][col] = [255,0,0]


        print(int(y + h / 2), int(x + w / 2), frame[int(y + h / 2)][int(x + w / 2)])
        frame[int(y + h / 2)][int(x + w / 2)] = [255, 0, 0]
        # frame[int(y+h/2), int(x+w/2), 0] = 255
        # frame[int(y + h / 2), int(x + w / 2), 1] = 0
        # frame[int(y + h / 2), int(x + w / 2), 2] = 0
        # frame[int(y + h / 2) + 10][int(x + w / 2) + 10] = [255, 0, 0]
        # frame[int(y + h / 2) - 10][int(x + w / 2) - 10] = [255, 0, 0]

    return frame


def WatermarkFrame(frame):
    print(len(frame), len(frame[0]))
    frame[0][0] = [255, 0, 0]
    frame[len(frame) - 1][0] = [255, 0, 0]
    frame[0][len(frame[0]) - 1] = [255, 0, 0]
    frame[len(frame) - 1][len(frame[0]) - 1] = [255, 0, 0]

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

def VerifyFrame(frame):
    # print("Verify frame")
    return VerifyWatermark(frame)

def VerifyFace(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        print(int(y + h / 2), int(x + w / 2), frame[int(y + h / 2)][int(x + w / 2)])
        if not (frame[int(y + h / 2)][int(x + w / 2)] == [255, 0, 0]).all():
            return False
    return True

def VerifyWatermark(frame):
    print("Watermark")
    print(frame[0][0])
    rowMax = len(frame) - 1
    colMax = len(frame[0]) - 1
    return ((frame[0][0] == [255, 0, 0]).all() and
            (frame[rowMax][0] == [255, 0, 0]).all() and
            (frame[0][colMax] == [255, 0, 0]).all() and
            (frame[rowMax][colMax] == [255, 0, 0]).all())


def paintFrame(frame):
    print("Encrypt frame")
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.circle(frame, (int(x + w/2), int(y + h/2)), 1, (255,0,0), 5)

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

if __name__=='__main__':
    rewrite('Videos/Video1.mp4')
    EncryptVideo("Video_Rewrite.mp4")
    # watchVideo("Videos/Video1.mp4")
    # watchVideo("Encrypted_Video.mp4")
    print(VerifyVideo('Encrypted_Video.mp4'))


