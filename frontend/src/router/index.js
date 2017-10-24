import Vue from 'vue'
import VueRouter from 'vue-router'
import hello from '../components/HelloWorld.vue'
import User from '../views/User.vue'
import Login from '../views/Login.vue'
import store from '../store/store'
import * as types from '../store/types'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: '/',
    component: hello
  },
  {
    path: '/user',
    name: 'user',
    meta: {
      requireAuth: true
    },
    component: User
  },
  {
    path: '/login',
    name: 'login',
    component: Login
  }
]

// 页面刷新时，重新赋值token
if (window.localStorage.getItem('token')) {
  store.commit(types.LOGIN, window.localStorage.getItem('token'))
}

const router = new VueRouter({
  routes
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(r => r.meta.requireAuth)) {
    if (store.state.token) {
      next()
    } else {
      next({
        path: '/login',
        query: {redirect: to.fullPath}
      })
    }
  } else {
    next()
  }
})

export default router
