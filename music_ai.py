import os
import random
import pygame
import cv2
from deepface import DeepFace


pygame.mixer.init()

def detect_mood_from_face():
    cam = cv2.VideoCapture(0)
    mood = "chill"  

    print(" Looking at your face... press 'q' to quit camera if stuck.")

    while True:
        ret, frame = cam.read()
        if not ret:
            break


        cv2.imshow("Mood Detection (press q to capture)", frame)

    
        if cv2.waitKey(1) & 0xFF == ord('q'):
            try:
                result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
                emotion = result[0]['dominant_emotion']
                print(" Detected Emotion:", emotion)

            
                if emotion in ["happy", "surprise"]:
                    mood = "happy"
                elif emotion in ["sad", "angry", "fear", "disgust"]:
                    mood = "sad"
                else:
                    mood = "chill"
            except Exception as e:
                print(" Error detecting emotion:", e)
            break

    cam.release()
    cv2.destroyAllWindows()
    return mood

def play_music(mood):
    folder = os.path.join("music", mood)
    if not os.path.exists(folder):
        print(f" No folder found: {folder}")
        return

    songs = [f for f in os.listdir(folder) if f.lower().endswith(".mp3")]
    if not songs:
        print(" No songs in this folder.")
        return

    current_song = None

    def start_song():
        nonlocal current_song
        current_song = random.choice(songs)
        path = os.path.join(folder, current_song)
        print(f" Now Playing: {current_song}")
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()

    start_song()

    while True:
        cmd = input("(s=stop, p=play, n=next, q=quit): ").lower()
        if cmd == "s":
            pygame.mixer.music.stop()
            print(" Music stopped.")
        elif cmd == "p":
            pygame.mixer.music.play()
            print(" Music playing again.")
        elif cmd == "n":
            pygame.mixer.music.stop()
            start_song()
        elif cmd == "q":
            pygame.mixer.music.stop()
            print(" Exiting player.")

print(" Detecting your mood from face...")
feeling = detect_mood_from_face()
print(f" AI thinks you are: {feeling}")
play_music(feeling)