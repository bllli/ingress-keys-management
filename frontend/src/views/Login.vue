<template>
  <div class="ui middle aligned center aligned grid">
    <div class="column">
      <h2 class="ui teal image header">
        <img src="../assets/logo.png" class="image">
        <div class="content">
          Ingress keys Management
        </div>
      </h2>
      <div class="ui warning message" v-show="login_error">
        <i class="close icon"></i>
        <div class="header">
          账号或密码错误！
        </div>
        请检查并重试。如需帮助请邮件联系管理员 me#bllli.cn (# -> @)
      </div>
      <form class="ui large form" @submit.prevent="login">
        <div>
          <div class="ui stacked segment">
            <div class="field">
              <div class="ui left icon input">
                <i class="user icon"></i>
                <input type="text" name="username" placeholder="用户名" v-model="user.username">
              </div>
            </div>
            <div class="field">
              <div class="ui left icon input">
                <i class="lock icon"></i>
                <input type="password" name="password" placeholder="密码" v-model="user.password">
              </div>
            </div>
            <button type="submit" class="ui fluid large teal submit button">登录</button>
          </div>

          <div class="ui error message"></div>
        </div>
      </form>

      <div class="ui message">
        New to us? <a href="#">注册</a>
      </div>
    </div>
  </div>
</template>

<script>
  import * as types from '../store/types'
  import $ from 'jquery'
  /* eslint-disable no-unused-vars */
  const semantic = require('../../semantic/dist/semantic.js')
  export default {
    name: '',
    data () {
      return {
        user: {
          username: '',
          password: ''
        },
        login_error: false,
        msg: ''
      }
    },
    mounted () {
      this.$store.commit(types.TITLE, 'Login')
    },
    methods: {
      login () {
        const self = this

        if (this.user.username && this.user.password) {
//          console.log('username: ' + this.user.username + ' password: ' + this.user.password + ' IN LOGIN VUE')
          this.axios({
            method: 'post',
            url: '/api/token/',
            data: {
              username: self.user.username,
              password: self.user.password
            }
          }).then(function (response) {
            self.$store.commit(types.LOGIN, response.data.token)
//            console.log('token got: ', response.data.token)
            let redirect = decodeURIComponent(self.$route.query.redirect || '/')
            self.$router.push({
              path: redirect
            })
          }).catch(function (error) {
//            console.log('error: ', error)
            self.login_error = true
          })
        }
      }
    }
  }

  $(document)
    .ready(function () {
      $('.ui.form')
        .form({
          fields: {
            username: {
              identifier: 'username',
              rules: [
                {
                  type: 'empty',
                  prompt: '请输入用户名'
                },
                {
                  type: 'length[3]',
                  prompt: '请输入正确的用户名'
                }
              ]
            },
            password: {
              identifier: 'password',
              rules: [
                {
                  type: 'empty',
                  prompt: '还没有输入密码呢'
                },
                {
                  type: 'length[6]',
                  prompt: '密码至少是六位数'
                }
              ]
            }
          }
        })
    })
</script>
