
from django.db import models
from FetchData.datamodels.model_manager import LotteryHistoryManager

class LotteryKL8dHistory(models.Model):
    index = models.IntegerField(null=True, blank=True)  # 添加索引字段
    issue = models.CharField(max_length=10, primary_key=True)  # 期号
    open_time = models.DateField()  # 开奖时间
    front_winning_num = models.CharField(max_length=100)  # 前区中奖号码
    back_winning_num = models.CharField(max_length=100)  # 后区中奖号码
    seq_front_winning_num = models.CharField(max_length=100)  # 前区顺序号码
    seq_back_winning_num = models.CharField(max_length=100)  # 后区顺序号码
    sale_money = models.CharField(max_length=100)  # 销售金额
    r9_sale_money = models.CharField(max_length=100)  # R9销售金额
    prize_pool_money = models.CharField(max_length=100)  # 奖池金额
    week = models.CharField(max_length=10)  # 星期几

    objects = LotteryHistoryManager()

    class Meta:
        db_table = 'lottery_kl8'

    def __str__(self):
        return self.issue