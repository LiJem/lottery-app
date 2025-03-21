from django.shortcuts import render
from django.http import HttpResponse, JsonResponse


from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *  # 根据实际模型导入


# 定义类型与模型类的映射
MODEL_MAPPING = {
    'kl8': LotteryKL8dHistory,
    '3d': Lottery3dHistory,
    'p5': LotteryP5History,
    'ssq': LotterySSQHistory,
    'super': LotterySuperHistory,
}

def get_lottery_data(lottery_type):
    """
    根据彩票类型获取对应的数据
    :param lottery_type: 彩票类型，如 'kl8', '3d', 'p5' 等
    :return: QuerySet 对象
    """
    model_class = MODEL_MAPPING.get(lottery_type)
    if model_class:
        return model_class.objects.all()
    else:
        raise ValueError(f"未知的彩票类型: {lottery_type}")
    
#获取最近N期数据
def get_latest_data(lottery_type, num_issues):
    """
    根据彩票类型获取最近N期的数据
    :param lottery_type: 彩票类型，如 'kl8', '3d', 'p5' 等"
    """
    model_class = MODEL_MAPPING.get(lottery_type)
    if model_class:
        return model_class.objects.order_by('-issue')[:num_issues]
    else:
        raise ValueError(f"未知的彩票类型: {lottery_type}")

#获取指定期数数据
def get_issues_data(lottery_type, issue):
    """
    根据彩票类型获取指定期数的数据
    :param lottery_type: 彩票类型，如 'kl8', '3d', 'p5' 等"""
    """"
    """
    model_class = MODEL_MAPPING.get(lottery_type)
    if model_class:
        return model_class.objects.filter(issue=issue)
    else:
        raise ValueError(f"未知的彩票类型: {lottery_type}")


# def lottery_view(request, lottery_type):
#     try:
#         data = get_lottery_data(lottery_type)
#         return JsonResponse(list(data.values()), safe=False)
#     except ValueError as e:
#         return JsonResponse({'error': str(e)}, status=400, safe=False)


@api_view(['GET'])
def lottery_data(request, lottery_type):
    try:
        num = int(request.query_params.get('limit', 100))  # 默认取100期
        data = get_latest_data(lottery_type, num)
        return Response({
            'status': 'success',
            'data': list(data.values())
        })
    except ValueError as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=400)
