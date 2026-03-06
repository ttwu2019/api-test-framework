"""
HTTP客户端封装
"""
import requests
import yaml
import os

class HttpClient:
    def __init__(self):
        self.config = self._load_config()
        self.base_url = self.config.get('base_url', '')
        self.headers = self.config.get('headers', {})
    
    def _load_config(self):
        """加载配置文件"""
        config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml')
        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def request(self, method, endpoint, params=None, json=None, headers=None, **kwargs):
        """
        发送HTTP请求
        
        Args:
            method: 请求方法 (GET, POST, etc.)
            endpoint: 接口路径
            params: URL参数
            json: 请求体 (JSON)
            headers: 请求头
            **kwargs: 其他requests参数
        """
        url = f"{self.base_url}{endpoint}"
        
        # 合并请求头
        request_headers = {**self.headers, **(headers or {})}
        
        print(f"\n{'='*50}")
        print(f"请求: {method} {url}")
        print(f"Headers: {request_headers}")
        print(f"JSON: {json}")
        print(f"{'='*50}")
        
        response = requests.request(
            method=method,
            url=url,
            params=params,
            json=json,
            headers=request_headers,
            **kwargs
        )
        
        print(f"\n响应状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        
        return response
    
    def post(self, endpoint, json=None, headers=None, **kwargs):
        """POST请求"""
        return self.request('POST', endpoint, json=json, headers=headers, **kwargs)
    
    def get(self, endpoint, params=None, headers=None, **kwargs):
        """GET请求"""
        return self.request('GET', endpoint, params=params, headers=headers, **kwargs)


# 全局实例
http_client = HttpClient()
