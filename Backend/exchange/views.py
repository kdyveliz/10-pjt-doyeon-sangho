import requests
from django.http import JsonResponse
from django.conf import settings

def get_exchange_rate(request):
    """
    한국수출입은행 API를 통해 환율 데이터를 가져옵니다.
    """
    base_currency = request.GET.get('base', 'KRW')  # 기준 통화 (기본값: KRW)
    target_currency = request.GET.get('target', 'USD')  # 대상 통화 (기본값: USD)
    amount = float(request.GET.get('amount', 1))  # 입력 금액 (기본값: 1)

    # 한국수출입은행 API 호출 URL
    url = f"https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={settings.EXPORT_IMPORT_BANK_API_KEY}&searchdate=20241120&data=AP01"

    try:
        # API 호출
        response = requests.get(url)
        response.raise_for_status()
        exchange_data = response.json()

        # 환율 찾기
        rate = next((item for item in exchange_data if item['cur_unit'] == target_currency), None)
        if not rate:
            return JsonResponse({'error': f'Currency {target_currency} not found.'}, status=400)

        exchange_rate = float(rate['deal_bas_r'].replace(',', ''))

        # 계산
        if base_currency == 'KRW':
            converted_value = amount / exchange_rate  # 원화를 타국 통화로 변환
        else:
            converted_value = amount * exchange_rate  # 타국 통화를 원화로 변환

        return JsonResponse({
            'result': 'success',
            'base_currency': base_currency,
            'target_currency': target_currency,
            'exchange_rate': exchange_rate,
            'converted_value': converted_value,
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
