"""
运行测试脚本
"""
import pytest
import os
import sys

# 项目根目录
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)


def main():
    """运行所有测试"""
    reports_dir = os.path.join(project_root, 'reports')
    os.makedirs(reports_dir, exist_ok=True)
    
    # pytest参数
    args = [
        'tests/',
        '-v',                    # 详细输出
        '-s',                    # 显示print输出
        '--html=reports/report.html',  # 生成HTML报告
        '--self-contained-html',       # HTML报告自包含样式
    ]
    
    print("=" * 50)
    print("开始运行接口测试...")
    print("=" * 50)
    
    exit_code = pytest.main(args)
    
    print("\n" + "=" * 50)
    if exit_code == 0:
        print("[SUCCESS] All tests passed!")
    else:
        print(f"[FAILED] Tests failed (exit code: {exit_code})")
    print("=" * 50)
    
    return exit_code


if __name__ == '__main__':
    sys.exit(main())
