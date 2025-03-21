from rest_framework.decorators import api_view
from rest_framework.response import Response
from services.analysis_service import LotteryAnalysisService

@api_view(['GET'])
def hot_cold_numbers(request, lottery_type, limit):
    try:
        # 获取分析结果
        hot_nums = LotteryAnalysisService.get_hot_numbers(lottery_type, limit)
        cold_nums = LotteryAnalysisService.get_cold_numbers(lottery_type, limit)
        
        return Response({
            "status": "success",
            "data": {
                "hot": hot_nums,
                "cold": cold_nums
            }
        })
    except Exception as e:
        return Response({"status": "error", "message": str(e)}, status=400)


@api_view(['GET'])
def number_occurrences(request, lottery_type):
    try:
        number = request.query_params.get('number')
        limit = int(request.query_params.get('limit', 100))
        
        if not number:
            raise ValueError("必须提供number参数")
            
        count = LotteryAnalysisService.get_number_occurrences(
            lottery_type, 
            number.strip(), 
            limit
        )
        
        return Response({
            "status": "success",
            "data": {
                "number": number,
                "occurrences": count,
                "total_issues": limit
            }
        })
        
    except Exception as e:
        return Response({"status": "error", "message": str(e)}, status=400)