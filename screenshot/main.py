import argparse
import os
import uuid
from PIL import Image
import win32api
import keyboard
import time
import dxcam

camera = dxcam.create()

def screenshot(mode, offset=320, save_path='captured_images', is_centered=True, left=0, top=0, right=0, bottom=0):
    timestamp = int(time.time())
    unique_id = str(uuid.uuid4())[:6]  # 生成长度为6的唯一随机字符串，用于区分同一时间戳下的截图
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    if mode == 'fullscreen':
        # 全屏截图模式
        frame = camera.grab()
    elif mode == 'partial':
        # 部分区域截图模式
        screen_size = win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)
        if is_centered:
            center_x, center_y = screen_size[0] / 2, screen_size[1] / 2
            left = max(0, center_x - offset)
            top = max(0, center_y - offset)
            right = min(screen_size[0], center_x + offset)
            bottom = min(screen_size[1], center_y + offset)
            region = (left, top, right, bottom)
            frame = camera.grab(region=region)
    else:
        frame = camera.grab()

    screenshot_path = f'{save_path}/{timestamp}_{unique_id}.png'
    screenshot = Image.fromarray(frame)
    screenshot.save(screenshot_path)
    print(f'截图成功，保存路径为 {screenshot_path}')

def main():
    parser = argparse.ArgumentParser(description='截图程序')
    parser.add_argument('mode', nargs='?', choices=['fullscreen', 'partial'], default='fullscreen', help='截图模式')
    parser.add_argument('--offset', type=int, default=320, help='部分截图的偏移值')
    parser.add_argument('--save_path', default='screenshot_images', help='保存路径')
    parser.add_argument('--is_centered', action='store_true', help='是否以屏幕中心为基准截图')
    parser.add_argument('--left', type=int, default=0, help='部分截图的左边界坐标')
    parser.add_argument('--top', type=int, default=0, help='部分截图的上边界坐标')
    parser.add_argument('--right', type=int, default=0, help='部分截图的右边界坐标')
    parser.add_argument('--bottom', type=int, default=0, help='部分截图的下边界坐标')
    
    args = parser.parse_args()

    # 监听CapsLock键事件
    def on_capslock(event):
        if event.name == 'caps lock' and event.event_type == keyboard.KEY_DOWN:
            screenshot(args.mode, args.offset, args.save_path, args.is_centered, args.left, args.top, args.right, args.bottom)

    # 监听CapsLock键事件
    keyboard.on_press_key('caps lock', on_capslock)

    # 等待Esc键停止程序
    keyboard.wait('esc')

if __name__ == '__main__':
    main()
