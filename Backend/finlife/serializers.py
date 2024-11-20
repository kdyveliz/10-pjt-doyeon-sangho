from rest_framework import serializers
from .models import (DepositOptions,
                      DepositProducts,
                      SavingsProducts,
                      SavingsOptions)


class DepositProductsSerializer(serializers.ModelSerializer):
  class Meta:
    model = DepositProducts
    fields = '__all__'

class DepositOptionsSerializer(serializers.ModelSerializer):
  class Meta:
    model = DepositOptions
    fields = '__all__'    



class SavingsProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingsProducts
        fields = '__all__'


class SavingsOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingsOptions
        fields = '__all__'