"""
pytest配置文件
"""
import pytest
import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)


@pytest.fixture(scope="session")
def base_url():
    """基础URL fixture"""
    return "https://api-test.ehutong.net"


def pytest_configure(config):
    """pytest配置"""
    config.addinivalue_line(
        "markers", "smoke: 冒烟测试"
    )
    config.addinivalue_line(
        "markers", "regression: 回归测试"
    )
