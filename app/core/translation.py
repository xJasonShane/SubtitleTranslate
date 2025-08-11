import time
import hashlib
import base64
import json
import requests

class TranslationAPI:
    def __init__(self, platform, api_key, api_secret):
        """初始化翻译API
        Args:
            platform: 翻译平台
            api_key: API密钥
            api_secret: API密钥密码
        """
        self.platform = platform
        self.api_key = api_key
        self.api_secret = api_secret
        
        # 设置API端点
        if platform == "火山翻译":
            self.api_url = "https://translate.volcengineapi.com"
        else:
            raise ValueError(f"不支持的翻译平台: {platform}")
        
    def translate(self, text, from_lang="auto", to_lang="zh"):
        """翻译文本
        Args:
            text: 要翻译的文本
            from_lang: 源语言，默认为自动检测
            to_lang: 目标语言，默认为中文
        Returns:
            翻译后的文本
        """
        if self.platform == "火山翻译":
            return self._volc_translate(text, from_lang, to_lang)
        else:
            raise ValueError(f"不支持的翻译平台: {self.platform}")
        
    def _volc_translate(self, text, from_lang="auto", to_lang="zh"):
        """火山翻译API调用
        Args:
            text: 要翻译的文本
            from_lang: 源语言
            to_lang: 目标语言
        Returns:
            翻译后的文本
        """
        # 参考火山翻译API文档：https://www.volcengine.com/docs/4640/65067
        # 准备请求参数
        timestamp = str(int(time.time()))
        nonce = str(int(time.time() * 1000))
        
        # 构造签名
        signature = self._generate_volc_signature(timestamp, nonce)
        
        # 构造请求头
        headers = {
            "X-Date": timestamp,
            "X-Nonce": nonce,
            "X-Content-Sha256": self._compute_sha256(text),
            "Authorization": f"HMAC-SHA256 Credential={self.api_key}, SignedHeaders=content-type;x-date;x-nonce, Signature={signature}",
            "Content-Type": "application/json"
        }
        
        # 构造请求体
        body = {
            "TargetLanguage": to_lang,
            "SourceLanguage": from_lang,
            "TextList": [text]
        }
        
        # 发送请求
        try:
            response = requests.post(
                f"{self.api_url}/api/v2/translate/text",
                headers=headers,
                json=body
            )
            
            # 处理响应
            if response.status_code == 200:
                result = response.json()
                if result.get("ResponseMetadata", {}).get("Error"):
                    raise Exception(f"翻译API错误: {result['ResponseMetadata']['Error']['Message']}")
                
                translations = result.get("TranslationList", [])
                if translations and len(translations) > 0:
                    return translations[0].get("Translation", text)
                else:
                    return text
            else:
                raise Exception(f"翻译API请求失败: 状态码 {response.status_code}, 响应内容 {response.text}")
        except Exception as e:
            raise Exception(f"火山翻译API调用失败: {str(e)}")
        
    def _generate_volc_signature(self, timestamp, nonce):
        """生成火山翻译API签名
        Args:
            timestamp: 时间戳
            nonce: 随机数
        Returns:
            签名字符串
        """
        # 构造签名字符串
        sign_str = f"POST\n/api/v2/translate/text\n{timestamp}\n{nonce}\n"
        
        # 使用HMAC-SHA256算法生成签名
        key = self.api_secret.encode("utf-8")
        message = sign_str.encode("utf-8")
        
        import hmac
        signature = hmac.new(key, message, digestmod=hashlib.sha256).digest()
        
        # 对签名进行Base64编码
        return base64.b64encode(signature).decode("utf-8")
        
    def _compute_sha256(self, text):
        """计算文本的SHA256哈希值
        Args:
            text: 文本内容
        Returns:
            SHA256哈希值
        """
        sha256 = hashlib.sha256()
        sha256.update(text.encode("utf-8"))
        return base64.b64encode(sha256.digest()).decode("utf-8")