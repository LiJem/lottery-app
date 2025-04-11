import requests
import json
from datetime import datetime

# 基础URL
BASE_URL = 'http://localhost:8000'

def test_api(endpoint, method='GET', params=None, data=None):
    """通用API测试函数"""
    url = f"{BASE_URL}{endpoint}"
    print(f"\n测试接口: {url}")
    print(f"方法: {method}")
    
    try:
        if method == 'GET':
            response = requests.get(url, params=params)
        else:
            response = requests.post(url, params=params, json=data)
        
        print(f"状态码: {response.status_code}")
        print("响应数据:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        return response.status_code == 200
    except Exception as e:
        print(f"测试失败: {str(e)}")
        return False

def test_all_apis():
    """测试所有API接口"""
    # 1. 测试分析接口
    print("\n=== 测试分析接口 ===")
    test_api('/analysis/latest/')
    test_api('/analysis/trend/')
    test_api('/analysis/hot-numbers/')
    test_api('/analysis/cold-numbers/')
    test_api('/analysis/statistics/')

    # 2. 测试彩票数据接口
    print("\n=== 测试彩票数据接口 ===")
    test_api('/api/ssq/', params={'limit': 5})
    test_api('/api/kl8/', params={'limit': 5})
    test_api('/api/3d/', params={'limit': 5})
    test_api('/api/p5/', params={'limit': 5})
    test_api('/api/super/', params={'limit': 5})

if __name__ == '__main__':
    print("开始API测试...")
    test_all_apis()
    print("\n测试完成！") 