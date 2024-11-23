import cv2
import os
from PIL import Image
import pytesseract

def play_video_frame_by_frame(video_path):
    # Open the video file
    print("'n' for next")
    print("'p' for previous")
    print("'s' to select a frame. Select the area in new window and Hit 'Enter'")
    print("'j' to jump, then go to terminal to provide the frame number")
    print("'q' to quit.")
    cap = cv2.VideoCapture(video_path)


    folder_path = "text_collect"
    crop_image_name = f"./{folder_path}/cropped_output.jpg"
    
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    if not cap.isOpened():
        print("Error: Unable to open the video.")
        return

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Total Frames: {total_frames}")

    current_frame = 0

    while cap.isOpened():
        cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame)
        ret, frame = cap.read()

        if not ret:
            print("End of video or unable to fetch the frame.")
            break

        cv2.imshow('Video Frame by Frame', frame)
        print(f"Current Frame: {current_frame}/{total_frames}")

        # Handle keyboard inputs
        key = cv2.waitKey(0) & 0xFF

        if key == ord('n'):  # Go to the next frame
            current_frame += 1
        elif key == ord('p'):  # Go to the previous frame
            current_frame = max(0, current_frame - 1)
        elif key == ord('q'):  # Quit the video
            print("Exiting...")
            break
        elif key == ord('j'):  # Jump to a specific frame
            frame_number = input("Enter frame number to jump to: ")
            if frame_number.isdigit():
                frame_number = int(frame_number)
                if 0 <= frame_number < total_frames:
                    current_frame = frame_number
                else:
                    print("Invalid frame number. Please try again.")
            else:
                print("Invalid input. Please enter a number.")
        elif key == ord('s'):  # Select for save
            roi = cv2.selectROI("Select Area", frame, fromCenter=False, showCrosshair=True)
            cv2.destroyWindow("Select Area") 

            x, y, w, h = roi  # Unpack the ROI coordinates
            cropped_image = frame[int(y):int(y+h), int(x):int(x+w)]

            # Save the cropped image
            cv2.imwrite(crop_image_name, cropped_image)
        else:
            print("Invalid key. Use 'n' for next, 'p' for previous, 'j' to jump, 'q' to quit.")

    cap.release()
    cv2.destroyAllWindows()

    image = Image.open(crop_image_name)
    text = pytesseract.image_to_string(image)
    
    f = open(f"{folder_path}/last_text.txt", "w+")
    f.write(text)
    f.close()

# Example usage
video_path = 'Arrest001_x264.mp4'  # Replace with your video file path
play_video_frame_by_frame(video_path)
