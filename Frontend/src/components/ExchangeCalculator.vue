<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

// 상태 변수
const amount = ref(0);
const baseCurrency = ref('KRW');
const targetCurrency = ref('USD');
const convertedValue = ref(0);
const currencies = ref(['KRW', 'USD', 'EUR', 'JPY', 'CNY']); // 주요 통화 리스트

// API URL
const API_URL = 'http://127.0.0.1:8000/api/exchange-rate/';

// 환율 계산 요청
const calculateExchange = async () => {
  try {
    const response = await axios.get(API_URL, {
      params: {
        base: baseCurrency.value,
        target: targetCurrency.value,
        amount: amount.value,
      },
    });
    convertedValue.value = response.data.converted_value;
  } catch (error) {
    console.error('Failed to calculate exchange:', error);
  }
};
</script>

<template>
  <div>
    <h1>환율 계산기</h1>
    <form @submit.prevent="calculateExchange">
      <label>
        금액:
        <input v-model.number="amount" type="number" placeholder="금액을 입력하세요" />
      </label>
      <label>
        기준 통화:
        <select v-model="baseCurrency">
          <option v-for="currency in currencies" :key="currency" :value="currency">
            {{ currency }}
          </option>
        </select>
      </label>
      <label>
        대상 통화:
        <select v-model="targetCurrency">
          <option v-for="currency in currencies" :key="currency" :value="currency">
            {{ currency }}
          </option>
        </select>
      </label>
      <button type="submit">계산</button>
    </form>
    <p>결과: {{ amount }} {{ baseCurrency }} = {{ convertedValue.toFixed(2) }} {{ targetCurrency }}</p>
  </div>
</template>

<style scoped>
form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
</style>
