from django.shortcuts import render
from django.conf import settings
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import DepositProducts, DepositOptions,SavingsProducts, SavingsOptions
from rest_framework import status
from .serializers import DepositProductsSerializer, DepositOptionsSerializer,SavingsProductsSerializer, SavingsOptionsSerializer
from django.shortcuts import get_list_or_404


@api_view(['GET'])
def save_deposit_products(request):
  API_KEY = settings.API_KEY
  url = f'http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json?auth={API_KEY}&topFinGrpNo=020000&pageNo=1'
  response = requests.get(url).json()

  data_product = response['result']['baseList']
  data_options = response['result']['optionList']

  product_dict = {}
  for value in data_product:
    fin_prdt_cd = value["fin_prdt_cd"]
    kor_co_nm = value["kor_co_nm"]
    fin_prdt_nm = value["fin_prdt_nm"]
    etc_note = value["etc_note"]
    join_deny = value["join_deny"]
    join_member = value["join_member"]
    join_way = value["join_way"]
    spcl_cnd = value["spcl_cnd"]

    deposit_product, created = DepositProducts.objects.get_or_create(
    fin_prdt_cd=fin_prdt_cd,
    defaults={
        'kor_co_nm': kor_co_nm,
        'fin_prdt_nm': fin_prdt_nm,
        'etc_note': etc_note,
        'join_deny': join_deny,
        'join_member': join_member,
        'join_way': join_way,
        'spcl_cnd': spcl_cnd,
      }
    )
        
    product_dict[fin_prdt_cd] = deposit_product

  for option_data in data_options:
    fin_prdt_cd = option_data['fin_prdt_cd']
    intr_rate_type_nm = option_data['intr_rate_type_nm']
    intr_rate = option_data['intr_rate']
    intr_rate2 = option_data['intr_rate2']
    if not intr_rate:
      intr_rate = -1
    if not intr_rate2:
      intr_rate2 = -1  
    save_trm = option_data['save_trm']
    
    if fin_prdt_cd in product_dict:
      deposit_option, created = DepositOptions.objects.get_or_create(
        product = product_dict[fin_prdt_cd],
        fin_prdt_cd = fin_prdt_cd,
        intr_rate_type_nm = intr_rate_type_nm,
        intr_rate = intr_rate,
        intr_rate2 = intr_rate2,
        save_trm = save_trm,
        defaults={
          'product' : product_dict[fin_prdt_cd],
          'fin_prdt_cd' : fin_prdt_cd,
          'intr_rate_type_nm' : intr_rate_type_nm,
          'intr_rate' : intr_rate,
          'intr_rate2' : intr_rate2,
          'save_trm' : save_trm,
        }
      )

  return Response({"message" : "Data saved successfully"})

@api_view(['GET', 'POST'])
def deposit_products(request):
  if request.method == 'GET':
    products = DepositProducts.objects.all()
    serializer = DepositProductsSerializer(products, many = True)
    return Response(serializer.data, status=status.HTTP_200_OK)
  elif request.method == 'POST':
    serializer = DepositProductsSerializer(data = request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_200_OK)
    else:
      return Response({"message" : "이미 있는 데이터이거나, 데이터가 잘못 입력되었습니다."})

@api_view(['GET'])
def deposit_product_options(request, fin_prdt_cd):
  if request.method == "GET":
    options = get_list_or_404(DepositOptions, fin_prdt_cd = fin_prdt_cd)
    serializer = DepositOptionsSerializer(options, many = True)
    return Response(serializer.data, status=status.HTTP_200_OK)
@api_view(['GET'])
def top_rate(request):
   # 최고 금리를 가진 옵션을 찾기
    top_option = DepositOptions.objects.order_by('-intr_rate2').first()
    
    # 최고 금리를 가진 옵션이 없다면 에러 메시지 반환
    if not top_option:
        return Response({"error": "No deposit options available."}, status=status.HTTP_404_NOT_FOUND)
    
    # 최고 금리를 가진 옵션에 해당하는 상품 정보 조회
    product = top_option.product
    product_serializer = DepositProductsSerializer(product)
    
    # 해당 상품의 모든 옵션 조회
    options = DepositOptions.objects.filter(product=product)
    options_serializer = DepositOptionsSerializer(options, many=True)
    
    # 상품 정보와 옵션 정보 함께 반환
    return Response({
        "product": product_serializer.data,
        "options": options_serializer.data
    }, status=status.HTTP_200_OK)


