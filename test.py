import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import json

with open('config.json', 'r') as config_file:
    config_data = json.load(config_file)

# Initialize pose landmarker
try:
    options = vision.PoseLandmarkerOptions(
        base_options=mp.tasks.BaseOptions(model_asset_path='pose_landmarker.task'),
        num_poses=2,  # Rileva fino a 2 persone
        min_pose_detection_confidence=0.3,
        min_pose_presence_confidence=0.3,
        min_tracking_confidence=0.3
    )
    detector = vision.PoseLandmarker.create_from_options(options)
except Exception as e:
    print(f"Errore nella creazione del detector: {e}")
    print("Verifica che 'pose_landmarker.task' esista nel progetto")
    raise

cap = cv2.VideoCapture('videos/' + config_data["VIDEO_SELECTION"] + ".mp4")  # o 0 per webcam
frame_count = 0
skip_frames = 10  # Processa ogni 10 frame

# Colori diversi per persone diverse
colors = [
    (0, 255, 0),      # Verde
    (255, 0, 0),      # Blu
    (0, 0, 255),      # Rosso
    (255, 255, 0),    # Ciano
    (255, 0, 255),    # Magenta
    (0, 255, 255),    # Giallo
]

# Connessioni standard del corpo
connections = [
    (11, 13), (13, 15),  # Braccio sinistro
    (12, 14), (14, 16),  # Braccio destro
    (11, 12),            # Spalle
    (23, 25), (25, 27),  # Gamba sinistra
    (24, 26), (26, 28),  # Gamba destra
    (23, 24),            # Fianchi
]

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1
    if frame_count % skip_frames != 0:
        continue

    # Converti in formato MediaPipe
    mp_image = mp.Image(
        image_format=mp.ImageFormat.SRGB, 
        data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    )

    # Rileva i landmark
    results = detector.detect(mp_image)

    # Disegna i landmark per tutte le persone rilevate
    if results.pose_landmarks:
        for person_idx, person_landmarks in enumerate(results.pose_landmarks):
            # Seleziona colore basato sull'indice della persona
            color = colors[person_idx % len(colors)]
            
            # Disegna i joint (articolazioni)
            for landmark in person_landmarks:
                x = int(landmark.x * frame.shape[1])
                y = int(landmark.y * frame.shape[0])
                
                # Disegna il cerchio con colore per persona
                cv2.circle(frame, (x, y), 5, color, -1)
                # Aggiungi bordo scuro per migliore visibilità
                cv2.circle(frame, (x, y), 5, (0, 0, 0), 1)
            
            # Disegna le connessioni tra i landmark
            for start, end in connections:
                if start < len(person_landmarks) and end < len(person_landmarks):
                    x1 = int(person_landmarks[start].x * frame.shape[1])
                    y1 = int(person_landmarks[start].y * frame.shape[0])
                    x2 = int(person_landmarks[end].x * frame.shape[1])
                    y2 = int(person_landmarks[end].y * frame.shape[0])
                    
                    # Disegna la linea con colore per persona
                    cv2.line(frame, (x1, y1), (x2, y2), color, 2)
            
            # Aggiungi etichetta con ID persona
            cv2.putText(
                frame, 
                f"Person {person_idx + 1}", 
                (10, 30 + person_idx * 25),
                cv2.FONT_HERSHEY_SIMPLEX, 
                0.7, 
                color, 
                2
            )

    # Mostra il numero totale di persone rilevate
    if results.pose_landmarks:
        cv2.putText(
            frame, 
            f"People detected: {len(results.pose_landmarks)}", 
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 
            1, 
            (255, 255, 255), 
            2
        )

    # Mostra il frame
    cv2.imshow("Pose Detection - Multiple People", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()