import cv2 as cv
import mediapipe as mp
from google.protobuf.json_format import MessageToDict

mp_drawings=mp.soultions.drawing_utils
mp_drawing_styles=mp.soultions.drawing_styles
mp_hands=mp.soultions.hands
hand_landmarks = 0
i = 0

def gethandmove(hand_landmarks):
    landmarks=hand_landmarks.landmarks
    if all([landmarks[i].y<landmarks[i+3].y for i in range(9,20,4)]):
        return "rock"
    elif landmarks[13].y < landmarks[16].y and landmarks[17].y < landmarks[20].y:
        return "scissors"
    else:
        return "paper"
    

def players():
    if results.multi_hand_landmarks:
        for i in results.multi_handedness:
            label = MessageToDict(i)['classfication'][0]['label']
            if label == 'Right':
                cv.putText(frame,'player 1',(10,90),cv.FONT_HERSHEY_PLAIN,2,(255,000,0),2,cv.LINE_AA)
            if label == 'left':
                cv.putText(frame,'player 2',(980,90),cv.FONT_HERSHEY_PLAIN,2,(255,0,0),2,cv.LINE_AA)

vid = cv.VideoCapture(0)
vid.set(3,4000)
vid.set(4,2000)
clock = 0
p1_move = p2_move = None
gameText=""
success = True
count = 0
count1 = 0

with mp_hands.Hands(model_complexity = 0, min_tracking_confidence=0.5, min_detection_confidence=0.5):
    while True:
        ret,frame = vid.read()
        if not ret or frame is None:
            break
        frame = cv.cvtColor(frame,cv.COLOR_BGR2RGB)
        results = hands.process(frame)
        frame = cv.cvtColor(frame,cv.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame,hand_landmarks,mp_hands.HAND_CONNECTIONS,
                                          mp_drawing_styles.get_default_hand_lamdmarks_style(),
                                          mp_drawing_styles.get_default_hand_connections_style())
                
        frame = cv.flip(frame,1)
        players()
        if 0 <= clock < 40:
            success = True
            gameText="ready?"
        elif clock < 50:
            gameText="3..."
        elif clock < 60:
            gameText="2..."
        elif clock < 70:
            gameText="1..."
        elif clock < 80:
            gameText="GO!"
        elif clock == 80:
            if results.multi_hand_landmarks:
                for i in results.multi_handedness:
                    hls=results.multi_hand_landmarks
                    if hls and lan(hls) ==2:
                        players()
                        label = MessageToDict(i)['classification'][0]['label']
                        if label == 'Left':
                            p1_move = gethandmove(hls[0])
                        if label == 'Right':
                            p2_move = gethandmove(hls[1])
            else:
                success = False
        elif clock < 82:
            if success:
                gameText = f"player 1 played {p1_move}.player 2 played {p2_move}."
                if p1_move == p2_move:
                    gameText = f"{gameText} game is tied."
                elif p1_move == 'paper' and p2_move == 'rock':
                    gameText=f"{gameText} player1 wins."
                    count+=1
                elif p1_move == 'rock' and p2_move == 'scissors':
                    gameText=f"{gameText} player1 wins."
                    count+=1
                elif p1_move == 'scissors' and p2_move == 'paper':
                    gameText=f"{gameText} player1 wins."
                    count+=1
                else:
                    gameText = f"{gameText} player 2 wins."
                    count1+=1
            else:
                gameText="you didn't play properly."
        
        clock =(clock + 1)%110
    
    cv.putText(frame,gameText,(10,30),cv.FONT_HERSHEY_PLAIN,2,(255,0,0),2,cv.LINE_AA)

    cv.putText(frame,f'player1 score:{count}',(10,60),cv.FONT_HERSHEY_PLAIN,2,(255,000,000),2,cv.LINE_AA)

    cv.putText(frame,f'player2 score:{count1}',(980,60),cv.FONT_HERSHEY_PLAIN,2,(255,0,000),2,cv.LINE_AA)
    
    cv.rectangle(frame,(31,670),(1230,708),(0,255,255),3)

    cv.putText(frame,'note: no other signs are allowed other than rock, paper, scissors',(36,700),cv.FONT_HERSHEY_PLAIN,2,(0,000,255),2,cv.LINE_AA)

    cv.imshow('RO-PA-SCI',frame)

    if cv.waitKey(1) & 0xFF == ord(''):
        breakpoint
vid.release()
cv.destroyAllWindows()