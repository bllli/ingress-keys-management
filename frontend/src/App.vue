<template>
  <div id="app">
    <div class="ui menu">
      <div class="header item">
        <router-link to="/">Key-logo</router-link>
      </div>
      <router-link to="/user" class="item">用户</router-link>
      <a class="item">Link</a>
      <div class="ui dropdown item" tabindex="0">
        Dropdown
        <i class="dropdown icon"></i>
        <div class="menu" tabindex="-1">
          <div class="item">Action</div>
          <div class="item">Another Action</div>
          <div class="item">Something else here</div>
          <div class="divider"></div>
          <div class="item">Separated Link</div>
          <div class="divider"></div>
          <div class="item">One more separated link</div>
        </div>
      </div>
      <div class="right menu">
        <div class="item">
          <div class="ui action left icon input">
            <i class="search icon"></i>
            <input type="text" placeholder="Search">
            <button class="ui button">提交</button>
          </div>
        </div>
        <a class="item" v-show="token" v-on:click="logout">登出</a>
        <router-link to="login" class="item" v-show="!token">登录/注册</router-link>
      </div>
    </div>
    <!--<hello></hello>-->
    <!--<course-set></course-set>-->
    <router-view class="view"></router-view>
  </div>
</template>

<script>
  import $ from 'jquery'
  import {mapState} from 'vuex'
  import * as types from './store/types'

  import hello from './components/HelloWorld.vue'
  import User from './views/User.vue'
  import Login from './views/Login.vue'

  const inBrowser = typeof window !== 'undefined'
  if (inBrowser) {
    /* eslint-disable no-unused-vars */
    var semantic = require('../semantic/dist/semantic.js')
  }

  export default {
    name: 'app',
    mounted: function () {
      $('.ui.dropdown').dropdown()
    },
    computed: mapState({
      title: state => state.title,
      token: state => state.token
    }),
    components: {hello, Login, User},
    methods: {
      logout () {
        this.$store.commit(types.LOGOUT)
        this.$router.push({
          path: '/'
        })
      }
    }
  }
</script>

<style>
  @import '../semantic/dist/semantic.css';
  .column {
    max-width: 600px;
  }
</style>
