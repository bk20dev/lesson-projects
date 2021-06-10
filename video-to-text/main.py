import cv2
import numpy as np


def generate_character(array):
    # Convert binary value to decimal
    binary = np.flip([*array[:3, 0], *array[:3, 1], array[3][0], array[3][1]])
    value = int(''.join(map(str, binary)), 2)

    # Return proper unicode character
    return chr(0x2800 + value)


def write_frame(frame, file):
    for row in range(0, frame.shape[0] - 3, 4):
        for col in range(0, frame.shape[1] - 1, 2):
            # Cut a frame in the image
            arr = frame[row:row + 4, col:col + 2]
            arr = np.reshape(arr, (4, 2))

            # Get unicode character
            char = generate_character(arr).encode('utf8')

            # Save the frame in the file
            file.write(char)
        file.write('\n'.encode('utf8'))
    file.write('\n'.encode('utf8'))


def generate_frames(video_path, out_path, dim=(480, 360)):
    video = cv2.VideoCapture(video_path)
    current_frame = 0
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    with open(out_path, "wb+") as out:
        while video.isOpened():
            ret, img = video.read()

            if not ret:
                break

            # Resize the image and then create a grayscale image
            img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
            img = cv2.inRange(img, 0, 100) / 255
            img = img.astype(int)

            # Save the current frame to the file
            write_frame(img, out)

            # Print some information to console
            current_frame += 1
            progress = format(current_frame / total_frames * 100, ".2f")
            print(f'\rGenerated {current_frame} of {total_frames} frames ({progress}%)', end='')


generate_frames("video.mp4", "out.txt", (60, 45))
