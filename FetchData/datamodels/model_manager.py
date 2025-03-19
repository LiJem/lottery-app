
from django.db import models

class LotteryHistoryManager(models.Manager):
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