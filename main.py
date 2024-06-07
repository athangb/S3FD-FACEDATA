from utility import install_required_packages, download_youtube_video, extract_faces_from_videos, mask_images
from helper import check_directory_exists, create_directories

def main():
    install_required_packages()
    
    create_directories(['/content/input', '/content/trimdata', '/content/facedata', '/content/output_mask'])
    
    if not check_directory_exists('/content/input'):
        print("Input directory does not exist.")
        return

    download_youtube_video(
        output_file_path="/content/input/video.mp4",
        url="https://www.youtube.com/watch?v=_V6_JsqWG0o&list=RD_V6_JsqWG0o&start_radio=1",
        resolution="1080p",
        start=10,
        end=20,
        trim_file="trimdata/file1.mp4"
    )
    
    extract_faces_from_videos('/content/trimdata', '/content/facedata')
    
    mask_images('/content/facedata', '/content/output_mask')

if __name__ == "__main__":
    main()
