import os
import cv2
import imageio

def save_to_video(output_path, output_video_file, frame_rate=20):
    """
    Save a series of images into a .mp4 video
    @outout_path: the folder that contains images, all the images should be orignized in order
    @output_video_file: the video path, endwith .mp4
    @frame_rate: frame rate
    """
    list_files = os.listdir(output_path)
    all=[]
    for file in list_files:
        all.append(int(file.split('.')[0]))
    all.sort()
    # 拿一张图片确认宽高
    img0 = cv2.imread(os.path.join(output_path, str(all[0])+'.png'))
    # print(img0)
    height, width, layers = img0.shape
    # 视频保存初始化 VideoWriter
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    videowriter = cv2.VideoWriter(output_video_file, fourcc, frame_rate, (width, height))
    # 核心，保存的东西
    for f in all:
        # print("saving..." + f)
        img = cv2.imread(os.path.join(output_path, str(f)+'.png'))
        videowriter.write(img)
    videowriter.release()
    cv2.destroyAllWindows()
    print('Success save %s!' % output_video_file)

def save_hdr(path,files):
    '''
    @ path: save path
    @ files: [H,W,C]
    '''
    imageio.imwrite(path, files, format='hdr')