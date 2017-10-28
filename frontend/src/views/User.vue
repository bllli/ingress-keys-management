<template>
  <div class="ui text container">
    <h3 class="ui dividing header"><a v-bind:href="url">{{ username }}</a></h3>
    <div class="ui top attached tabular menu">
      <router-link class="item" to="/user">Home</router-link>
      <router-link class="item" to="/user/upload_portals">My Upload Portals</router-link>
      <router-link class="item" to="/user/own_key_portals">Own-Key Portals</router-link>
    </div>
    <router-view></router-view>
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
      $('.menu .item').tab()
      const self = this
      this.axios.get('/api/users/?query=myself', {
      }).then(function (response) {
        console.log(response)
        self.username = response.data.username
        self.url = response.data.url
      }).catch(function (error) {
        console.log(error)
      })
    }
  }
</script>
