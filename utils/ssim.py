import cv2
from skimage.metrics import structural_similarity as ssim

def calculate_video_ssim(original_video_path, transmitted_video_path):
    cap1 = cv2.VideoCapture(original_video_path)
    cap2 = cv2.VideoCapture(transmitted_video_path)
    scores = []

    while cap1.isOpened() and cap2.isOpened():
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()

        if not ret1 or not ret2:
            break

        gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

        if gray1.shape != gray2.shape:
            gray2 = cv2.resize(gray2, (gray1.shape[1], gray1.shape[0]))


        score, _ = ssim(gray1, gray2, full=True)
        scores.append(score)

    cap1.release()
    cap2.release()

    return sum(scores) / len(scores) if scores else 0

if __name__ == "__main__":
    original_video = "share/input/testmedia/test.y4m"
    transmitted_video = "share/output/trace/outvideo_dummy.y4m"
    average_ssim = calculate_video_ssim(original_video, transmitted_video)
    print("Average SSIM:", average_ssim)
