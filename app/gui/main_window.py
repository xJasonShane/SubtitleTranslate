import os
import json
from tkinter import Tk, Frame, Button, Label, Entry, Text, Scrollbar, filedialog, messagebox, ttk
from app.core import TranslationAPI
from app.core.subtitle_processor import SubtitleProcessor

class MainWindow(Tk):
    def __init__(self):
        """初始化主窗口"""
        super().__init__()
        self.title("字幕翻译工具")
        self.geometry("800x600")
        
        # 设置变量
        self.api_key = ""
        self.api_secret = ""
        self.translation_platform = "火山翻译"
        self.translation_api = None
        self.target_language = "zh"
        
        # 初始化业务逻辑层
        self.subtitle_processor = SubtitleProcessor()
        
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
        
        # 创建语言映射字典（显示名称 -> 语言代码）
        self.language_map = {"中文": "zh", "英文": "en", "日语": "ja", "韩语": "ko", "法语": "fr", "德语": "de"}
        # 使用中文名称作为下拉选项
        self.lang_var = ttk.Combobox(lang_frame, values=list(self.language_map.keys()), width=10)
        self.lang_var.current(0)  # 默认选中中文
        self.lang_var.pack(side="left", padx=5)
        
        Button(lang_frame, text="翻译", command=self.translate_subtitle).pack(side="right", padx=5)
        
        # 文本显示区域 - 使用PanedWindow实现可调整大小的面板
        text_frame = Frame(self.translate_tab)
        text_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # 创建垂直分隔面板
        paned_window = ttk.PanedWindow(text_frame, orient="vertical")
        paned_window.pack(fill="both", expand=True)
        
        # 原始文本区域
        original_frame = Frame(paned_window)
        paned_window.add(original_frame, weight=1)  # 设置权重为1
        
        Label(original_frame, text="原始文本").pack(anchor="w")
        self.original_text = Text(original_frame, wrap="word")
        scrollbar1 = Scrollbar(original_frame, command=self.original_text.yview)
        self.original_text.configure(yscrollcommand=scrollbar1.set)
        self.original_text.pack(side="left", fill="both", expand=True)
        scrollbar1.pack(side="left", fill="y")
        
        # 翻译文本区域
        translated_frame = Frame(paned_window)
        paned_window.add(translated_frame, weight=1)  # 设置权重为1
        
        Label(translated_frame, text="翻译文本").pack(anchor="w")
        self.translated_text = Text(translated_frame, wrap="word")
        scrollbar2 = Scrollbar(translated_frame, command=self.translated_text.yview)
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
        
        # 版本号按钮，点击检查更新
        # 导入版本号
        from app.version import VERSION
        self.version_btn = Button(about_frame, text=f"字幕翻译工具 v{VERSION}", command=self.check_for_updates, relief="flat", cursor="hand2")
        self.version_btn.pack(anchor="w", pady=2)
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
            self.subtitle_data = self.subtitle_processor.load_subtitle(self.subtitle_file)
            # 显示字幕内容
            self.display_subtitle()
        except Exception as e:
            messagebox.showerror("错误", f"加载字幕文件失败: {str(e)}")
            
    def display_subtitle(self):
        """显示字幕内容"""
        self.original_text.delete(1.0, "end")
        self.translated_text.delete(1.0, "end")
        
        for i, subtitle in enumerate(self.subtitle_processor.subtitle_data):
            self.original_text.insert("end", f"{i+1}. {subtitle.text}\n\n")
            
    def translate_subtitle(self):
        """翻译字幕"""
        if not self.subtitle_processor.subtitle_data:
            messagebox.showwarning("警告", "请先选择并加载字幕文件")
            return
        
        if not self.api_key or not self.api_secret:
            messagebox.showwarning("警告", "请先在设置中配置API密钥")
            return
        
        # 根据选择的中文名称获取对应的语言代码
        self.target_language = self.language_map[self.lang_var.get()]
        
        try:
            # 清空翻译文本区域
            self.translated_text.delete(1.0, "end")
            
            # 翻译字幕
            self.subtitle_processor.translate_subtitle(self.translation_api, self.target_language)
            
            # 显示翻译结果
            for i, subtitle in enumerate(self.subtitle_processor.subtitle_data):
                self.translated_text.insert("end", f"{i+1}. {subtitle.translated_text}\n\n")
                
            messagebox.showinfo("成功", "字幕翻译完成")
        except Exception as e:
            messagebox.showerror("错误", f"翻译失败: {str(e)}")
            
    # 移除不再需要的call_translation_api方法
            
    def apply_changes(self):
        """应用用户对翻译文本的更改"""
        if not self.subtitle_processor.subtitle_data:
            messagebox.showwarning("警告", "没有可应用更改的字幕数据")
            return
        
        try:
            # 获取翻译文本区域的内容
            translated_content = self.translated_text.get(1.0, "end").strip()
            
            # 应用更改
            self.subtitle_processor.apply_changes(translated_content)
            
            messagebox.showinfo("成功", "更改已应用")
        except Exception as e:
            messagebox.showerror("错误", f"应用更改失败: {str(e)}")
            
    def export_subtitle(self):
        """导出翻译后的字幕文件"""
        if not self.subtitle_processor.subtitle_data:
            messagebox.showwarning("警告", "没有可导出的字幕数据")
            return
        
        save_path = filedialog.asksaveasfilename(
            defaultextension=".srt",
            filetypes=[("SRT文件", "*.srt"), ("所有文件", "*.*")]
        )
        
        if save_path:
            try:
                output_path = self.subtitle_processor.export_subtitle(save_path)
                messagebox.showinfo("成功", f"字幕已导出到: {output_path}")
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

    def check_for_updates(self):
        """检查GitHub上的最新版本"""
        import requests
        import webbrowser
        from tkinter import messagebox
        
        from app.version import VERSION
        current_version = VERSION
        github_releases_url = "https://github.com/xJasonShane/SubtitleTranslate/releases"
        github_api_url = "https://api.github.com/repos/xJasonShane/SubtitleTranslate/releases/latest"
        
        # 先弹出确认对话框
        if not messagebox.askyesno("检查更新", "是否检查软件更新?"):
            return  # 用户点击"否"，退出检查
        
        try:
            # 显示正在检查更新
            self.version_btn.config(text="检查更新中...")
            self.update_idletasks()  # 刷新UI
            
            # 打印调试信息
            print(f"检查更新: 请求URL: {github_api_url}")
            
            # 发送请求获取最新版本，添加headers模拟浏览器
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(github_api_url, headers=headers, timeout=15)
            
            # 打印响应状态
            print(f"检查更新: 响应状态码: {response.status_code}")
            print(f"检查更新: 响应内容: {response.text[:200]}...")  # 只打印前200个字符
            
            response.raise_for_status()
            
            # 解析响应
            latest_release = response.json()
            latest_version = latest_release.get("tag_name", f"v{VERSION}").lstrip("v")
            
            # 比较版本
            if self._compare_versions(latest_version, current_version) > 0:
                # 有新版本
                update_msg = f"发现新版本 {latest_version}!\n\n当前版本: {current_version}\n\n是否前往GitHub下载最新版本?"
                if messagebox.askyesno("更新可用", update_msg):
                    webbrowser.open(github_releases_url)
            else:
                # 已是最新版本
                messagebox.showinfo("检查更新", f"当前已是最新版本: {current_version}")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                error_msg = f"GitHub仓库或发布版本不存在: {str(e)}"
                print(f"检查更新错误: {error_msg}")
                messagebox.showerror("资源不存在", error_msg)
                messagebox.showinfo("故障排除", "请确认GitHub仓库地址是否正确，或该仓库尚未发布任何版本")
            else:
                error_msg = f"HTTP错误: {str(e)}"
                print(f"检查更新错误: {error_msg}")
                messagebox.showerror("网络错误", error_msg)
                messagebox.showinfo("故障排除", "请检查您的网络连接，确保可以访问GitHub.com\n或尝试稍后再试")
        except requests.exceptions.RequestException as e:
            error_msg = f"无法连接到GitHub: {str(e)}"
            print(f"检查更新错误: {error_msg}")
            messagebox.showerror("网络错误", error_msg)
            messagebox.showinfo("故障排除", "请检查您的网络连接，确保可以访问GitHub.com\n或尝试稍后再试")
        except ValueError as e:
            messagebox.showerror("数据解析错误", f"无法解析GitHub响应: {str(e)}")
        except Exception as e:
            messagebox.showerror("更新检查失败", f"检查更新时发生错误: {str(e)}")
        finally:
            # 恢复按钮文本
            self.version_btn.config(text=f"字幕翻译工具 v{current_version}")
    
    def _compare_versions(self, version1, version2):
        """比较两个版本号
        返回值:
        - 1: version1 > version2
        - 0: version1 == version2
        - -1: version1 < version2
        """
        # 处理预发布版本标识
        def _parse_version(v):
            parts = v.split('-')
            main_version = parts[0]
            # 解析主版本号为整数列表
            main_parts = [int(x) for x in main_version.split('.') if x.isdigit()]
            # 处理预发布版本
            pre_release = parts[1] if len(parts) > 1 else ''
            return (main_parts, pre_release)
        
        v1_main, v1_pre = _parse_version(version1)
        v2_main, v2_pre = _parse_version(version2)
        
        # 比较主版本号
        if v1_main != v2_main:
            return 1 if v1_main > v2_main else -1
        
        # 主版本号相同，比较预发布版本
        # 正式版本(没有预发布标识)比任何预发布版本都新
        if not v1_pre and v2_pre:
            return 1
        if v1_pre and not v2_pre:
            return -1
        
        # 都有预发布标识，按字母顺序比较
        if v1_pre != v2_pre:
            return 1 if v1_pre > v2_pre else -1
        
        return 0