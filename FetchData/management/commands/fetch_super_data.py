from datetime import datetime
from django.core.management.base import BaseCommand
from FetchData.management.commands.common import LotteryDataFetcher
from FetchData.datamodels.data_super_model import LotterySuperLottoHistory

class SuperLottoDataFetcher(LotteryDataFetcher):
    def __init__(self):
        super().__init__(lottery_id=281)

    def fetch_all_results(self):
        start_date = "2008-01-01"
        end_date = datetime.now().strftime("%Y-%m-%d")
        all_results = self.fetch_results_by_date(start_date, end_date)

        if all_results:
            filtered_results = self.filter_results(all_results)
            return filtered_results
        else:
            print("未能获取到超级大乐透数据")
            return []

class Command(BaseCommand):
    help = 'Fetch and store 大乐透 lottery data'

    def handle(self, *args, **options):
        fetcher = SuperLottoDataFetcher()
        results = fetcher.fetch_all_results()

        if results:
            # 对结果按期号进行排序
            sorted_results  = sorted(results, key=lambda x: int(x['issue']))

            # 批量插入数据
            for index, result in enumerate(sorted_results , start=1):
                open_time = datetime.strptime(result['openTime'], '%Y-%m-%d')
                LotterySuperLottoHistory.objects.update_or_create(
                    issue=result['issue'], 
                    defaults={
                        'index': index,  # 添加索引字段
                        'open_time': open_time,
                        'front_winning_num': result['frontWinningNum'],
                        'back_winning_num': result['backWinningNum'],
                        'seq_front_winning_num': result['seqFrontWinningNum'],
                        'seq_back_winning_num': result['seqBackWinningNum'],
                        'sale_money': result['saleMoney'],
                        'r9_sale_money': result['r9SaleMoney'],
                        'prize_pool_money': result['prizePoolMoney'],
                        'week': result['week']
                    }
                )

            self.stdout.write(self.style.SUCCESS('超级大乐透数据已成功写入数据库'))
        else:
            self.stdout.write(self.style.ERROR('未能获取到超级大乐透数据'))



