"""
创建订单和支付接口测试
"""
import pytest
import os
import sys
import json
from datetime import datetime, timedelta

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.http_client import http_client


def load_request_data(filename):
    """从data目录加载请求参数"""
    data_path = os.path.join(os.path.dirname(__file__), '..', 'data', filename)
    with open(data_path, 'r', encoding='utf-8') as f:
        return json.load(f)


class TestCreateOrder:
    """创建订单接口测试"""
    
    # Authorization token
    AUTH_TOKEN = "1323941.eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyTmFtZSI6Im84dkFydDZvX1JVSGh5d1dpYWtGTmxTejVtX1EiLCJleHAiOjE3NzI4NjkyMDgsInVzZXJJZCI6MTMyMzk0MSwidGVybWluYWxUeXBlIjoxMDAwM30.wKdZN1IUtA9s4YNchdOhTQdb9SCl5cKzQ6uNeo-8g5A"
    
    def test_create_order(self):
        """
        测试创建订单接口
        接口: /miniapp/service/usr/new/createOrder
        方法: POST
        """
        # 动态生成时间 - 未来5小时
        future_time = (datetime.now() + timedelta(hours=5)).strftime("%Y-%m-%d %H:%M:%S")
        
        # 加载请求参数并修改动态字段
        payload = load_request_data('create_order.json')
        payload['remark'] = "测试订单-" + future_time
        payload['serviceDates'][0]['homeTime'] = future_time
        
        # 发送请求 (带Authorization header)
        response = http_client.post(
            endpoint="/ehutong-ehutcore-front-miniapp/miniapp/service/usr/new/createOrder",
            json=payload,
            headers={
                "Authorization": self.AUTH_TOKEN
            }
        )
        
        print(f"\n响应状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        # 断言响应状态码
        assert response.status_code == 200, f"期望状态码200，实际{response.status_code}"
        
        # 解析响应JSON
        result = response.json()
        
        # 验证返回code为0
        assert result.get("code") == 0, f"期望code为0，实际{result.get('code')}"
        
        # 验证返回msg
        assert result.get("msg") == "success", f"期望msg为success，实际{result.get('msg')}"
        
        # 验证orderUid存在且不为空
        order_uid = result.get("result", {}).get("orderUid")
        assert order_uid, "orderUid不能为空"
        assert len(order_uid) > 0, "orderUid不能为空字符串"
        
        print(f"\n[OK] 订单创建成功!")
        print(f"[OK] orderUid: {order_uid}")
        
        # 保存orderUid到文件供后续使用
        reports_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'reports')
        os.makedirs(reports_dir, exist_ok=True)
        order_file = os.path.join(reports_dir, 'order_result.txt')
        with open(order_file, 'w', encoding='utf-8') as f:
            f.write(f"orderUid: {order_uid}\n")
            f.write(f"创建时间: {future_time}\n")
            f.write(f"完整响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
        
        print(f"\n[Test Passed]")


class TestOrderPayment:
    """订单支付接口测试"""
    
    # Authorization token
    AUTH_TOKEN = "1323941.eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyTmFtZSI6Im84dkFydDZvX1JVSGh5d1dpYWtGTmxTejVtX1EiLCJleHAiOjE3NzI4NjkyMDgsInVzZXJJZCI6MTMyMzk0MSwidGVybWluYWxUeXBlIjoxMDAwM30.wKdZN1IUtA9s4YNchdOhTQdb9SCl5cKzQ6uNeo-8g5A"
    
    def _create_order_for_payment(self):
        """创建订单并返回orderUid"""
        future_time = (datetime.now() + timedelta(hours=5)).strftime("%Y-%m-%d %H:%M:%S")
        
        payload = load_request_data('create_order.json')
        payload['remark'] = "测试支付订单-" + future_time
        payload['serviceDates'][0]['homeTime'] = future_time
        
        response = http_client.post(
            endpoint="/ehutong-ehutcore-front-miniapp/miniapp/service/usr/new/createOrder",
            json=payload,
            headers={"Authorization": self.AUTH_TOKEN}
        )
        
        result = response.json()
        
        # 检查接口返回是否成功
        if result.get("code") != 0:
            print(f"[ERROR] 创建订单失败: {result.get('msg')}")
            return None
            
        return result.get("result", {}).get("orderUid")
    
    def test_order_payment(self):
        """
        测试订单支付接口
        接口: /miniapp/gold/nurse/usr/pay
        方法: POST
        """
        # 先创建订单获取orderUid
        order_uid = self._create_order_for_payment()
        print(f"\n[INFO] 创建的订单orderUid: {order_uid}")
        assert order_uid, "订单失败，无法获取orderUid"
        
        # 加载支付请求参数
        payload = load_request_data('order_pay.json')
        payload['orduid'] = order_uid
        
        # 发送支付请求
        response = http_client.post(
            endpoint="/ehutong-ehutcore-front-miniapp/miniapp/gold/nurse/usr/pay",
            json=payload,
            headers={"Authorization": self.AUTH_TOKEN}
        )
        
        print(f"\n响应状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        # 断言响应状态码
        assert response.status_code == 200, f"期望状态码200，实际{response.status_code}"
        
        # 解析响应JSON
        result = response.json()
        
        # 验证返回code为0
        assert result.get("code") == 0, f"期望code为0，实际{result.get('code')}"
        
        # 验证返回msg
        assert result.get("msg") == "success", f"期望msg为success，实际{result.get('msg')}"
        
        # 验证支付结果
        payment_result = result.get("result")
        assert payment_result, "支付结果不能为空"
        
        print(f"\n[OK] 订单支付成功!")
        print(f"[OK] 支付结果: {payment_result}")
        print(f"\n[Test Passed]")


class TestNurseFeeOrder:
    """护理员管理费订单接口测试"""
    
    # Authorization token
    AUTH_TOKEN = "1323941.eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyTmFtZSI6Im84dkFydDZvX1JVSGh5d1dpYWtGTmxTejVtX1EiLCJleHAiOjE3NzI4NjkyMDgsInVzZXJJZCI6MTMyMzk0MSwidGVybWluYWxUeXBlIjoxMDAwM30.wKdZN1IUtA9s4YNchdOhTQdb9SCl5cKzQ6uNeo-8g5A"
    
    def _create_nurse_fee_order(self):
        """创建护理员管理费订单并返回orderUid"""
        # 动态生成时间 - 未来5小时
        future_time = (datetime.now() + timedelta(hours=5)).strftime("%Y-%m-%d %H:%M:%S")
        
        # 加载请求参数并修改动态字段
        payload = load_request_data('create_nurse_fee_order.json')
        payload['remark'] = "测试护理员管理费订单-" + future_time
        payload['serviceDates'][0]['homeTime'] = future_time
        
        # 发送请求
        response = http_client.post(
            endpoint="/ehutong-ehutcore-front-miniapp/miniapp/service/usr/new/createOrder",
            json=payload,
            headers={"Authorization": self.AUTH_TOKEN}
        )
        
        result = response.json()
        
        # 检查接口返回是否成功
        if result.get("code") != 0:
            print(f"[ERROR] 创建订单失败: {result.get('msg')}")
            return None
            
        order_uid = result.get("result", {}).get("orderUid")
        print(f"[INFO] 创建的订单orderUid: {order_uid}")
        return order_uid
    
    def test_create_nurse_fee_order(self):
        """
        测试创建护理员管理费订单接口
        接口: /miniapp/service/usr/new/createOrder
        方法: POST
        """
        # 动态生成时间 - 未来5小时
        future_time = (datetime.now() + timedelta(hours=5)).strftime("%Y-%m-%d %H:%M:%S")
        
        # 加载请求参数并修改动态字段
        payload = load_request_data('create_nurse_fee_order.json')
        payload['remark'] = "测试护理员管理费订单-" + future_time
        payload['serviceDates'][0]['homeTime'] = future_time
        
        # 发送请求
        response = http_client.post(
            endpoint="/ehutong-ehutcore-front-miniapp/miniapp/service/usr/new/createOrder",
            json=payload,
            headers={"Authorization": self.AUTH_TOKEN}
        )
        
        print(f"\n响应状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        # 断言响应状态码
        assert response.status_code == 200, f"期望状态码200，实际{response.status_code}"
        
        # 解析响应JSON
        result = response.json()
        
        # 验证返回code为0
        assert result.get("code") == 0, f"期望code为0，实际{result.get('code')}"
        
        # 验证返回msg
        assert result.get("msg") == "success", f"期望msg为success，实际{result.get('msg')}"
        
        # 验证orderUid存在且不为空
        order_uid = result.get("result", {}).get("orderUid")
        assert order_uid, "orderUid不能为空"
        
        print(f"\n[OK] 护理员管理费订单创建成功!")
        print(f"[OK] orderUid: {order_uid}")
        
        print(f"\n[Test Passed]")
        
        return order_uid
    
    def test_nurse_fee_order_payment(self):
        """
        测试护理员管理费订单金币支付接口
        接口: /miniapp/gold/nurse/usr/pay
        方法: POST
        """
        # 先创建订单获取orderUid
        order_uid = self._create_nurse_fee_order()
        assert order_uid, "订单失败，无法获取orderUid"
        print(f"\n[INFO] 护理员管理费订单orderUid: {order_uid}")
        
        # 加载支付请求参数
        payload = load_request_data('order_pay.json')
        payload['orduid'] = order_uid
        
        # 发送支付请求
        response = http_client.post(
            endpoint="/ehutong-ehutcore-front-miniapp/miniapp/gold/nurse/usr/pay",
            json=payload,
            headers={"Authorization": self.AUTH_TOKEN}
        )
        
        print(f"\n响应状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        # 断言响应状态码
        assert response.status_code == 200, f"期望状态码200，实际{response.status_code}"
        
        # 解析响应JSON
        result = response.json()
        
        # 验证返回code为0
        assert result.get("code") == 0, f"期望code为0，实际{result.get('code')}"
        
        # 验证返回msg
        assert result.get("msg") == "success", f"期望msg为success，实际{result.get('msg')}"
        
        # 验证支付结果
        payment_result = result.get("result")
        assert payment_result, "支付结果不能为空"
        
        print(f"\n[OK] 护理员管理费订单支付成功!")
        print(f"[OK] 支付结果: {payment_result}")
        print(f"\n[Test Passed]")


class TestNurseServiceOrder:
    """护士服务订单接口测试"""
    
    # Authorization token
    AUTH_TOKEN = "1323941.eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyTmFtZSI6Im84dkFydDZvX1JVSGh5d1dpYWtGTmxTejVtX1EiLCJleHAiOjE3NzI4NjkyMDgsInVzZXJJZCI6MTMyMzk0MSwidGVybWluYWxUeXBlIjoxMDAwM30.wKdZN1IUtA9s4YNchdOhTQdb9SCl5cKzQ6uNeo-8g5A"
    
    # Header with m-port=501
    HEADERS = {
        "Authorization": AUTH_TOKEN,
        "m-port": "501"
    }
    
    def test_create_nurse_service_order(self):
        """
        测试护士服务创建订单接口
        接口: /miniapp/service/usr/new/createOrder
        方法: POST
        """
        # 动态生成时间 - 未来5小时
        future_time = (datetime.now() + timedelta(hours=5)).strftime("%Y-%m-%d %H:%M:%S")
        
        # 加载请求参数并修改动态字段
        payload = load_request_data('create_nurse_service_order.json')
        payload['remark'] = "测试护士服务订单-" + future_time
        payload['serviceDates'][0]['homeTime'] = future_time
        
        # 发送请求
        response = http_client.post(
            endpoint="/ehutong-ehutcore-front-miniapp/miniapp/service/usr/new/createOrder",
            json=payload,
            headers=self.HEADERS
        )
        
        print(f"\n响应状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        # 断言响应状态码
        assert response.status_code == 200, f"期望状态码200，实际{response.status_code}"
        
        # 解析响应JSON
        result = response.json()
        
        # 验证返回code为0
        assert result.get("code") == 0, f"期望code为0，实际{result.get('code')}"
        
        # 验证返回msg
        assert result.get("msg") == "success", f"期望msg为success，实际{result.get('msg')}"
        
        # 验证orderUid存在且不为空
        order_uid = result.get("result", {}).get("orderUid")
        assert order_uid, "orderUid不能为空"
        
        print(f"\n[OK] 护士服务订单创建成功!")
        print(f"[OK] orderUid: {order_uid}")
        
        print(f"\n[Test Passed]")
        
        return order_uid
    
    def test_nurse_service_order_payment(self):
        """
        测试护士服务订单金币支付接口
        接口: /miniapp/order/pay
        方法: POST
        """
        # 先创建订单获取orderUid
        order_uid = self.test_create_nurse_service_order()
        print(f"\n[INFO] 护士服务订单orderUid: {order_uid}")
        
        # 加载支付请求参数
        payload = load_request_data('nurse_service_pay.json')
        payload['orderId'] = order_uid
        
        # 发送支付请求
        response = http_client.post(
            endpoint="/ehutong-ehutcore-front-miniapp/miniapp/order/pay",
            json=payload,
            headers=self.HEADERS
        )
        
        print(f"\n响应状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        # 断言响应状态码
        assert response.status_code == 200, f"期望状态码200，实际{response.status_code}"
        
        # 解析响应JSON
        result = response.json()
        
        # 验证返回code为0
        assert result.get("code") == 0, f"期望code为0，实际{result.get('code')}"
        
        # 验证返回msg
        assert result.get("msg") == "success", f"期望msg为success，实际{result.get('msg')}"
        
        # 验证支付结果
        payment_result = result.get("result")
        assert payment_result, "支付结果不能为空"
        
        print(f"\n[OK] 护士服务订单支付成功!")
        print(f"[OK] 支付结果: {payment_result}")
        print(f"\n[Test Passed]")


if __name__ == '__main__':
    pytest.main([__file__, '-v', '-s'])
