import pyperclip
import webbrowser
import time
import keyboard

def search_selected_text():
    try:
        # 发送Ctrl+C复制选中的文本
        keyboard.press_and_release('ctrl+c')
        # 等待复制操作完成
        time.sleep(0.1)
        
        # 从剪贴板获取文本
        selected_text = pyperclip.paste().strip()
        
        if not selected_text:
            print("没有选中任何文本")
            return
        
        print(f"搜索内容: {selected_text}")
        
        # 构建Google搜索URL
        search_url = f"https://www.google.com/search?q={selected_text}"
        
        # 用默认浏览器打开搜索页面
        webbrowser.open(search_url)
        
    except Exception as e:
        print(f"发生错误: {str(e)}")

if __name__ == "__main__":
    print("请选中要搜索的文本，然后按Ctrl+Shift+G进行搜索...")
    print("按Esc退出程序")
    
    # 注册快捷键Ctrl+Shift+G来触发搜索
    keyboard.add_hotkey('ctrl+shift+g', search_selected_text)
    
    # 保持程序运行，等待快捷键
    keyboard.wait('esc')
    print("程序已退出")
