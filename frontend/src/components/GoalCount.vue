<template>
  <div class="flex flex-col">
    <button class="text-2xl text-lightWhite font-bold  fa-sharp fa-solid fa-chevron-up" ></button>

    <input class="w-8 h-10 rounded-sm text-center text-4xl text-supDarkPurple font-['Acme'] bg-gradient-to-r from-cyan-500 to-blue-500" type="text" v-model="goalCount" placeholder="0" />

    <button class="text-2xl text-lightWhite font-bold fa-sharp fa-solid fa-chevron-down"></button>
    <span>{{goalCount}}</span>
  </div>
</template>

<script>
export default {
  name: 'GoalCount',
};
</script>