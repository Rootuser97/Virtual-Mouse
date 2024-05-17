import sys
import subprocess
import cv2
import dlib
import pyautogui as control
from utilties import *

if __name__=='__main__':
    print('Virtual mouse for motor disabled people')

    if len(sys.argv) < 3:
        print('Please provide programs to execute as macro for head up and down')
        exit()
    
    MACRO_U = sys.argv[1]
    MACRO_D = sys.argv[2]

    webcam0 = cv2.VideoCapture(0)
    
    face_detector = dlib.get_frontal_face_detector()
    landmark_predictor = dlib.shape_predictor(
        "model/shape_predictor_68_face_landmarks.dat"
    )

    CURSOR_ENABLED_MODE = False

    while True:
        _, frame = webcam0.read()
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (640, 480))
        grayscale_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_detector(grayscale_image)
        if len(faces) == 0:
            continue

        user_face = faces[0]
        x1 = user_face.left()
        y1 = user_face.top()
        x2 = user_face.right()
        y2 = user_face.bottom()
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0) if CURSOR_ENABLED_MODE else (0, 0, 255), 1)

        shape = landmark_predictor(grayscale_image, user_face)
        points_array = get_numpy_array(shape)

        leftEye = points_array[lStart:lEnd]
        rightEye = points_array[rStart:rEnd]
        nose = points_array[nStart:nEnd]
        leftEye, rightEye = rightEye, leftEye

        leftEyeRatio = get_eye_aspect_ratio(leftEye)
        rightEyeRatio = get_eye_aspect_ratio(rightEye)
        bothEyeRatio = (leftEyeRatio + rightEyeRatio) / 2.0
        nosePoint = (nose[3, 0], nose[3, 1])

        cv2.putText(frame, "CURSOR ENABLED" if CURSOR_ENABLED_MODE else "CURSOR DISABLED", (0, 25), cv2.FONT_HERSHEY_PLAIN, 2.0, (0, 255, 0) if CURSOR_ENABLED_MODE else (0, 0, 255), 2)

        if bothEyeRatio <= CLOSED_EYE_AR_THRESHOLD:
            CLOSED_EYE_FRAME_COUNTER += 1

            if CLOSED_EYE_FRAME_COUNTER > CLOSED_EYE_FRAME_THRESHOLD:
                CURSOR_ENABLED_MODE = not CURSOR_ENABLED_MODE
                ANCHOR_POINT = nosePoint
                CLOSED_EYE_FRAME_COUNTER = 0
        else:
            CLOSED_EYE_FRAME_COUNTER = 0

        if CURSOR_ENABLED_MODE:
            cv2.line(frame, ANCHOR_POINT, nosePoint, (255, 255, 255), 1)
            direction = get_direction(nosePoint, ANCHOR_POINT)
            
            drag = 15
            if direction == 'right':
                control.moveRel(drag, 0)
                cv2.putText(frame, "R", (600, 25), cv2.FONT_HERSHEY_PLAIN, 2.0, (255, 0, 0), 2)
            elif direction == 'left':
                control.moveRel(-drag, 0)
                cv2.putText(frame, "L", (600, 25), cv2.FONT_HERSHEY_PLAIN, 2.0, (255, 0, 0), 2)
            elif direction == 'up':
                control.moveRel(0, -drag)
                cv2.putText(frame, "U", (600, 25), cv2.FONT_HERSHEY_PLAIN, 2.0, (255, 0, 0), 2)
            elif direction == 'down':
                control.moveRel(0, drag)
                cv2.putText(frame, "D", (600, 25), cv2.FONT_HERSHEY_PLAIN, 2.0, (255, 0, 0), 2)
        else:
            direction = get_direction(nosePoint, ANCHOR_POINT)
            cv2.line(frame, ANCHOR_POINT, nosePoint, (255, 255, 255), 1)

            if direction == 'up':
                cv2.putText(frame, "U", (600, 25), cv2.FONT_HERSHEY_PLAIN, 2.0, (255, 0, 0), 2)
                if bothEyeRatio >= EYE_AR_THRESHOLD:
                    EYE_FRAME_COUNTER += 1
                    
                    if EYE_FRAME_COUNTER > EYE_FRAME_THRESHOLD:
                        subprocess.call(MACRO_U)
                        EYE_FRAME_COUNTER = 0
                else:
                    EYE_FRAME_COUNTER = 0
            elif direction == 'down':
                cv2.putText(frame, "D", (600, 25), cv2.FONT_HERSHEY_PLAIN, 2.0, (255, 0, 0), 2)
                if bothEyeRatio >= EYE_AR_THRESHOLD:
                    EYE_FRAME_COUNTER += 1
                    
                    if EYE_FRAME_COUNTER > EYE_FRAME_THRESHOLD:
                        subprocess.call(MACRO_D)
                        EYE_FRAME_COUNTER = 0
                else:
                    EYE_FRAME_COUNTER = 0
            elif direction == 'left':
                cv2.putText(frame, "L", (600, 25), cv2.FONT_HERSHEY_PLAIN, 2.0, (255, 0, 0), 2)
                if bothEyeRatio >= EYE_AR_THRESHOLD:
                    EYE_FRAME_COUNTER += 1
                    
                    if EYE_FRAME_COUNTER > EYE_FRAME_THRESHOLD:
                        control.leftClick()
                        EYE_FRAME_COUNTER = 0
                else:
                    EYE_FRAME_COUNTER = 0
            elif direction == 'right':
                cv2.putText(frame, "R", (600, 25), cv2.FONT_HERSHEY_PLAIN, 2.0, (255, 0, 0), 2)
                if bothEyeRatio >= EYE_AR_THRESHOLD:
                    EYE_FRAME_COUNTER += 1
                    
                    if EYE_FRAME_COUNTER > EYE_FRAME_THRESHOLD:
                        control.rightClick()
                        EYE_FRAME_COUNTER = 0
                else:
                    EYE_FRAME_COUNTER = 0

        cv2.imshow("face viewer", frame)
        key = cv2.waitKey(1)
        if key == ord("q") or key == ord("Q"):
            break

    cv2.destroyAllWindows()
    webcam0.release()
