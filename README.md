# 字幕翻译工具

这是一个基于Python的字幕翻译工具，支持多种常见字幕格式，通过调用翻译API实现字幕的自动翻译，并提供简单易用的GUI界面。

## 功能特点

- 支持SRT格式字幕文件的加载和解析
- 集成火山翻译API，支持多种语言互译
- 提供直观的GUI界面，方便用户操作
- 支持翻译结果的编辑和微调
- 支持翻译后的字幕文件导出

## 安装指南

1. 克隆项目到本地

```bash
https://github.com/xJasonShane/SubtitleTranslate.git
cd SubtitleTranslate
```

2. 创建并激活虚拟环境

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. 安装依赖包

```bash
pip install -r requirements.txt
```

## 使用说明

1. 运行程序

```bash
python subtitle_translate.py
```

2. 在软件设置界面配置火山翻译API密钥

3. 切换到字幕翻译界面，选择要翻译的字幕文件

4. 选择目标语言，点击翻译按钮

5. 查看翻译结果，可以对翻译文本进行微调

6. 点击应用更改按钮，保存修改后的翻译结果

7. 点击导出按钮，将翻译后的字幕保存到指定位置

## 支持的语言

目前支持的目标语言包括：中文(zh)、英文(en)、日语(ja)、韩语(ko)、法语(fr)、德语(de)等。

## 依赖项

- Python 3.7+
- requests
- pysrt
- tkinter

## 许可证

本项目采用MIT许可证，详情请见LICENSE文件。

## 作者

xJasonShane

## GitHub地址

https://github.com/xJasonShane/SubtitleTranslate
