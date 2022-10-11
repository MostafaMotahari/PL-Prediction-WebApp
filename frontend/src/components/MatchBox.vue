<template>
    <div class="flex flex-row justify-center        items-center space-x-5 p-5 my-3 bg-supDarkPurple rounded-xl shadow-2xl shadow-dark">

      <TeamDetails teamName="Liverpool"/>

      <GoalCount />

      <span>VS</span>

      <!-- <GoalCount /> -->

      <TeamDetails teamName="Brighton"/>
    </div>
</template>

<script>
import TeamDetails from '@/components/TeamDetails.vue'
import GoalCount from '@/components/GoalCount.vue'

export default {
  name: 'MatchBox',
  components: {
      TeamDetails,
      GoalCount
  }
}
</script>