import os
from app.core.subtitle_parser import SubtitleParser

class SubtitleProcessor:
    """字幕处理器类，处理字幕的加载、翻译和导出"""
    def __init__(self):
        """初始化字幕处理器"""
        self.parser = SubtitleParser()
        self.subtitle_data = None
        self.subtitle_file = None
        
    def load_subtitle(self, file_path):
        """加载字幕文件
        Args:
            file_path: 字幕文件路径
        Returns:
            解析后的字幕数据
        Raises:
            Exception: 加载失败时抛出异常
        """
        if not os.path.exists(file_path):
            raise Exception(f"文件不存在: {file_path}")
        
        self.subtitle_file = file_path
        try:
            self.subtitle_data = self.parser.parse_file(file_path)
            return self.subtitle_data
        except Exception as e:
            raise Exception(f"加载字幕文件失败: {str(e)}")
            
    def translate_subtitle(self, translation_api, target_language):
        """翻译字幕
        Args:
            translation_api: 翻译API实例
            target_language: 目标语言代码
        Returns:
            翻译后的字幕数据
        Raises:
            Exception: 翻译失败时抛出异常
        """
        if not self.subtitle_data:
            raise Exception("没有加载字幕数据")
        
        if not translation_api:
            raise Exception("翻译API未初始化")
        
        try:
            for subtitle in self.subtitle_data:
                translated_text = translation_api.translate(subtitle.text, to_lang=target_language)
                subtitle.translated_text = translated_text
            return self.subtitle_data
        except Exception as e:
            raise Exception(f"翻译字幕失败: {str(e)}")
            
    def apply_changes(self, translated_content):
        """应用用户对翻译文本的更改
        Args:
            translated_content: 用户修改后的翻译内容
        Returns:
            应用更改后的字幕数据
        Raises:
            Exception: 应用更改失败时抛出异常
        """
        if not self.subtitle_data:
            raise Exception("没有可应用更改的字幕数据")
        
        try:
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
            return self.subtitle_data
        except Exception as e:
            raise Exception(f"应用更改失败: {str(e)}")
            
    def export_subtitle(self, output_path):
        """导出翻译后的字幕文件
        Args:
            output_path: 输出文件路径
        Raises:
            Exception: 导出失败时抛出异常
        """
        if not self.subtitle_data:
            raise Exception("没有可导出的字幕数据")
        
        try:
            self.parser.export_subtitle(self.subtitle_data, output_path)
            return output_path
        except Exception as e:
            raise Exception(f"导出字幕失败: {str(e)}")