# 接口测试框架

## 安装依赖

```bash
pip install requests pytest pytest-html
```

## 项目结构

```
api_test_framework/
├── config/
│   └── config.yaml          # 配置文件
├── utils/
│   ├── http_client.py       # HTTP客户端封装
│   └── logger.py            # 日志工具
├── tests/
│   ├── conftest.py          # pytest配置
│   └── test_store.py        # 接口测试用例
├── reports/                 # 测试报告目录
└── run_tests.py            # 运行脚本
```

## 运行测试

```bash
# 运行所有测试
python run_tests.py

# 指定测试用例
pytest tests/test_store.py -v

# 生成HTML报告
pytest tests/ -v --html=reports/report.html
```
