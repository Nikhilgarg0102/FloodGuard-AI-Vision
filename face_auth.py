import cv2

# load trained recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer.yml")

# load face detector
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)

def authenticate_user():

    cap = cv2.VideoCapture(0)

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(
            gray,
            1.3,
            5
        )

        for (x, y, w, h) in faces:

            face = gray[y:y+h, x:x+w]

            user_id, confidence = recognizer.predict(face)

            # lower confidence = better match
            if confidence < 60:

                cv2.putText(
                    frame,
                    "ACCESS GRANTED",
                    (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0,255,0),
                    2
                )

                cv2.rectangle(
                    frame,
                    (x,y),
                    (x+w,y+h),
                    (0,255,0),
                    2
                )

                cv2.imshow("Authentication", frame)

                cv2.waitKey(2000)

                cap.release()
                cv2.destroyAllWindows()

                return True

            else:

                cv2.putText(
                    frame,
                    "UNAUTHORIZED",
                    (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0,0,255),
                    2
                )

                cv2.rectangle(
                    frame,
                    (x,y),
                    (x+w,y+h),
                    (0,0,255),
                    2

                )

        cv2.imshow("Authentication", frame)

        # press ESC to exit
        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

    return False