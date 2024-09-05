import cv2
import os
import random
import time
import mediapipe as mp
import pygame

pygame.mixer.init()
pygame.init()
pygame.font.init()

# Create a Pygame window
win = pygame.display.set_mode((1440, 850))

cheering_sound = pygame.mixer.Sound("cheering.mp3")
clapping_sound = pygame.mixer.Sound("claps.mp3")
over_sound = pygame.mixer.Sound("game-over.mp3")
beep_sound = pygame.mixer.Sound("beep_sound.mp3")


class HandDetector:
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=self.mode, max_num_hands=self.maxHands,
                                        min_detection_confidence=self.detectionCon,
                                        min_tracking_confidence=self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):
        lmlist = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmlist.append((id, cx, cy))
                if draw:
                    cv2.circle(img, (cx, cy), 7, (255, 255, 130), cv2.FILLED)
        return lmlist

    def fingersUp(self, lmlist):
        fingers = []
        tipIds = [4, 8, 12, 16, 20]

        # Thumb
        if lmlist[tipIds[0]][1] > lmlist[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Fingers
        for id in range(1, 5):
            if lmlist[tipIds[id]][2] < lmlist[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers


def display_random_images(image_dir, images, num_images=8, frame_width=500, frame_height=500):
    selected_images = random.sample(images, num_images)

    for image_name in selected_images:
        image_path = os.path.join(image_dir, image_name)
        image = cv2.imread(image_path)

        if image is None:
            print(f"Error loading image {image_name}")
            continue

        resized_image = cv2.resize(image, (frame_width, frame_height))

        # Convert image to RGB
        image_rgb = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)

        # Convert to Pygame surface
        image_surface = pygame.surfarray.make_surface(image_rgb)

        # Flip the image surface vertically
        image_surface = pygame.transform.flip(image_surface, False, True)

        win.fill((255, 255, 255))  # Set the background to white
        win.blit(image_surface, ((win.get_width() - frame_width) // 2, (win.get_height() - frame_height) // 2))
        pygame.display.update()


        pygame.time.delay(1000)

    return selected_images

def show_countdown(win, countdown_images, beep_sound, delay=1000):
    for image_name in countdown_images:
        image_path = os.path.join('.', image_name)
        image = cv2.imread(image_path)

        if image is None:
            print(f"Error loading countdown image {image_name}")
            continue

        resized_image = cv2.resize(image, (500, 500))
        image_rgb = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
        image_surface = pygame.surfarray.make_surface(image_rgb)

        # Flip the image surface vertically
        image_surface = pygame.transform.flip(image_surface, False, True)

        # Display the countdown image on the white background
        win.fill((255, 255, 255))
        win.blit(image_surface, ((win.get_width() - 500) // 2, (win.get_height() - 500) // 2))
        pygame.display.update()

        # Play the beep sound
        beep_sound.play()

        # Wait for the specified delay
        pygame.time.delay(delay)

def gesture_to_image_name(fingers, predefined_gestures):
    for gesture, pattern in predefined_gestures.items():
        if fingers == pattern:
            return gesture
    return None

def display_text_on_screen(win, text, font_size=64):
    if not pygame.font.get_init():
        print("Font system not initialized. Cannot display text.")
        return

    try:
        font = pygame.font.Font(None, font_size)
        text_surface = font.render(text, True, (0, 0, 0))
        win.fill((255, 255, 255))  # Set the background to white
        win.blit(text_surface, ((win.get_width() - text_surface.get_width()) // 2,
                                (win.get_height() - text_surface.get_height()) // 2))
        pygame.display.update()
    except pygame.error as e:
        print(f"Error rendering text: {e}")

# def display_text_on_screen(win, text, font_size=64):
#     font = pygame.font.Font(None, font_size)
#     text_surface = font.render(text, True, (0, 0, 0))
#     win.fill((255, 255, 255))  # Set the background to white
#     win.blit(text_surface, ((win.get_width() - text_surface.get_width()) // 2,
#                             (win.get_height() - text_surface.get_height()) // 2))
#     pygame.display.update()

def main():
    predefined_gestures = {
        'Thumbs Up': [1, 0, 0, 0, 0],
        'Index Up': [0, 1, 0, 0, 0],
        'Peace': [0, 1, 1, 0, 0],
        'Rock and Roll': [1, 1, 0, 0, 1],
        'Fist': [0, 0, 0, 0, 0],
        'five': [1, 1, 1, 1, 1],
        'middle_finger': [0, 0, 1, 0, 0],
        'pinky': [0, 0, 0, 0, 1],
        'three': [0, 1, 1, 1, 0],
        'thumb_three': [1, 1, 1, 0, 0],
        'L': [1, 1, 0, 0, 0],
        'pinky_three': [0, 0, 1, 1, 1],
        'four': [0, 1, 1, 1, 1],
        'middle down three': [0, 1, 0, 1, 1],
        'call sign': [1, 0, 0, 0, 1],
        'joint_two': [0, 0, 0, 1, 1],
    }

    image_dir = '.'
    images = [
        'fist.png', 'index_up.jpg', 'peace.png', 'three.jpeg', 'thumbs_up.jpeg', 'rock_and_roll.jpeg', 'L.jpeg',
        'call_me.jpeg', 'pinky.jpg', 'thumb_three.jng', 'joint_two.jpeg', 'five.jpeg', 'four.jpg'
    ]

    selected_images = display_random_images(image_dir, images)

    image_to_gesture = {
        'fist.png': 'Fist',
        'index_up.jpg': 'Index Up',
        'peace.png': 'Peace',
        'rock_and_roll.jpeg': 'Rock and Roll',
        'three.jpeg': 'three',
        'thumbs_up.jpeg': 'Thumbs Up',
        'L.jpeg': 'L',
        'call_me.jpeg': 'call sign',
        'pinky.jpg': 'pinky',
        'thumb_three.jng': 'thumb_three',
        'joint_two.jpeg': 'joint_two',
        'five.jpeg': 'five',
        'four.jpg': 'four',
    }

    countdown_images = ['3.jpg', '2.jpg', '1.jpg']

    # Display countdown before capturing gestures
    show_countdown(win, countdown_images, beep_sound)

    # Ensure the selected images map to gestures without repetition
    expected_gestures = [image_to_gesture[img] for img in selected_images]
    print(f"Expected Gestures: {expected_gestures}")

    # Capture real-time gestures
    cap = cv2.VideoCapture(0)
    detector = HandDetector()
    captured_gestures = []
    consistent_gesture_start = None
    consistent_gesture = None

    running = True
    while running and len(captured_gestures) < len(expected_gestures):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        success, img = cap.read()
        if not success:
            break

        img = detector.findHands(img)
        lmlist = detector.findPosition(img)

        if len(lmlist) != 0:
            fingers = detector.fingersUp(lmlist)
            gesture_name = gesture_to_image_name(fingers, predefined_gestures)


            if gesture_name and gesture_name in expected_gestures:
                if consistent_gesture_start is None or gesture_name != consistent_gesture:
                    consistent_gesture_start = time.time()
                    consistent_gesture = gesture_name
                elif time.time() - consistent_gesture_start >= 1:
                    captured_gestures.append(gesture_name)
                    # display_text_on_screen(win, f"Gesture: {gesture_name}", font_size=64)
                    print(f"Gesture: {gesture_name}")
                    beep_sound.play()
                    pygame.time.delay(1000)
                    consistent_gesture_start = None
                    consistent_gesture = None
            else:
                if consistent_gesture_start is None or gesture_name != consistent_gesture:
                    consistent_gesture_start = time.time()
                    consistent_gesture = gesture_name
                elif time.time() - consistent_gesture_start >= 1:
                    captured_gestures.append("Random")
                    print("Gesture: Random")
                    beep_sound.play()
                    pygame.time.delay(1000)
                    consistent_gesture_start = None
                    consistent_gesture = None


        # Show real-time camera feed in Pygame window
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        imgSurface = pygame.surfarray.make_surface(imgRGB)
        imgSurface = pygame.transform.rotate(imgSurface, -90)
        imgSurface = pygame.transform.flip(imgSurface, True, False)
        win.fill((255, 255, 255))  # Set the background to white
        win.blit(imgSurface, ((win.get_width() - imgSurface.get_width()) // 2,
                              (win.get_height() - imgSurface.get_height()) // 2))
        pygame.display.update()

    cap.release()

    correct_count = sum([1 for i in range(len(expected_gestures)) if i < len(captured_gestures) and expected_gestures[i] == captured_gestures[i]])

    if correct_count == 8:
        display_text_on_screen(win, "You win 3 candies!", 64)
        cheering_sound.play()
    elif correct_count >= 5:
        display_text_on_screen(win, "You win 2 candies!", 64)
        clapping_sound.play()
    elif correct_count >= 4:
        display_text_on_screen(win, "You win 1 candy!", 64)
        clapping_sound.play()
    else:
        display_text_on_screen(win, "Keep practicing!", 64)
        over_sound.play()

    pygame.time.delay(5000)

    pygame.quit()


if __name__ == "__main__":
    main()
