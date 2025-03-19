import json
import requests
import time

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
            "callback": f"jQuery112205721622909327504_{timestamp}",
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
            "accept-language": "zh-CN,zh;q=0.9,en-GB;q=0.8,en-US;q=0.7,en;q=0.6",
            "connection": "keep-alive",
            "cookie": "PHPSESSID=d5idt7fujltrd0j99neca17ek2; Hm_lvt_12e4883fd1649d006e3ae22a39f97330=1733110337; HMACCOUNT=AC9E31EBF54BD0C5; _ga=GA1.1.817644494.1733110667; Hm_lvt_692bd5f9c07d3ebd0063062fb0d7622f=1733110667; _ga_9FDP3NWFMS=GS1.1.1733110666.1.1.1733110675.0.0.0; Hm_lpvt_12e4883fd1649d006e3ae22a39f97330=1733110675; Hm_lpvt_692bd5f9c07d3ebd0063062fb0d7622f=1733110675",  # 替换为实际的 cookie
            "host": "jc.zhcw.com",
            "referer": "https://www.zhcw.com/",
            "sec-ch-ua": '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
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
