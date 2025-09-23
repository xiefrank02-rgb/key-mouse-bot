import pyautogui
import random
import time
import sys

def main():
    # 禁用PyAutoGUI的安全功能（防止鼠标移到左上角终止程序）
    pyautogui.FAILSAFE = False
    
    print("自动鼠标移动脚本已启动...")
    print("按 Ctrl+C 停止脚本")
    
    try:
        while True:
            # 生成30-60秒之间的随机等待时间
            wait_time = random.uniform(10, 30)
            print(f"将在 {wait_time:.1f} 秒后移动鼠标...")
            
            # 等待设定的时间
            time.sleep(wait_time)
            
            # 获取当前鼠标位置
            current_x, current_y = pyautogui.position()
            
            # 生成微小的随机移动偏移量（-5到5之间）
            move_x = random.randint(-5, 5)
            move_y = random.randint(-5, 5)
            
            # 计算新位置
            new_x = current_x + move_x
            new_y = current_y + move_y
            
            # 确保新位置在屏幕范围内
            screen_width, screen_height = pyautogui.size()
            new_x = max(0, min(new_x, screen_width - 1))
            new_y = max(0, min(new_y, screen_height - 1))
            
            # 移动鼠标到新位置，移动时间0.5秒
            pyautogui.moveTo(new_x, new_y, duration=0.5)
            print(f"鼠标已移动到: ({new_x}, {new_y})")
            # 模拟按多次空格键（例如连续按3次）
            # pyautogui.press('space', presses=1, interval=0.5)  # interval为每次按下的间隔时间（秒）
            # print("已经按下空格")

            
    except KeyboardInterrupt:
        print("\n脚本已停止")
        sys.exit(0)

if __name__ == "__main__":
    main()
