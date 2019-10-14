import cv2
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
def rewrite(video):
    cap = cv2.VideoCapture(video)
    out = cv2.VideoWriter(
        'Video_Rewrite.avi',
        # cv2.VideoWriter_fourcc('H','F','Y','U'),
        # int(cap.get(cv2.CAP_PROP_FOURCC)),
        cv2.VideoWriter_fourcc('F','F','V','1'),
        # cv2.VideoWriter_fourcc('M','J','2','C'),
        # cv2.VideoWriter_fourcc('X','2','6','4'),
        # -1,
        # 0,
        cap.get(cv2.CAP_PROP_FPS),
        (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    )
    print("Replicating el video")
    while cap.isOpened():
        ret, img = cap.read()
        if not ret:
            break
        # print(img[0][0])
        out.write(img)
    cap.release()
    out.release()

def EncryptVideo(video):
    cap = cv2.VideoCapture(video)
    print(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
    print(int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    out = cv2.VideoWriter(
        # 'Encrypted_Video.mp4',
        'Encrypted_Video.avi',
        # int(cap.get(cv2.CAP_PROP_FOURCC)),
        # cv2.VideoWriter_fourcc('A','S','L','C'),
        # cv2.VideoWriter_fourcc('D','I','V','X'),
        cv2.VideoWriter_fourcc('F','F','V','1'),
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
    WatermarkFrame(frame)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        print(int(y + h / 2), int(x + w / 2), frame[int(y + h / 2)][int(x + w / 2)])
        frame[int(y + h / 2)][int(x + w / 2)] = [255, 0, 0]

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
        if not ret or isFrameVerified == 0 or isFrameVerified == 2:
            break
        isFrameVerified = VerifyFrame(img)

    cap.release()
    return isFrameVerified

def VerifyFrame(frame):
    watermarkResult = VerifyWatermark(frame)
    if watermarkResult == 2:
        return watermarkResult
    return VerifyFace(frame)


def VerifyFace(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        print(int(y + h / 2), int(x + w / 2), frame[int(y + h / 2)][int(x + w / 2)])
        if not (frame[int(y + h / 2)][int(x + w / 2)] == [255, 0, 0]).all():
            return 0
    return 1

def VerifyWatermark(frame):
    print("Watermark")
    print(frame[0][0])
    rowMax = len(frame) - 1
    colMax = len(frame[0]) - 1
    isWatermarked = ((frame[0][0] == [255, 0, 0]).all() and
            (frame[rowMax][0] == [255, 0, 0]).all() and
            (frame[0][colMax] == [255, 0, 0]).all() and
            (frame[rowMax][colMax] == [255, 0, 0]).all())
    if isWatermarked:
      return 1
    else:
      return 2


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
    # rewrite('Video_Rewrite.avi')
    # EncryptVideo("Video_Rewrite.mp4")
    EncryptVideo("Video_Rewrite.avi")
    # watchVideo("Videos/Video1.mp4")
    # watchVideo("Encrypted_Video.mp4")
    print(VerifyVideo('Encrypted_Video.avi'))


