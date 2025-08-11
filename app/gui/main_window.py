import os
import json
from tkinter import Tk, Frame, Button, Label, Entry, Text, Scrollbar, filedialog, messagebox, ttk
from app.core import TranslationAPI

class MainWindow(Tk):
    def __init__(self):
        """初始化主窗口"""
        super().__init__()
        self.title("字幕翻译工具")
        self.geometry("800x600")
        
        # 设置变量
        self.subtitle_file = None
        self.subtitle_data = None
        self.target_language = "zh"
        self.api_key = ""
        self.api_secret = ""
        self.translation_platform = "火山翻译"
        self.translation_api = None
        
        # 加载配置
        self.load_config()
        
        # 初始化翻译API
        self.init_translation_api()
        
        # 创建界面
        self.create_widgets()
        
    def create_widgets(self):
        """创建UI组件"""
        # 创建选项卡控件
        self.tab_control = ttk.Notebook(self)
        
        # 字幕翻译选项卡
        self.translate_tab = Frame(self.tab_control)
        self.tab_control.add(self.translate_tab, text="字幕翻译")
        
        # 软件设置选项卡
        self.settings_tab = Frame(self.tab_control)
        self.tab_control.add(self.settings_tab, text="软件设置")
        
        self.tab_control.pack(expand=1, fill="both")
        
        # 设置字幕翻译选项卡
        self.setup_translate_tab()
        
        # 设置软件设置选项卡
        self.setup_settings_tab()
        
    def setup_translate_tab(self):
        """设置字幕翻译选项卡"""
        # 文件选择区域
        file_frame = Frame(self.translate_tab)
        file_frame.pack(fill="x", padx=10, pady=5)
        
        Label(file_frame, text="字幕文件: ").pack(side="left", padx=5)
        
        self.file_path_var = Entry(file_frame, width=50)
        self.file_path_var.pack(side="left", padx=5, expand=True, fill="x")
        
        Button(file_frame, text="选择文件", command=self.select_subtitle_file).pack(side="right", padx=5)
        
        # 语言选择区域
        lang_frame = Frame(self.translate_tab)
        lang_frame.pack(fill="x", padx=10, pady=5)
        
        Label(lang_frame, text="目标语言: ").pack(side="left", padx=5)
        
        self.lang_var = ttk.Combobox(lang_frame, values=["zh", "en", "ja", "ko", "fr", "de"], width=10)
        self.lang_var.current(0)
        self.lang_var.pack(side="left", padx=5)
        
        Button(lang_frame, text="翻译", command=self.translate_subtitle).pack(side="right", padx=5)
        
        # 文本显示区域
        text_frame = Frame(self.translate_tab)
        text_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # 原始文本区域
        Label(text_frame, text="原始文本").pack(anchor="w")
        self.original_text = Text(text_frame, height=10, wrap="word")
        scrollbar1 = Scrollbar(text_frame, command=self.original_text.yview)
        self.original_text.configure(yscrollcommand=scrollbar1.set)
        self.original_text.pack(side="left", fill="both", expand=True)
        scrollbar1.pack(side="left", fill="y")
        
        # 翻译文本区域
        Label(text_frame, text="翻译文本").pack(anchor="w")
        self.translated_text = Text(text_frame, height=10, wrap="word")
        scrollbar2 = Scrollbar(text_frame, command=self.translated_text.yview)
        self.translated_text.configure(yscrollcommand=scrollbar2.set)
        self.translated_text.pack(side="left", fill="both", expand=True)
        scrollbar2.pack(side="left", fill="y")
        
        # 操作按钮区域
        btn_frame = Frame(self.translate_tab)
        btn_frame.pack(fill="x", padx=10, pady=5)
        
        Button(btn_frame, text="导出", command=self.export_subtitle).pack(side="right", padx=5)
        Button(btn_frame, text="应用更改", command=self.apply_changes).pack(side="right", padx=5)
        
    def setup_settings_tab(self):
        """设置软件设置选项卡"""
        # API设置区域
        api_frame = Frame(self.settings_tab)
        api_frame.pack(fill="x", padx=10, pady=10)
        
        Label(api_frame, text="翻译平台: ").grid(row=0, column=0, sticky="w", pady=5)
        self.platform_var = ttk.Combobox(api_frame, values=["火山翻译"], width=20)
        self.platform_var.current(0)
        self.platform_var.grid(row=0, column=1, sticky="w", pady=5)
        
        Label(api_frame, text="API Key: ").grid(row=1, column=0, sticky="w", pady=5)
        self.api_key_var = Entry(api_frame, width=40, show="*")
        self.api_key_var.grid(row=1, column=1, sticky="w", pady=5)
        self.api_key_var.insert(0, self.api_key)
        
        Label(api_frame, text="API Secret: ").grid(row=2, column=0, sticky="w", pady=5)
        self.api_secret_var = Entry(api_frame, width=40, show="*")
        self.api_secret_var.grid(row=2, column=1, sticky="w", pady=5)
        self.api_secret_var.insert(0, self.api_secret)
        
        # 按钮区域
        btn_frame = Frame(self.settings_tab)
        btn_frame.pack(fill="x", padx=10, pady=10)
        
        Button(btn_frame, text="保存设置", command=self.save_settings).pack(side="left", padx=5)
        Button(btn_frame, text="重置", command=self.reset_settings).pack(side="left", padx=5)
        
        # 关于信息区域
        about_frame = Frame(self.settings_tab)
        about_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        Label(about_frame, text="字幕翻译工具 v1.0.0").pack(anchor="w", pady=2)
        Label(about_frame, text="作者: xJasonShane").pack(anchor="w", pady=2)
        Label(about_frame, text="许可证: MIT").pack(anchor="w", pady=2)
        Label(about_frame, text="GitHub: https://github.com/xJasonShane/SubtitleTranslate").pack(anchor="w", pady=2)
        
    def select_subtitle_file(self):
        """选择字幕文件"""
        file_path = filedialog.askopenfilename(
            filetypes=[("字幕文件", "*.srt *.ass"), ("所有文件", "*.*")]
        )
        if file_path:
            self.file_path_var.delete(0, "end")
            self.file_path_var.insert(0, file_path)
            self.subtitle_file = file_path
            self.load_subtitle()
            
    def load_subtitle(self):
        """加载字幕文件"""
        try:
            import pysrt
            file_ext = os.path.splitext(self.subtitle_file)[1].lower()
            if file_ext == ".srt":
                self.subtitle_data = pysrt.open(self.subtitle_file)
            elif file_ext == ".ass":
                # 这里需要实现ASS文件解析，pysrt可能不支持
                messagebox.showerror("错误", "暂时不支持ASS格式文件")
                return
            else:
                messagebox.showerror("错误", "不支持的文件格式")
                return
            
            # 显示字幕内容
            self.display_subtitle()
        except Exception as e:
            messagebox.showerror("错误", f"加载字幕文件失败: {str(e)}")
            
    def display_subtitle(self):
        """显示字幕内容"""
        self.original_text.delete(1.0, "end")
        self.translated_text.delete(1.0, "end")
        
        for i, subtitle in enumerate(self.subtitle_data):
            self.original_text.insert("end", f"{i+1}. {subtitle.text}\n\n")
            
    def translate_subtitle(self):
        """翻译字幕"""
        if not self.subtitle_data:
            messagebox.showwarning("警告", "请先选择并加载字幕文件")
            return
        
        if not self.api_key or not self.api_secret:
            messagebox.showwarning("警告", "请先在设置中配置API密钥")
            return
        
        self.target_language = self.lang_var.get()
        
        try:
            # 清空翻译文本区域
            self.translated_text.delete(1.0, "end")
            
            # 翻译每个字幕
            for i, subtitle in enumerate(self.subtitle_data):
                translated_text = self.call_translation_api(subtitle.text)
                subtitle.translated_text = translated_text
                self.translated_text.insert("end", f"{i+1}. {translated_text}\n\n")
                
            messagebox.showinfo("成功", "字幕翻译完成")
        except Exception as e:
            messagebox.showerror("错误", f"翻译失败: {str(e)}")
            
    def call_translation_api(self, text):
        """调用翻译API"""
        if not self.translation_api:
            raise Exception("翻译API未初始化，请先配置API密钥")
        
        try:
            return self.translation_api.translate(text, to_lang=self.target_language)
        except Exception as e:
            raise Exception(f"翻译API调用失败: {str(e)}")
            
    def apply_changes(self):
        """应用用户对翻译文本的更改"""
        if not self.subtitle_data:
            messagebox.showwarning("警告", "没有可应用更改的字幕数据")
            return
        
        try:
            # 获取翻译文本区域的内容
            translated_content = self.translated_text.get(1.0, "end").strip()
            
            # 按段落分割
            translated_paragraphs = translated_content.split("\n\n")
            
            # 应用更改到每个字幕
            for i, paragraph in enumerate(translated_paragraphs):
                if i < len(self.subtitle_data):
                    # 提取翻译文本（去掉序号）
                    parts = paragraph.split(". ", 1)
                    if len(parts) > 1:
                        translated_text = parts[1].strip()
                    else:
                        translated_text = paragraph.strip()
                    
                    # 应用到字幕数据
                    self.subtitle_data[i].translated_text = translated_text
            
            messagebox.showinfo("成功", "更改已应用")
        except Exception as e:
            messagebox.showerror("错误", f"应用更改失败: {str(e)}")
            
    def export_subtitle(self):
        """导出翻译后的字幕文件"""
        if not self.subtitle_data:
            messagebox.showwarning("警告", "没有可导出的字幕数据")
            return
        
        save_path = filedialog.asksaveasfilename(
            defaultextension=".srt",
            filetypes=[("SRT文件", "*.srt"), ("所有文件", "*.*")]
        )
        
        if save_path:
            try:
                # 实现导出逻辑
                with open(save_path, 'w', encoding='utf-8') as f:
                    for subtitle in self.subtitle_data:
                        f.write(f"{subtitle.index}\n")
                        f.write(f"{subtitle.start} --> {subtitle.end}\n")
                        if hasattr(subtitle, 'translated_text'):
                            f.write(f"{subtitle.translated_text}\n")
                        else:
                            f.write(f"{subtitle.text}\n")
                        f.write("\n")
                
                messagebox.showinfo("成功", f"字幕已导出到: {save_path}")
            except Exception as e:
                messagebox.showerror("错误", f"导出失败: {str(e)}")
                
    def load_config(self):
        """加载配置"""
        config_file = "config.json"
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.api_key = config.get("api_key", "")
                    self.api_secret = config.get("api_secret", "")
                    self.translation_platform = config.get("platform", "火山翻译")
                    # 初始化翻译API
                    self.init_translation_api()
            except Exception as e:
                print(f"加载配置失败: {str(e)}")
                
    def save_settings(self):
        """保存设置"""
        self.api_key = self.api_key_var.get()
        self.api_secret = self.api_secret_var.get()
        self.translation_platform = self.platform_var.get()
        
        config = {
            "api_key": self.api_key,
            "api_secret": self.api_secret,
            "platform": self.translation_platform
        }
        
        try:
            with open("config.json", 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=4)
            
            # 重新初始化翻译API
            self.init_translation_api()
            
            messagebox.showinfo("成功", "设置已保存")
        except Exception as e:
            messagebox.showerror("错误", f"保存设置失败: {str(e)}")
            
    def reset_settings(self):
        """重置设置"""
        self.api_key = ""
        self.api_secret = ""
        self.translation_platform = "火山翻译"
        
        self.api_key_var.delete(0, "end")
        self.api_secret_var.delete(0, "end")
        self.platform_var.current(0)
        
        # 删除配置文件
        config_file = "config.json"
        if os.path.exists(config_file):
            try:
                os.remove(config_file)
            except Exception as e:
                print(f"删除配置文件失败: {str(e)}")
        
        # 重新初始化翻译API
        self.init_translation_api()
        
        messagebox.showinfo("成功", "设置已重置")
        
    def init_translation_api(self):
        """初始化翻译API"""
        if self.api_key and self.api_secret:
            try:
                self.translation_api = TranslationAPI(
                    self.translation_platform,
                    self.api_key,
                    self.api_secret
                )
            except Exception as e:
                print(f"初始化翻译API失败: {str(e)}")
                self.translation_api = None
        else:
            self.translation_api = None