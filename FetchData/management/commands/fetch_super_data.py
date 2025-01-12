from decimal import Decimal, InvalidOperation
import requests
from datetime import datetime
from django.core.management.base import BaseCommand
from django.db import transaction

from FetchData.datamodels.data_super_model import LotterySuperLottoHistory

class SuperLottoDataFetcher:
    def __init__(self, game_no, province_id=0, page_size=30, is_verify=1):
        self.game_no = game_no
        self.province_id = province_id
        self.page_size = page_size
        self.is_verify = is_verify
        self.base_url = "https://webapi.sporttery.cn/gateway/lottery/getHistoryPageListV1.qry"

    def fetch_results(self, page_no=1):
        params = {
            "gameNo": self.game_no,
            "provinceId": self.province_id,
            "pageSize": self.page_size,
            "isVerify": self.is_verify,
            "pageNo": page_no
        }

        headers = {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "origin": "https://static.sporttery.cn",
            "referer": "https://static.sporttery.cn/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
        }

        try:
            response = requests.get(self.base_url, params=params, headers=headers)
            response.raise_for_status()  # 检查HTTP响应状态码
            json_data = response.json()
            if not json_data.get('success', False):
                print(f"API请求成功但返回失败: {json_data}")
                return None
            print(f"成功获取第 {page_no} 页数据")
            return json_data
        except requests.RequestException as e:
            print(f"请求失败：{e}")
            return None
        except ValueError as e:  # 包括JSON解码错误
            print(f"解析响应内容失败：{e}")
            return None

    def fetch_all_results(self):
        all_results = []
        page_no = 1

        while True:
            print(f"正在处理第 {page_no} 页...")
            page_results = self.fetch_results(page_no)

            if not page_results:
                print(f"未能获取第 {page_no} 页的数据")
                break

            value = page_results.get('value', {})
            data_list = value.get('list', [])

            if not data_list:
                print("当前页无数据，认为是最后一页")
                break

            all_results.extend(data_list)
            page_no += 1

        # 对所有结果按 lotteryDrawNum 或其他合适的字段进行倒序排序
        all_results.sort(key=lambda x: int(x['lotteryDrawNum']), reverse=False)
        return all_results

    @transaction.atomic  # 确保所有数据库操作在一个事务中完成
    def process_results(self, results):
        for result in results:
            try:
                draw_time_str = result['lotteryDrawTime']
                if len(draw_time_str) < 10:
                    print(f"无效的抽奖时间格式: {draw_time_str}")
                    continue

                draw_time = datetime.strptime(draw_time_str[:10], '%Y-%m-%d').date()

                # 解析 lottery_draw_result 字符串为前区和后区数据
                try:
                    result_parts = result['lotteryDrawResult'].split()
                    if len(result_parts) != 7:
                        raise ValueError("开奖结果应包含7个数字")
                    front_area = ' '.join(result_parts[:5])
                    back_area = ' '.join(result_parts[5:])
                except (ValueError, IndexError) as e:
                    print(f"解析开奖结果失败: {e}")
                    continue

                # 使用 update_or_create 来创建或更新记录
                lotto_history, created = LotterySuperLottoHistory.objects.update_or_create(
                    lottery_draw_num=result['lotteryDrawNum'],
                    defaults={
                        'front_area_result': front_area,
                        'back_area_result': back_area,
                        'draw_time': draw_time,
                    }
                )

                # 如果有 issueIndex，则设置它；否则计算一个新的 index
                # if 'issueIndex' in result and result['issueIndex'] is not None:
                #     lotto_history.index = result['issueIndex']
                # elif created:  # 只有在创建新记录时才计算新的 index
                #     max_index = LotterySuperLottoHistory.objects.aggregate(datamodels.Max('index'))['index__max']
                #     lotto_history.index = (max_index or 0) + 1

                lotto_history.save()

            except Exception as e:
                print(f"处理记录时出错: {e}")

class Command(BaseCommand):
    help = 'Fetch and store Super Lotto lottery data'

    def handle(self, *args, **options):
        super_lotto_fetcher = SuperLottoDataFetcher(game_no=85)
        all_super_lotto_results = super_lotto_fetcher.fetch_all_results()

        if all_super_lotto_results:
            super_lotto_fetcher.process_results(all_super_lotto_results)
            self.stdout.write(self.style.SUCCESS('超级大乐透数据已成功写入数据库'))
        else:
            self.stdout.write(self.style.ERROR('未能获取到超级大乐透数据'))