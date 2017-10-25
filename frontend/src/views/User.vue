<template>
  <div class="ui middle aligned center">
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
      this.axios.get('/api/users/?query=myself', {
      }).then(function (response) {
        console.log(response)
        self.username = response.data.username
      }).catch(function (error) {
        console.log(error)
      })
    }
  }
</script>
