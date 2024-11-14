import cv2 as cv
import mediapipe as mp
from google.protobuf.json_format import MessageToDict

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

def get_hand_move(hand_landmarks):
    landmarks = hand_landmarks.landmark
    if all([landmarks[i].y < landmarks[i+3].y for i in range(9,20,4)]):
        return "rock"
    elif landmarks[13].y < landmarks[16].y and landmarks[17].y < landmarks[20].y:
        return "scissors"
    else:
        return "paper"

def detect_players(results, frame):
    if results.multi_hand_landmarks:
        for i in results.multi_handedness:
            label = MessageToDict(i)['classification'][0]['label']
            if label == 'Right':
                cv.putText(frame, 'Player 1', (10, 90), cv.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2, cv.LINE_AA)
            elif label == 'Left':
                cv.putText(frame, 'Player 2', (980, 90), cv.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2, cv.LINE_AA)

def main():
    vid = cv.VideoCapture(0)
    vid.set(3, 1920)
    vid.set(4, 1080)
    clock = 0
    p1_move, p2_move = None, None
    game_text = ""
    success = True
    p1_score, p2_score = 0, 0

    with mp_hands.Hands(model_complexity=0, min_tracking_confidence=0.5, min_detection_confidence=0.5) as hands:
        while True:
            ret, frame = vid.read()
            if not ret or frame is None:
                break
            frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            results = hands.process(frame)
            frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style()
                    )

            frame = cv.flip(frame, 1)
            detect_players(results, frame)

            if 0 <= clock < 40:
                success = True
                game_text = "Ready?"
            elif clock < 50:
                game_text = "3..."
            elif clock < 60:
                game_text = "2..."
            elif clock < 70:
                game_text = "1..."
            elif clock < 80:
                game_text = "GO!"
            elif clock == 80:
                if results.multi_hand_landmarks:
                    for i in results.multi_handedness:
                        hand_landmarks = results.multi_hand_landmarks
                        if hand_landmarks and len(hand_landmarks) == 2:
                            detect_players(results, frame)
                            label = MessageToDict(i)['classification'][0]['label']
                            if label == 'Left':
                                p1_move = get_hand_move(hand_landmarks[0])
                            elif label == 'Right':
                                p2_move = get_hand_move(hand_landmarks[1])
                else:
                    success = False
            elif clock < 82:
                if success:
                    game_text = f"Player 1 played {p1_move}. Player 2 played {p2_move}."
                    if p1_move == p2_move:
                        game_text = f"{game_text} Game is tied."
                    elif (p1_move, p2_move) in [('paper', 'rock'), ('rock', 'scissors'), ('scissors', 'paper')]:
                        game_text = f"{game_text} Player 1 wins."
                        p1_score += 1
                    else:
                        game_text = f"{game_text} Player 2 wins."
                        p2_score += 1
                else:
                    game_text = "You didn't play properly."

            clock = (clock + 1) % 110

            cv.putText(frame, game_text, (10, 30), cv.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2, cv.LINE_AA)
            cv.putText(frame, f'Player 1 score: {p1_score}', (10, 60), cv.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2, cv.LINE_AA)
            cv.putText(frame, f'Player 2 score: {p2_score}', (980, 60), cv.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2, cv.LINE_AA)
            cv.rectangle(frame, (31, 670), (1230, 708), (0, 255, 255), 3)
            cv.putText(frame, 'Note: No other signs are allowed other than rock, paper, scissors', (36, 700), cv.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2, cv.LINE_AA)

            cv.imshow('Rock, Paper, Scissors', frame)

            if cv.waitKey(1) & 0xFF == ord('q'):
                break

    vid.release()
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()
