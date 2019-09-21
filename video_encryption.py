import cv2
face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

def EncryptVideo(video):
    cap = cv2.VideoCapture(video)
    print(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
    print(int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    out = cv2.VideoWriter(
        'Encrypted_Video.mp4',
        int(cap.get(cv2.CAP_PROP_FOURCC)),
        cap.get(cv2.CAP_PROP_FPS),
        (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    )
    print("Do video encryption")

    while cap.isOpened():
        ret, img = cap.read()
        if not ret:
            break
        EncryptFrame(img)
        out.write(img)
    cap.release()
    out.release()


def EncryptFrame(frame):
    print("Encrypt frame")
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.circle(frame, (int(x + w/2), int(y + h/2)), 1, (255,0,0), 5)
    #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #faces = face_cascade.detectMultiScale(gray, 1.3, 5)

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

EncryptVideo("Videos/Video1.mp4")
# watchVideo("Videos/Video1.mp4")
# watchVideo("Encrypted_Video.mp4")
"""
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture("Videos/ForrestGump.mp4")

while 1:
    ret, img = cap.read(
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    """


