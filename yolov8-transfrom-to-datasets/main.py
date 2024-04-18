import argparse
import os
import shutil
import os.path

yolov8_image_ext = ['.jpg', '.jpeg', '.png', '.tif', '.tiff', '.bmp', '.dng', '.mpo', '.webp', '.pfm']
yolov8_label_ext = '.txt'

global image_folder
global label_folder

def get_labels(folder_path):
    global label_folder 
    label_folder = folder_path
    txt_files = [f for f in os.listdir(folder_path) if f.endswith(yolov8_label_ext)]
    return txt_files

def get_images_by_labels(folder_path, labels):
    global image_folder 
    image_folder = folder_path
    img_files = []

    for label in labels:
        label_name, _ = os.path.splitext(label)
        for ext in yolov8_image_ext:
            img_file = label_name + ext
            if os.path.isfile(os.path.join(folder_path, img_file)):
                img_files.append(img_file)
                break

    return img_files


def create_dataset_folder(folder_path, dataset_type, img_files):
    dataset_path = os.path.join(folder_path, dataset_type)
    labels_path = os.path.join(dataset_path, 'labels')
    images_path = os.path.join(dataset_path, 'images')
    
    os.makedirs(images_path, exist_ok=True)
    os.makedirs(labels_path, exist_ok=True)

    for img_name in img_files:
        label_name = os.path.splitext(img_name)[0] + yolov8_label_ext
        img_src = os.path.join(image_folder, img_name) 
        img_dst = os.path.join(images_path, img_name)
        label_src = os.path.join(label_folder, label_name)
        label_dst = os.path.join(labels_path, label_name)
        shutil.copy(img_src, img_dst)
        shutil.copy(label_src, label_dst)

def main():
    parser = argparse.ArgumentParser(description='yolov8-datasets-transform')
    parser.add_argument('labels_file', help='labels文件地址')
    parser.add_argument('image_folder', help='图片文件夹地址')
    parser.add_argument('--output_folder', default='datasets', help='数据集存储路径')
    parser.add_argument('--ratio', choices=['7:3', '7:2:1'], default='7:3', help='训练集、验证集和测试集的比例')
    args = parser.parse_args()
    labels = get_labels(args.labels_file)

    if not labels:
        print("没有在当前文件夹下找到 txt 文件", "路径:f{args.labels_file}")
        return
    img_files = get_images_by_labels(args.image_folder, labels)
    if not img_files:
        print("没有在当前文件夹下找到 jpg, jpeg', png, tif, tiff, bmp, dng, mpo, webp, pfm 图片文件",  "路径:f{args.image_folder}")
        return

    if args.ratio == '7:3':
        num_train = int(len(img_files) * 0.7)
        train_set = img_files[:num_train]
        valid_set = img_files[num_train:]
        test_set = []
    else:
        num_train = int(len(img_files) * 0.7)
        num_valid = int(len(img_files) * 0.2)
        train_set = img_files[:num_train]
        valid_set = img_files[num_train:num_train + num_valid]
        test_set = img_files[num_train + num_valid:]

    print("Trains:", len(train_set))
    create_dataset_folder(args.output_folder, "train", train_set)
    print("Valids:", len(valid_set))
    create_dataset_folder(args.output_folder, "val", valid_set)
    print("Tests:", len(test_set))
    create_dataset_folder(args.output_folder,"test", test_set)

main()
