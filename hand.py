import cv2
import mediapipe as mp
import re



def recognizeHandGesture(landmarks):
    thumbState = 'UNKNOW'
    indexFingerState = 'UNKNOW'
    middleFingerState = 'UNKNOW'
    ringFingerState = 'UNKNOW'
    littleFingerState = 'UNKNOW'
    number_of_oupen_fingers = 0

    pseudoFixKeyPoint = landmarks['x2']
    if (landmarks['x3'] < pseudoFixKeyPoint and landmarks['x4'] < landmarks['x3']):
        thumbState = 'OPEN'
        number_of_oupen_fingers += 1
    elif (landmarks['x3'] < pseudoFixKeyPoint and landmarks['x4'] < landmarks['x5']):
        thumbState = 'CLOSE'   
    print('thumbState ',thumbState)
    
    pseudoFixKeyPoint = landmarks['y6']
    if (landmarks['y7'] < pseudoFixKeyPoint and landmarks['y8'] < landmarks['y7']):
        indexFingerState = 'OPEN'
        number_of_oupen_fingers += 1
    elif (landmarks['y7'] < landmarks['y8']) and (landmarks['y7'] < landmarks['y5']):
        indexFingerState = 'CLOSE' 
    print("indexFingerState ", indexFingerState)
    
    
    pseudoFixKeyPoint = landmarks['y10']
    if (landmarks['y11'] < pseudoFixKeyPoint and landmarks['y12'] < landmarks['y11']):
        middleFingerState = 'OPEN'  
        number_of_oupen_fingers += 1
    elif (landmarks['y11'] < landmarks['y12']) and (landmarks['y12'] > landmarks['y9']):
        middleFingerState = 'CLOSE'
    print("middleFingerState ", middleFingerState)
    
    pseudoFixKeyPoint = landmarks['y14']
    if (landmarks['y15'] < pseudoFixKeyPoint and landmarks['y16'] < landmarks['y15']):
        ringFingerState = 'OPEN'  
        number_of_oupen_fingers += 1
    elif (landmarks['y15'] < landmarks['y16']) and (landmarks['y13'] < landmarks['y16']):
        ringFingerState = 'CLOSE'
    print("ringFingerState ", ringFingerState)
    
    pseudoFixKeyPoint = landmarks['y18']
    if (landmarks['y19'] < pseudoFixKeyPoint and landmarks['y20'] < landmarks['y19']):
        littleFingerState = 'OPEN'   
        number_of_oupen_fingers += 1
    elif ( landmarks['y19'] < landmarks['y20']) and ( landmarks['y17'] < landmarks['y20']):
        littleFingerState = 'CLOSE'
    print("littleFingerState ", littleFingerState)
    
    cv2.putText(image, str(number_of_oupen_fingers), (10,450), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), 2, cv2.LINE_AA)
    
    if thumbState == "OPEN" and indexFingerState == "OPEN" and middleFingerState == "CLOSE" and ringFingerState == "UNKNOW" and littleFingerState == "OPEN":
        cv2.putText(image, "ROCK", (270,80), cv2.FONT_HERSHEY_COMPLEX, 3, (0, 0, 200), 5, cv2.LINE_AA)
    elif thumbState == "CLOSE" and indexFingerState == "OPEN" and middleFingerState == "OPEN" and ringFingerState == "CLOSE" and (littleFingerState == "CLOSE" or littleFingerState == "UNKNOW"):
        cv2.putText(image, "VICTORY", (200,80), cv2.FONT_HERSHEY_COMPLEX, 3, (150, 0, 0), 5, cv2.LINE_AA)
    elif (thumbState == "OPEN" or thumbState == "UNKNOW") and indexFingerState == "OPEN" and middleFingerState == "OPEN" and ringFingerState == "CLOSE" and littleFingerState == "CLOSE":
        cv2.putText(image, "YES", (200,80), cv2.FONT_HERSHEY_COMPLEX, 3, (150, 0, 150), 5, cv2.LINE_AA)
    elif thumbState == "OPEN" and (indexFingerState == "CLOSE" or indexFingerState == "UNKNOW") and middleFingerState == "UNKNOW" and ringFingerState == "UNKNOW" and littleFingerState == "OPEN":
        cv2.putText(image, "CALL ME", (200,80), cv2.FONT_HERSHEY_COMPLEX, 3, (150, 150, 50), 5, cv2.LINE_AA)
    
def getStructuredLandmarks(landmarks):
    regex = r" [x,y]: [0-9].{15}"
    dict_result = {}
    matches = re.finditer(regex, landmarks, re.MULTILINE)
    
    number_x = 1
    number_y = 1 
    

    for matchNum, match in enumerate(matches, start=1):
        x = 0
        y = 0
        
        try:
            if "x" in match.group():
                dict_result[f"x{number_x}"] = float(match.group()[5:-1])
                number_x += 1
            if "y" in match.group():
                dict_result[f"y{number_y}"] = float(match.group()[5:-1])
                number_y += 1
        except ValueError:
            if "x" in match.group():
                dict_result[f"x{number_x}"] = float(match.group()[5:8])
                number_x += 1
            if "y" in match.group():
                dict_result[f"y{number_y}"] = float(match.group()[5:8])
                number_y += 1
            
        print("****************")
        print(dict_result)
        print("****************")
        
    return dict_result


# The landmarks array has the following structur: [x0, y0, x1, y1, ....., x20, y20]
# with for example x0 and y0 the x and y values of the landmark at index 0.


mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# For webcam input:
hands = mp_hands.Hands(
    min_detection_confidence=0.7, min_tracking_confidence=0.6)
cap = cv2.VideoCapture(0)
while cap.isOpened():
    success, image = cap.read()
    if not success:
        break

    # Flip the image horizontally for a later selfie-view display, and convert
    # the BGR image to RGB.
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    results = hands.process(image)

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    
    if results.multi_hand_landmarks:
        list_result_landmarks = []

        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            mp_hands.HAND_CONNECTIONS
            list_result_landmarks.append(str(hand_landmarks))

        if len(list_result_landmarks) == 1:
            print(recognizeHandGesture(getStructuredLandmarks(str(list_result_landmarks))))
        
        elif len(list_result_landmarks) == 2:
            print(recognizeHandGesture(getStructuredLandmarks(str(list_result_landmarks[0]))))

    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(5) & 0xFF == 27:
        break

hands.close()
cap.release()
