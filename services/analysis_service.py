import re

class LotteryAnalysisService:
    @classmethod
    def get_hot_numbers(cls, lottery_type, limit):
        """获取热门号码（基于号码范围规范）"""
        all_counts = cls._get_all_number_counts(lottery_type, limit)
        valid_counts = {
            num: count for num, count in all_counts.items() 
            if cls._is_valid_number(lottery_type, num)
        }
        return sorted(valid_counts.items(), key=lambda x: -x[1])[:10]

    @classmethod
    def get_cold_numbers(cls, lottery_type, limit):
        """获取冷门号码（基于号码范围规范）"""
        all_counts = cls._get_all_number_counts(lottery_type, limit)
        valid_counts = {
            num: count for num, count in all_counts.items()
            if cls._is_valid_number(lottery_type, num)
        }
        return sorted(valid_counts.items(), key=lambda x: x[1])[:10]

    @classmethod
    def get_number_occurrences(cls, lottery_type, number, limit=100):
        """获取指定号码在N期内的出现次数"""
        if not cls._is_valid_number(lottery_type, number):
            raise ValueError(f"无效号码: {number} 该彩种不存在此号码")
        counts = cls._get_number_counts(lottery_type, number, limit)
        return counts

    @classmethod
    def _is_valid_number(cls, lottery_type, number):
        """修复号码验证逻辑"""
        number_ranges = {
            'kl8': {'length': 2, 'min': 1, 'max': 80},
            'ssq': {'length': 2, 'min': 1, 'max': 33},
            'super': {'length': 2, 'min': 1, 'max': 35},
            '3d': {'length': 3, 'pattern': r'^\d{3}$'},
            'p5': {'length': 5, 'pattern': r'^\d{5}$'}
        }
        
        rules = number_ranges.get(lottery_type)
        if not rules:
            return False
            
        if len(number) != rules['length']:
            return False
            
        if lottery_type in ['kl8', 'ssq', 'super']:
            try:
                num = int(number)
                return rules['min'] <= num <= rules['max']
            except ValueError:
                return False
        else:
            return re.match(rules['pattern'], number) is not None

    @classmethod
    def get_number_range(cls, lottery_type):
        """获取指定彩票类型的号码范围规范"""
        NUMBER_RANGES = {
            'kl8': {'type': 'number', 'min': 1, 'max': 80, 'length': 2},
            'ssq': {'type': 'number', 'min': 1, 'max': 33, 'length': 2},
            'super': {'type': 'number', 'min': 1, 'max': 35, 'length': 2},
            '3d': {'type': 'pattern', 'pattern': r'^\d{3}$', 'length': 3},
            'p5': {'type': 'pattern', 'pattern': r'^\d{5}$', 'length': 5}
        }
        
        spec = NUMBER_RANGES.get(lottery_type.lower())
        if not spec:
            raise ValueError(f"无效的彩票类型: {lottery_type}")
            
        return {
            'lottery_type': lottery_type,
            'number_spec': spec
        }

    @classmethod
    def _get_number_counts(cls, lottery_type, number, limit):
        """获取指定号码出现次数统计"""
        historical_draws = cls._fetch_historical_draws(lottery_type, limit)
        count = 0
        
        for draw in historical_draws:
            if number in draw:
                count += 1
        
        return count

    @classmethod
    def _get_all_number_counts(cls, lottery_type, limit):
        """获取所有号码出现次数统计"""
        number_spec = cls.get_number_range(lottery_type)['number_spec']
        counts = {}
        
        # 模拟从数据库或其他数据源获取的历史开奖数据
        historical_draws = cls._fetch_historical_draws(lottery_type, limit)
        
        for draw in historical_draws:
            for num in draw:
                if cls._is_valid_number(lottery_type, num):
                    if num in counts:
                        counts[num] += 1
                    else:
                        counts[num] = 1
        
        return counts

    @classmethod
    def _fetch_historical_draws(cls, lottery_type, limit):
        """从数据库获取真实历史开奖数据"""
        # 原导入语句替换为
        from FetchData.datamodels import MODEL_MAPPING
        
        # 获取对应彩票类型的模型类（保持4空格缩进）
        model = MODEL_MAPPING.get(lottery_type.lower())
        if not model:
            raise ValueError(f"不支持的彩票类型: {lottery_type}")
        
        # 获取最近N期开奖数据（按期号倒序）
        records = model.objects.all().order_by('-issue')[:limit]
        
        return [
            record.front_winning_num.split(',')
            for record in records
            if record.front_winning_num
        ]

        # """模拟获取历史开奖数据"""
        # import random
        # draws = []
        # number_spec = cls.get_number_range(lottery_type)['number_spec']
        
        # if number_spec['type'] == 'number':
        #     min_num = number_spec['min']
        #     max_num = number_spec['max']
        #     length = number_spec['length']
        # elif number_spec['type'] == 'pattern':
        #     length = number_spec['length']
        
        # for _ in range(limit):
        #     draw = set()
        #     while len(draw) < length:
        #         if number_spec['type'] == 'number':
        #             num = str(random.randint(min_num, max_num))
        #         elif number_spec['type'] == 'pattern':
        #             num = ''.join(str(random.randint(0, 9)) for _ in range(length))
        #         if cls._is_valid_number(lottery_type, num):
        #             draw.add(num)
        #     draws.append(list(draw))
        
        # return draws



