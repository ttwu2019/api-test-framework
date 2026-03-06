"""
门店二维码接口测试
"""
import pytest
import os
import sys
import json

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.http_client import http_client


def load_request_data(filename):
    """从data目录加载请求参数"""
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', filename)
    with open(data_path, 'r', encoding='utf-8') as f:
        return json.load(f)


class TestStoreQrCode:
    """门店H5二维码接口测试"""
    
    def test_get_h5_qrcode(self):
        """
        测试获取门店H5二维码接口
        接口: /miniapp/channel/store/h5QrCode
        方法: POST
        """
        # 加载请求参数
        payload = load_request_data('store_qrcode.json')
        
        # 发送请求
        response = http_client.post(
            endpoint="/ehutong-ehutcore-front-miniapp/miniapp/channel/store/h5QrCode",
            json=payload
        )
        
        # 断言响应状态码
        assert response.status_code == 200, f"期望状态码200，实际{response.status_code}"
        
        # 验证响应内容是图片
        content_type = response.headers.get('Content-Type', '')
        print(f"\nContent-Type: {content_type}")
        
        # 检查是否返回图片
        assert 'image' in content_type.lower(), f"期望返回图片，实际Content-Type: {content_type}"
        
        # 保存图片到报告目录
        if response.content:
            reports_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'reports')
            os.makedirs(reports_dir, exist_ok=True)
            image_path = os.path.join(reports_dir, 'store_qrcode.png')
            with open(image_path, 'wb') as f:
                f.write(response.content)
            print(f"\n图片已保存到: {image_path}")
        
        # 验证图片大小
        assert len(response.content) > 0, "返回的图片内容为空"
        print(f"\n图片大小: {len(response.content)} bytes")
        
        print("\n[Test Passed]")
    
    def test_get_h5_qrcode_with_invalid_store(self):
        """
        测试无效门店ID
        """
        payload = {
            "channelId": "244",
            "storeId": "999999"
        }
        
        response = http_client.post(
            endpoint="/ehutong-ehutcore-front-miniapp/miniapp/channel/store/h5QrCode",
            json=payload
        )
        
        print(f"\n状态码: {response.status_code}")
        print(f"Content-Type: {response.headers.get('Content-Type', '')}")


if __name__ == '__main__':
    pytest.main([__file__, '-v', '-s'])
