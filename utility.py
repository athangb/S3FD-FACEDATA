import os
import subprocess
from pytube import YouTube
from moviepy.video.io.VideoFileClip import VideoFileClip
import cv2
import numpy as np
from sfd_detector import SFDDetector
import glob

def install_required_packages():
    required_packages = [
        "imageio==2.4.1",
        "moviepy",
        "datetime",
        "ffmpeg-python",
        "git+https://github.com/anorak-7/pytube.git"
    ]
    
    for package in required_packages:
        install_package(package)

def install_package(package_name):
    subprocess.check_call([os.sys.executable, "-m", "pip", "install", package_name])

def download_youtube_video(output_file_path, url, resolution, start, end, trim_file):
    yt = YouTube(url)
    yt = yt.streams.filter(res=resolution).first().download(output_path=".", filename=output_file_path)
    trimmed_video = VideoFileClip(output_file_path).subclip(start, end)
    trimmed_video.write_videofile(trim_file)

def extract_faces_from_videos(input_dir, output_dir):
    device = 'cuda'
    detector = SFDDetector(device, path_to_detector='s3fd.pth')
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    for video_file in glob.glob(os.path.join(input_dir, '*.mp4')):
        video_name = os.path.splitext(os.path.basename(video_file))[0]
        video_output_dir = os.path.join(output_dir, video_name)
        
        if not os.path.exists(video_output_dir):
            os.makedirs(video_output_dir)
            
        cap = cv2.VideoCapture(video_file)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        for i in range(frame_count):
            ret, frame = cap.read()
            
            if not ret:
                break
                
            bboxes = detector.detect_from_image(frame)
            
            for j, bbox in enumerate(bboxes):
                x1, y1, x2, y2, score = bbox
                face = frame[int(y1):int(y2), int(x1):int(x2)]
                
                if face.size == 0:
                    continue
                
                output_path = os.path.join(video_output_dir, f'face_{i}_{j}.jpg')
                cv2.imwrite(output_path, face)
                
        cap.release()

def mask_images(input_dir, output_dir):
    for subdir in os.listdir(input_dir):
        subdir_path = os.path.join(input_dir, subdir)
        if not os.path.isdir(subdir_path):
            continue

        out_subdir_path = os.path.join(output_dir, subdir)
        os.makedirs(out_subdir_path, exist_ok=True)

        for filename in os.listdir(subdir_path):
            if not filename.lower().endswith('.jpg'):
                continue

            img_path = os.path.join(subdir_path, filename)
            img = cv2.imread(img_path)
            mask = np.zeros_like(img)

            mask[img.shape[0]//2 + img.shape[0]//5:, :, :] = 255
            mask = cv2.bitwise_not(mask)
            result = cv2.bitwise_and(img, mask)
            out_path = os.path.join(out_subdir_path, filename)
            cv2.imwrite(out_path, result)
