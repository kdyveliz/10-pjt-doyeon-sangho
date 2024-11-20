<script setup>
import { ref, onMounted, watch } from 'vue'

// 상태 변수
const amount = ref(0)
const baseCurrency = ref('KRW') // 기본 기준 통화
const targetCurrency = ref('USD') // 기본 대상 통화
const currencies = ref([]) // 통화 목록
const result = ref(0) // 계산 결과

// API URL
const API_URL = 'http://127.0.0.1:8000/exchange/'

// 환율 데이터 가져오기
const fetchCurrencies = async () => {
  try {
    const response = await fetch(API_URL)
    const data = await response.json()
    if (data.result === 'success') {
      currencies.value = Object.keys(data.exchange_rates).filter(
        (currency) => data.exchange_rates[currency] > 0
      )
    } else {
      console.error('Failed to fetch exchange rates:', data.message)
    }
  } catch (error) {
    console.error('Failed to fetch exchange rates:', error)
  }
}

// 환율 계산
const calculateExchange = async () => {
  try {
    const response = await fetch(API_URL)
    const data = await response.json()
    const rate = data.exchange_rates[targetCurrency.value]
    if (rate) {
      result.value = amount.value * rate
    } else {
      result.value = 0
      console.error('Invalid target currency rate')
    }
  } catch (error) {
    console.error('Failed to calculate exchange:', error)
  }
}

// 기준 통화가 변경될 때 환율 데이터를 새로 가져옵니다.
watch(baseCurrency, fetchCurrencies)

// 컴포넌트가 로드될 때 환율 데이터를 가져옵니다.
onMounted(fetchCurrencies)
</script>

<template>
  <div>
    <h1>환율 계산기</h1>
    <form @submit.prevent="calculateExchange">
      <label>
        금액:
        <input v-model.number="amount" type="number" placeholder="Enter amount" />
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
    <p v-if="result > 0">
      결과: {{ amount }} {{ baseCurrency }} = {{ result.toFixed(2) }} {{ targetCurrency }}
    </p>
  </div>
</template>

<style scoped>
form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
</style>
