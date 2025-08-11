"""应用程序入口点"""
from app.gui.main_window import MainWindow
import sys

def main():
    """主函数"""
    app = MainWindow()
    app.mainloop()
    
if __name__ == "__main__":
    main()