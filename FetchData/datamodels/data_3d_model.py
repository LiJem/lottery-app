
from django.db import models

class Lottery3dHistoryManager(models.Manager):
    def create_lottery_data(self, data, index=None):
        if index is None:
            # 获取当前最大的 index 值
            max_index = self.model.objects.aggregate(models.Max('index'))['index__max']
            index = (max_index or 0) + 1
        return self.create(
            index=index,
            issue=data['issue'],
            open_time=data['open_time'],
            front_winning_num=data['front_winning_num'],
            back_winning_num=data['back_winning_num'],
            seq_front_winning_num=data['seq_front_winning_num'],
            seq_back_winning_num=data['seq_back_winning_num'],
            sale_money=data['sale_money'],
            r9_sale_money=data['r9_sale_money'],
            prize_pool_money=data['prize_pool_money'],
            week=data['week'],
        )

    def update_lottery_data(self, issue, data, index=None):
        lottery = self.get(issue=issue)
        for key, value in data.items():
            setattr(lottery, key, value)
        if index is not None:
            lottery.index = index
        lottery.save()

    def delete_lottery_data(self, issue):
        self.filter(issue=issue).delete()

    def get_lottery_data(self, issue=None, reverse=False):
        if issue:
            return self.filter(issue=issue)
        else:
            queryset = self.all()
            if reverse:
                queryset = queryset.order_by('-issue')
            else:
                queryset = queryset.order_by('issue')
            return queryset

class Lottery3dHistory(models.Model):
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

    objects = Lottery3dHistoryManager()

    class Meta:
        db_table = 'lottery_3d'

    def __str__(self):
        return self.issue