<template>
    <div class="flex flex-col space-y-2">
        <img class="w-28 h-28 p-2" src="https://seeklogo.com/images/L/liverpool-fc-logo-3B886CFE17-seeklogo.com.png" alt="LiverPool">

        <span class="text-2xl text-center text-lightWhite font-bold font-['Acme']">
          {{ teamName }}
        </span>

    </div>
</template>

<script>
export default {
    name: 'TeamDetails',
    props: {
      teamName: String,
    }
}
</script>