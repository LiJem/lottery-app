import json
import requests
import time
from datetime import datetime
from django.core.management.base import BaseCommand
from FetchData.datamodels.data_3d_model import Lottery3dHistory


class LotteryDataFetcher:
    def __init__(self, lottery_id):
        self.recent_issues = 1000
        self.page_size = 30
        self.lottery_id = lottery_id

    def fetch_results_by_date_range(self, start_date, end_date, page_num=1, page_size=None):
        if page_size is None:
            page_size = self.page_size

        url = "https://jc.zhcw.com/port/client_json.php"
        timestamp = int(time.time() * 1000)

        params = {
            "callback": f"jQuery112206347322274095686_{timestamp}",
            "transactionType": "10001001",
            "lotteryId": self.lottery_id,
            "issueCount": "0",
            "startIssue": "0",
            "endIssue": "0",
            "startDate": start_date,
            "endDate": end_date,
            "type": "2",
            "pageNum": page_num,
            "pageSize": page_size,
            "tt": "0.28746476864436565",
            "_": timestamp
        }

        headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "zh-CN,zh;q=0.9",
            "connection": "keep-alive",
            "cookie": "your_cookie_here",  # 替换为实际的 cookie
            "host": "jc.zhcw.com",
            "referer": "https://www.zhcw.com/",
            "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "Windows",
            "sec-fetch-dest": "script",
            "sec-fetch-mode": "no-cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
        }

        response = requests.get(url, params=params, headers=headers)

        if response.status_code != 200:
            print(f"请求失败，状态码: {response.status_code}")
            return None

        jsonp_response = response.text
        json_data = json.loads(jsonp_response.split('(', 1)[1].rsplit(')', 1)[0])
        return json_data

    def fetch_results_by_date(self, start_date, end_date):
        all_results = []
        page_num = 1
        total_pages = None  # 总页数

        while True:
            print(f"正在处理第 {page_num} 页...")
            page_results = self.fetch_results_by_date_range(start_date, end_date, page_num=page_num)

            if not page_results or 'data' not in page_results:
                print(f"未能获取第 {page_num} 页的数据")
                break

            all_results.extend(page_results['data'])
            print(f"成功获取第 {page_num} 页的数据")

            # 检查是否为最后一页
            if total_pages is None and 'pages' in page_results:
                total_pages = int(page_results['pages'])

            if total_pages is not None and page_num >= total_pages:
                print("已到达最后一页")
                break

            if len(page_results['data']) < self.page_size:
                print("当前页数据量少于页面大小，认为是最后一页")
                break

            page_num += 1

        return all_results

    def filter_results(self, results):
        filtered_results = []
        for result in results:
            filtered_result = {key: value for key, value in result.items() if key != 'winnerDetails'}
            filtered_results.append(filtered_result)
        return filtered_results

class ThreeDDataFetcher(LotteryDataFetcher):
    def __init__(self):
        super().__init__(lottery_id=2)

    def fetch_all_results(self):
        start_date = "2000-01-01"
        end_date = datetime.now().strftime("%Y-%m-%d")
        all_results = self.fetch_results_by_date(start_date, end_date)

        if all_results:
            filtered_results = self.filter_results(all_results)
            return filtered_results
        else:
            print("未能获取到3D数据")
            return []

class Command(BaseCommand):
    help = 'Fetch and store 3D lottery data'

    def handle(self, *args, **options):
        three_d_fetcher = ThreeDDataFetcher()
        three_d_results = three_d_fetcher.fetch_all_results()

        if three_d_results:
            # 对结果按期号进行排序
            results_3d_sorted = sorted(three_d_results, key=lambda x: int(x['issue']))

            for index, result in enumerate(results_3d_sorted, start=1):

                # print(result)

                open_time = datetime.strptime(result['openTime'], '%Y-%m-%d')
                # open_time = pytz.timezone('UTC').localize(open_time)  # 添加时区信息

                Lottery3dHistory.objects.update_or_create(
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
            self.stdout.write(self.style.SUCCESS('3D数据已成功写入数据库'))
        else:
            self.stdout.write(self.style.ERROR('未能获取到3D数据'))