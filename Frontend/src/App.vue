<script setup>
import ExchangeCalculator from './components/ExchangeCalculator.vue'
</script>

<template>
  <div>
    <header>
      <nav>
        <router-link to="/">Home</router-link>
        <router-link to="/exchange-calculator">Exchange Calculator</router-link>
      </nav>
    </header>

    <main>
      <ExchangeCalculator />
    </main>
  </div>
</template>
