import numpy as np

EYE_AR_THRESHOLD = 0.32
EYE_FRAME_THRESHOLD = 8
EYE_FRAME_COUNTER = 0
CLOSED_EYE_AR_THRESHOLD = 0.23
CLOSED_EYE_FRAME_THRESHOLD = 8
CLOSED_EYE_FRAME_COUNTER = 0

ANCHOR_POINT = (0, 0)
(nStart, nEnd) = (27, 36)
(rStart, rEnd) = (36, 42) 
(lStart, lEnd) = (42, 48)

def get_numpy_array(shape):
	coordinates = np.zeros((shape.num_parts, 2), dtype="int")
	for i in range(0, shape.num_parts):
		coordinates[i] = (shape.part(i).x, shape.part(i).y)
	return coordinates

def get_eye_aspect_ratio(eye):
    A = np.linalg.norm(eye[1] - eye[5])
    B = np.linalg.norm(eye[2] - eye[4])
    C = np.linalg.norm(eye[0] - eye[3])
    return (A + B) / (2.0 * C)

def get_direction(nose_point, anchor_point):
    boundWidth, boundHeight = 30, 30
    nx, ny = nose_point
    x, y = anchor_point

    if nx > x + boundWidth:
        return 'right'
    elif nx < x - boundWidth:
        return 'left'
    elif ny > y + boundHeight:
        return 'down'
    elif ny < y - boundHeight:
        return 'up'
