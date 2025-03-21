# 修改路径配置
import os
import sys
import django

# 添加项目根目录和LotteryApp到Python路径
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.extend([
    base_dir,  # 项目根目录
    os.path.join(base_dir, 'LotteryApp')  # 添加LotteryApp目录
])

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LotteryApp.settings')
django.setup()

import unittest
from services.analysis_service import LotteryAnalysisService

class TestLotteryAnalysis(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """测试数据初始化"""
        # 可在此添加测试用数据库初始化代码
        pass

    def test_hot_numbers(self):
        """测试热门号码统计"""
        # 测试不同彩票类型
        for ltype in ['ssq', 'kl8', '3d']:
            with self.subTest(lottery_type=ltype):
                result = LotteryAnalysisService.get_hot_numbers(ltype, 100)
                self.assertEqual(len(result), 10)
                # 验证号码有效性
                for num, _ in result:
                    self.assertTrue(LotteryAnalysisService._is_valid_number(ltype, num))

    def test_cold_numbers(self):
        """测试冷门号码统计"""
        result = LotteryAnalysisService.get_cold_numbers('ssq', 100)
        self.assertEqual(len(result), 10)
        # 验证冷门号码顺序
        counts = [x[1] for x in result]
        self.assertEqual(counts, sorted(counts))

    def test_number_occurrences(self):
        """测试单号码出现次数"""
        # 测试有效号码
        count = LotteryAnalysisService.get_number_occurrences('ssq', '01', 100)
        self.assertIsInstance(count, int)
        
        # 测试无效号码
        with self.assertRaises(ValueError):
            LotteryAnalysisService.get_number_occurrences('ssq', '100', 100)

    def test_number_validation(self):
        """测试号码验证逻辑"""
        # 测试双色球
        self.assertTrue(LotteryAnalysisService._is_valid_number('ssq', '33'))
        self.assertFalse(LotteryAnalysisService._is_valid_number('ssq', '34'))
        
        # 测试3D
        self.assertTrue(LotteryAnalysisService._is_valid_number('3d', '123'))
        self.assertFalse(LotteryAnalysisService._is_valid_number('3d', '12'))

if __name__ == '__main__':
    unittest.main()
