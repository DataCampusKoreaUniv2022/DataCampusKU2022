'''

'''
from pytube import YouTube
import cv2, os


def video_download():
    url = input('Youtube url: ')
    yt = YouTube(url)
    DOWNLOAD_FOLDER = f"./yt_capture_imgs"

    stream = yt.streams.get_highest_resolution()
    stream.download(DOWNLOAD_FOLDER)

    return yt


def video_capture():
    yt = video_download()
    raw_title = r'{}'.format(yt.title)
    filepath = f"./yt_capture_imgs/{raw_title}.mp4"
    video = cv2.VideoCapture(filepath)

    if not video.isOpened():
        print("Could not Open :", filepath)
        exit(0)

    fps = round(video.get(cv2.CAP_PROP_FPS))
    print(fps)

    try:
        if not os.path.exists(filepath[:-4]):
            os.makedirs(filepath[:-4])
    except OSError:
        print ('Error: Creating directory. ' +  filepath[:-4])

    count = 0
    while(video.isOpened()):
        print(count)
        ret, image = video.read()
        if(int(video.get(1)) % fps == 0): #앞서 불러온 fps 값을 사용하여 1초마다 추출
            cv2.imwrite(filepath[:-4] + f"/frame{count}.jpg", image)
            print('Saved frame number :', str(int(video.get(1))))
            count += 1
            
    video.release()

video_capture()