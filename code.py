import cv2
import numpy as np


def process_frame(frame):
    frame = cv2.flip(frame, 0)

    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

   
    color_ranges = {
        'red': ([0, 150, 80], [10, 255, 255]),
        'green': ([40, 100, 100], [80, 255, 255]),
        'blue': ([90, 50, 50], [110, 255, 255]),  
        'yellow': ([20, 150, 150], [30, 255, 255])
    }

    for color, (lower, upper) in color_ranges.items():
        lower = np.array(lower, dtype=np.uint8)
        upper = np.array(upper, dtype=np.uint8)

        mask = cv2.inRange(hsv, lower, upper)
        mask = cv2.medianBlur(mask, 7) 

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            contour_area = cv2.contourArea(cnt)

            
            if contour_area > 500 and contour_area < 10000: 
                if len(cnt) >= 5: 
                    ellipse = cv2.fitEllipse(cnt)
                    (center, axes, angle) = ellipse

                    min_radius = 20  
                    max_radius = 120  
                    if min(axes) > min_radius and max(axes) < max_radius:
                        # Draw the ellipse on the frame
                        cv2.ellipse(frame, ellipse, (0, 255, 0), 2)
                        cv2.putText(frame, color, (int(center[0]), int(center[1]) - 10),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    return frame


def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Couldn't open the video.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("End of video or error reading frame.")
            break

        frame = process_frame(frame)
        cv2.imshow('Processed Video', frame)

        if cv2.waitKey(30) & 0xFF == ord('q'):  # Press 'q' to quit
            break

    cap.release()
    cv2.destroyAllWindows()


def process_webcam():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Couldn't access the webcam.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Couldn't read the frame.")
            break

        frame = process_frame(frame)
        cv2.imshow('Live Webcam', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    mode = input
    if mode == 'video':
        video_path = "C:\\Users\\black\\Downloads\\test subjects\\c.mov"  # Set file path directly
        process_video(video_path)
    elif mode == 'webcam':
        process_webcam()
    else:
        print("Invalid option. Please enter 'video' or 'webcam'.")
