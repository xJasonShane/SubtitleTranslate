import os
import pysrt

class SubtitleParser:
    """字幕解析器类，用于解析不同格式的字幕文件"""
    def __init__(self):
        """初始化字幕解析器"""
        pass
        
    def parse_file(self, file_path):
        """解析字幕文件
        Args:
            file_path: 字幕文件路径
        Returns:
            解析后的字幕数据
        Raises:
            Exception: 解析失败时抛出异常
        """
        if not os.path.exists(file_path):
            raise Exception(f"文件不存在: {file_path}")
        
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext == ".srt":
            return self._parse_srt(file_path)
        elif file_ext == ".ass":
            return self._parse_ass(file_path)
        else:
            raise Exception(f"不支持的文件格式: {file_ext}")
        
    def _parse_srt(self, file_path):
        """解析SRT格式字幕
        Args:
            file_path: SRT文件路径
        Returns:
            pysrt.SubRipFile: 解析后的SRT字幕对象
        """
        try:
            return pysrt.open(file_path)
        except Exception as e:
            raise Exception(f"解析SRT文件失败: {str(e)}")
        
    def _parse_ass(self, file_path):
        """解析ASS格式字幕
        Args:
            file_path: ASS文件路径
        Returns:
            list: 解析后的ASS字幕数据列表
        """
        # 这里实现ASS格式解析逻辑
        # 注意：这是一个简化实现，实际ASS格式更复杂
        try:
            subtitle_data = []
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            # 跳过[Script Info]和[V4+ Styles]部分
            i = 0
            while i < len(lines) and not lines[i].startswith("[Events]"):
                i += 1
            
            # 跳过[Events]标题和Format行
            if i < len(lines):
                i += 1
                while i < len(lines) and lines[i].startswith("Format:"):
                    i += 1
            
            # 解析Dialogue行
            while i < len(lines):
                line = lines[i].strip()
                if line.startswith("Dialogue:"):
                    # 格式: Dialogue: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
                    parts = line.split(",", 9)
                    if len(parts) >= 10:
                        start_time = parts[1]
                        end_time = parts[2]
                        text = parts[9]
                        
                        # 创建一个简单的字幕对象
                        subtitle = type('obj', (object,), {
                            'start': start_time,
                            'end': end_time,
                            'text': text
                        })
                        subtitle_data.append(subtitle)
                i += 1
            
            return subtitle_data
        except Exception as e:
            raise Exception(f"解析ASS文件失败: {str(e)}")
        
    def export_subtitle(self, subtitle_data, output_path):
        """导出字幕文件
        Args:
            subtitle_data: 字幕数据
            output_path: 输出文件路径
        Raises:
            Exception: 导出失败时抛出异常
        """
        try:
            file_ext = os.path.splitext(output_path)[1].lower()
            
            if file_ext == ".srt":
                self._export_srt(subtitle_data, output_path)
            elif file_ext == ".ass":
                self._export_ass(subtitle_data, output_path)
            else:
                raise Exception(f"不支持的导出格式: {file_ext}")
        except Exception as e:
            raise Exception(f"导出字幕失败: {str(e)}")
        
    def _export_srt(self, subtitle_data, output_path):
        """导出SRT格式字幕
        Args:
            subtitle_data: 字幕数据
            output_path: 输出文件路径
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            for i, subtitle in enumerate(subtitle_data):
                f.write(f"{i+1}\n")
                f.write(f"{subtitle.start} --> {subtitle.end}\n")
                if hasattr(subtitle, 'translated_text'):
                    f.write(f"{subtitle.translated_text}\n")
                else:
                    f.write(f"{subtitle.text}\n")
                f.write("\n")
        
    def _export_ass(self, subtitle_data, output_path):
        """导出ASS格式字幕
        Args:
            subtitle_data: 字幕数据
            output_path: 输出文件路径
        """
        # 简化实现，实际ASS格式更复杂
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("[Script Info]\n")
            f.write("Title: SubtitleTranslate Export\n")
            f.write("ScriptType: v4.00+\n")
            f.write("WrapStyle: 0\n\n")
            
            f.write("[V4+ Styles]\n")
            f.write("Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n")
            f.write("Style: Default,Arial,20,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,2,2,10,10,10,1\n\n")
            
            f.write("[Events]\n")
            f.write("Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
            
            for subtitle in subtitle_data:
                text = subtitle.translated_text if hasattr(subtitle, 'translated_text') else subtitle.text
                f.write(f"Dialogue: 0,{subtitle.start},{subtitle.end},Default,,0,0,0,,{text}\n")