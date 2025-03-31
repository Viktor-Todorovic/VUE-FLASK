<script setup>
import { RouterLink, RouterView } from 'vue-router'
import Navigacija from './components/Navigacija.vue';
</script>

<template>
  <Navigacija />
  <RouterView />
</template>

<style>
html,body{
  /* background: rgb(111,33,33) !important;
  background: linear-gradient(0deg, rgba(111,33,33,1) 15%, rgba(255,171,0,1) 73%) !important;
  background-repeat: no-repeat;
  height: 100% !important; */
  background-color:#e4daf7 !important;
  overflow-x: hidden;
}
</style>
