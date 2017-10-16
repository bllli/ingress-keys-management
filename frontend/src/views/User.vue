<template>
  <div>
    {{ username }}
  </div>
</template>

<script>
  export default {
    name: 'User',
    data () {
      return {
        username: '',
        url: ''
      }
    },
    mounted: function () {
      const self = this
      this.axios.get('/api/myself/', {
      }).then(function (response) {
        console.log(response)
        self.username = response.data.user
      }).catch(function (error) {
        console.log(error)
      })
    }
  }
</script>
