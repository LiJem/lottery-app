from django.db import models
from datetime import datetime, timezone
from sqlite3 import IntegrityError

from django.db import transaction, IntegrityError

class SuperLottoHistoryManager(models.Manager):
    @transaction.atomic  # 确保所有数据库操作在一个事务中完成
    def create_lottery_data(self, data, index=None):
        draw_time_str = data.get('lotteryDrawTime', '')
        if len(draw_time_str) < 10:
            print(f"无效的抽奖时间格式: {draw_time_str}")
            return None

        draw_time = timezone.datetime.strptime(draw_time_str[:10], '%Y-%m-%d').date()

        try:
            result_parts = data['lotteryDrawResult'].split()
            if len(result_parts) != 7:
                raise ValueError("开奖结果应包含7个数字")
            front_area = ' '.join(result_parts[:5])
            back_area = ' '.join(result_parts[5:])
        except (ValueError, IndexError) as e:
            print(f"解析开奖结果失败: {e}")
            return None

        if index is None:
            # 使用 select_for_update() 来避免并发问题
            max_index = self.model.objects.select_for_update().aggregate(models.Max('index'))['index__max']
            index = (max_index or 0) + 1
            print(f"自动计算的 index 值为: {index}")

        try:
            # 使用 update_or_create 来创建或更新记录，确保数据一致性
            lotto_history, created = self.model.objects.update_or_create(
                lottery_draw_num=data['lotteryDrawNum'],
                defaults={
                    'draw_time': draw_time,
                    'front_area_result': front_area,
                    'back_area_result': back_area,
                    'index': index,
                }
            )
            print(f"创建/更新记录，期号: {data['lotteryDrawNum']}，index: {index}")
            return lotto_history
        except IntegrityError as e:
            # 如果发生完整性错误（如重复键），则回滚事务
            transaction.set_rollback(True)
            print(f"创建记录时发生完整性错误：{data['lotteryDrawNum']}，错误信息: {e}")
            return None

    def get_lottery_data(self, lottery_draw_num=None, reverse=True):
        """
        获取彩票数据，默认按 index 或 lottery_draw_num 降序排列。
        """
        if lottery_draw_num:
            return self.filter(lottery_draw_num=lottery_draw_num).order_by('-index')
        else:
            queryset = self.all()
            if reverse:
                queryset = queryset.order_by('-index')  # 按 index 降序
            else:
                queryset = queryset.order_by('index')   # 按 index 升序
            return queryset
class LotterySuperLottoHistory(models.Model):
    index = models.IntegerField(null=True, blank=True, verbose_name="索引")  # 允许为空
    lottery_draw_num = models.CharField(max_length=10, primary_key=True, verbose_name="期号")
    draw_time = models.DateField(verbose_name="开奖日期")
    front_area_result = models.CharField(max_length=20, verbose_name="前区开奖结果")  # 前区结果
    back_area_result = models.CharField(max_length=10, verbose_name="后区开奖结果")  # 后区结果

    objects = SuperLottoHistoryManager()

    def save(self, *args, **kwargs):
        if self.index is None:
            # 在保存之前确保 index 被设置
            with transaction.atomic():
                max_index = self.__class__.objects.aggregate(models.Max('index'))['index__max']
                self.index = (max_index or 0) + 1
                # print(f"在 save 方法中自动计算的 index 值为: {self.index}")
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'lottery_super'
        verbose_name = "超级大乐透历史记录"
        verbose_name_plural = verbose_name
        unique_together = ['index', 'lottery_draw_num']  # 确保 index 和 lottery_draw_num 组合唯一

    def __str__(self):
        return f"{self.lottery_draw_num} - {self.draw_time} - 前区: {self.front_area_result}, 后区: {self.back_area_result}"