# 예금 데이터
@api_view(['GET'])
def save_savings_products(request):
    """
    적금 상품 데이터를 외부 API로부터 가져와 저장
    """
    API_KEY = settings.API_KEY
    url = f'http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json?auth={API_KEY}&topFinGrpNo=020000&pageNo=1'
    response = requests.get(url).json()

    data_product = response['result']['baseList']
    data_options = response['result']['optionList']

    product_dict = {}
    for value in data_product:
        fin_prdt_cd = value["fin_prdt_cd"]
        kor_co_nm = value["kor_co_nm"]
        fin_prdt_nm = value["fin_prdt_nm"]
        etc_note = value["etc_note"]
        join_deny = value["join_deny"]
        join_member = value["join_member"]
        join_way = value["join_way"]
        spcl_cnd = value["spcl_cnd"]

        savings_product, created = SavingsProducts.objects.get_or_create(
            fin_prdt_cd=fin_prdt_cd,
            defaults={
                'kor_co_nm': kor_co_nm,
                'fin_prdt_nm': fin_prdt_nm,
                'etc_note': etc_note,
                'join_deny': join_deny,
                'join_member': join_member,
                'join_way': join_way,
                'spcl_cnd': spcl_cnd,
            }
        )

        product_dict[fin_prdt_cd] = savings_product

    for option_data in data_options:
        fin_prdt_cd = option_data['fin_prdt_cd']
        intr_rate_type_nm = option_data['intr_rate_type_nm']
        intr_rate = option_data['intr_rate'] or -1
        intr_rate2 = option_data['intr_rate2'] or -1
        save_trm = option_data['save_trm']

        if fin_prdt_cd in product_dict:
            savings_option, created = SavingsOptions.objects.get_or_create(
                product=product_dict[fin_prdt_cd],
                fin_prdt_cd=fin_prdt_cd,
                intr_rate_type_nm=intr_rate_type_nm,
                intr_rate=intr_rate,
                intr_rate2=intr_rate2,
                save_trm=save_trm,
                defaults={
                    'product': product_dict[fin_prdt_cd],
                    'fin_prdt_cd': fin_prdt_cd,
                    'intr_rate_type_nm': intr_rate_type_nm,
                    'intr_rate': intr_rate,
                    'intr_rate2': intr_rate2,
                    'save_trm': save_trm,
                }
            )

    return Response({"message": "Data saved successfully"}, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST'])
def savings_products(request):
    """
    적금 상품 데이터를 조회 및 추가
    """
    if request.method == 'GET':
        products = SavingsProducts.objects.all()
        serializer = SavingsProductsSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = SavingsProductsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "데이터가 잘못 입력되었습니다."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def savings_product_options(request, fin_prdt_cd):
    """
    특정 적금 상품의 옵션 데이터를 조회
    """
    if request.method == "GET":
        options = get_list_or_404(SavingsOptions, fin_prdt_cd=fin_prdt_cd)
        serializer = SavingsOptionsSerializer(options, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def top_rate_savings_products(request):
    """
    최고 금리를 가진 적금 상품과 옵션 반환
    """
    top_option = SavingsOptions.objects.order_by('-intr_rate2').first()

    if not top_option:
        return Response({"error": "No savings options available."}, status=status.HTTP_404_NOT_FOUND)

    product = top_option.product
    product_serializer = SavingsProductsSerializer(product)

    options = SavingsOptions.objects.filter(product=product)
    options_serializer = SavingsOptionsSerializer(options, many=True)

    return Response({
        "product": product_serializer.data,
        "options": options_serializer.data
    }, status=status.HTTP_200_OK)



# 환율 데이터
@api_view(['GET'])
def fetch_exchange_rates(request):
    """
    Fetch real-time exchange rates from an external API.
    """
    API_URL = "https://openexchangerates.org/api/latest.json"
    API_KEY = settings.EXCHANGE_API_KEY  # 환경변수에서 API 키 가져오기

    try:
        response = requests.get(API_URL, params={"app_id": API_KEY})
        response.raise_for_status()  # HTTP 에러 발생 시 예외 처리
        data = response.json()
        return Response(data, status=status.HTTP_200_OK)
    except requests.exceptions.RequestException as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def calculate_exchange(request):
    """
    Calculate the exchanged amount based on the provided rates and amount.
    """
    try:
        base_currency = request.data.get("base_currency")  # 예: "USD"
        target_currency = request.data.get("target_currency")  # 예: "KRW"
        amount = float(request.data.get("amount", 0))  # 변환하려는 금액
        rates = request.data.get("rates")  # 환율 데이터 (외부 API에서 가져옴)

        # 계산
        if base_currency == "USD":
            rate = rates.get(target_currency)
        else:
            rate = rates.get(target_currency) / rates.get(base_currency)

        if not rate:
            return Response({"error": "Invalid currency code"}, status=status.HTTP_400_BAD_REQUEST)

        converted_amount = amount * rate
        return Response({"converted_amount": round(converted_amount, 2)}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)