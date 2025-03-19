# Generated by Django 5.1.3 on 2025-03-19 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Lottery3dHistory',
            fields=[
                ('index', models.IntegerField(blank=True, null=True)),
                ('issue', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('open_time', models.DateField()),
                ('front_winning_num', models.CharField(max_length=100)),
                ('back_winning_num', models.CharField(max_length=100)),
                ('seq_front_winning_num', models.CharField(max_length=100)),
                ('seq_back_winning_num', models.CharField(max_length=100)),
                ('sale_money', models.CharField(max_length=100)),
                ('r9_sale_money', models.CharField(max_length=100)),
                ('prize_pool_money', models.CharField(max_length=100)),
                ('week', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'lottery_3d',
            },
        ),
        migrations.CreateModel(
            name='LotteryKL8dHistory',
            fields=[
                ('index', models.IntegerField(blank=True, null=True)),
                ('issue', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('open_time', models.DateField()),
                ('front_winning_num', models.CharField(max_length=100)),
                ('back_winning_num', models.CharField(max_length=100)),
                ('seq_front_winning_num', models.CharField(max_length=100)),
                ('seq_back_winning_num', models.CharField(max_length=100)),
                ('sale_money', models.CharField(max_length=100)),
                ('r9_sale_money', models.CharField(max_length=100)),
                ('prize_pool_money', models.CharField(max_length=100)),
                ('week', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'lottery_kl8',
            },
        ),
        migrations.CreateModel(
            name='LotterySSQHistory',
            fields=[
                ('index', models.IntegerField(blank=True, null=True)),
                ('issue', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('open_time', models.DateField()),
                ('front_winning_num', models.CharField(max_length=100)),
                ('back_winning_num', models.CharField(max_length=100)),
                ('seq_front_winning_num', models.CharField(max_length=100)),
                ('seq_back_winning_num', models.CharField(max_length=100)),
                ('sale_money', models.CharField(max_length=100)),
                ('r9_sale_money', models.CharField(max_length=100)),
                ('prize_pool_money', models.CharField(max_length=100)),
                ('week', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'lottery_ssq',
            },
        ),
        migrations.CreateModel(
            name='LotterySuperLottoHistory',
            fields=[
                ('index', models.IntegerField(blank=True, null=True)),
                ('issue', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('open_time', models.DateField()),
                ('front_winning_num', models.CharField(max_length=100)),
                ('back_winning_num', models.CharField(max_length=100)),
                ('seq_front_winning_num', models.CharField(max_length=100)),
                ('seq_back_winning_num', models.CharField(max_length=100)),
                ('sale_money', models.CharField(max_length=100)),
                ('r9_sale_money', models.CharField(max_length=100)),
                ('prize_pool_money', models.CharField(max_length=100)),
                ('week', models.CharField(max_length=10)),
            ],
            options={
                'db_table': 'lottery_super',
            },
        ),
    ]
