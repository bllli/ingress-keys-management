<template>

</template>

<script>
  export default {
    name: 'Portal',
    data () {
      return {

      }
    },
    mounted: function () {
      const self = this
      this.axios.get('/api/portals//')
    }
  }
</script>
