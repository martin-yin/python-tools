import argparse
import os

# 获取标签文件夹下的所有 text 标准文件
def get_labels(folder_path):
    txt_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
    return txt_files

def get_images_bylabels(folder_path, labels):
    img_files = [f for f in os.listdir(folder_path) if f.endswith('.jpg')]
    return img_files

def main():
    parser = argparse.ArgumentParser(description='yolov8-datasets-transfrom')
    parser.add_argument('image_folder', help='图片文件夹地址', required=True)
    parser.add_argument('labels_file', help='labels文件地址', required=True)
    args = parser.parse_args()

if __name__ == '__main__':
    # main()
    labels = get_labels("C:\\Users\\martin-yin\\Desktop\\已经打标后整理完成的csgo-chicke样本\\valid\\labels")
    get_images_bylabels("", labels)
