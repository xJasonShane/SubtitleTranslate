"""字幕翻译工具入口文件"""
import sys
from app.gui.main_window import MainWindow

def main():
    """主函数"""
    app = MainWindow()
    app.mainloop()
    
if __name__ == "__main__":
    main()