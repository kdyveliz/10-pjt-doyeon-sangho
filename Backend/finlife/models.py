from django.db import models

# Create your models here.
class DepositProducts(models.Model):
  fin_prdt_cd = models.TextField(unique=True)
  kor_co_nm = models.TextField()
  fin_prdt_nm = models.TextField()
  etc_note = models.TextField()
  JOIN_DENY_CHOICES = [
        (1, '제한없음'),
        (2, '서민전용'),
        (3, '일부제한'),
    ]

  join_deny = models.IntegerField(choices=JOIN_DENY_CHOICES, default=1)
  join_member = models.TextField()
  join_way = models.TextField()
  spcl_cnd = models.TextField()


class DepositOptions(models.Model):
  product = models.ForeignKey(DepositProducts, on_delete=models.CASCADE)
  fin_prdt_cd = models.TextField()
  intr_rate_type_nm = models.CharField(max_length=100)
  intr_rate = models.FloatField()
  intr_rate2 = models.FloatField()
  save_trm = models.IntegerField()


class SavingsProducts(models.Model):
    fin_prdt_cd = models.TextField(unique=True)  # 금융 상품 코드
    kor_co_nm = models.TextField()  # 금융회사명
    fin_prdt_nm = models.TextField()  # 금융 상품명
    join_way = models.TextField()  # 가입 방법
    mtrt_int = models.TextField()  # 만기 후 이자율
    spcl_cnd = models.TextField()  # 우대 조건
    join_deny = models.IntegerField(
        choices=[
            (1, '제한없음'),
            (2, '서민전용'),
            (3, '일부제한'),
        ],
        default=1,
    )  # 가입 제한
    join_member = models.TextField()  # 가입 대상
    etc_note = models.TextField()  # 기타 유의사항
    max_limit = models.BigIntegerField(null=True, blank=True)  # 최고 한도
    dcls_strt_day = models.DateField(null=True, blank=True)  # 공시 시작일
    dcls_end_day = models.DateField(null=True, blank=True)  # 공시 종료일
    fin_co_subm_day = models.DateField(null=True, blank=True)  # 등록일


class SavingsOptions(models.Model):
    product = models.ForeignKey(SavingsProducts, on_delete=models.CASCADE)  # 적금 상품과 연결
    fin_prdt_cd = models.TextField()  # 금융 상품 코드
    intr_rate_type_nm = models.CharField(max_length=100)  # 금리 유형 명칭
    intr_rate = models.FloatField()  # 기본 이율
    intr_rate2 = models.FloatField(null=True, blank=True)  # 우대 이율
    save_trm = models.IntegerField()  # 저축 기간 (단위: 월)   