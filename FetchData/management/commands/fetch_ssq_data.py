
from datetime import datetime
from django.core.management.base import BaseCommand
from FetchData.management.commands.common import LotteryDataFetcher
from FetchData.datamodels.data_ssq_model import LotterySSQHistory

class SSQDataFetcher(LotteryDataFetcher):
    def __init__(self):
        super().__init__(lottery_id=1)

    def fetch_all_results(self):
        start_date = "2000-01-01"
        end_date = datetime.now().strftime("%Y-%m-%d")
        all_results = self.fetch_results_by_date(start_date, end_date)

        if all_results:
            filtered_results = self.filter_results(all_results)
            return filtered_results
        else:
            print("未能获取到双色球数据")
            return []

class Command(BaseCommand):
    help = 'Fetch and store 双色球 lottery data'

    def handle(self, *args, **options):
        fetcher = SSQDataFetcher()
        results = fetcher.fetch_all_results()

        if results:
            # 对结果按期号进行排序
            sorted_results  = sorted(results, key=lambda x: int(x['issue']))

            for index, result in enumerate(sorted_results , start=1):

                # print(result)

                open_time = datetime.strptime(result['openTime'], '%Y-%m-%d')
                # open_time = pytz.timezone('UTC').localize(open_time)  # 添加时区信息

                LotterySSQHistory.objects.update_or_create(
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
            self.stdout.write(self.style.SUCCESS('双色球数据已成功写入数据库'))
        else:
            self.stdout.write(self.style.ERROR('未能获取到双色球数据'))