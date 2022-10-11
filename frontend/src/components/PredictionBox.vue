<template>
    <div class="flex flex-col">
        <form action="">
            <MatchBox />
        </form>
    </div>
</template>

<script>
import MatchBox from '@/components/MatchBox.vue'

export default {
    name: 'PredictionBox',
    components: {
        MatchBox
    }
}
</script>