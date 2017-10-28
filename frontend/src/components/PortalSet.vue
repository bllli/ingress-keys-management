<template>
  <div class="ui bottom attached tab segment active">
    <div class="ui styled accordion">
      <div class="active title"><i class="dropdown icon"></i>Portal List</div>
      <div class="active content">
        <div class="accordion">
          <!-- 这里循环标签 -->
          <div class="ui divided items">
            <div class="item" v-for="po in portals">
              <div class="image">
                <img v-bind:src="po.image">
              </div>
              <div class="content">
                <a class="header">{{po.title}}</a>
                <div class="meta">
                  <span class="cinema"><a :href="po.link">{{po.link}}</a></span>
                </div>
                <div class="extra">
                  <div class="ui label" v-for="tag in po.tags">{{ tag.name }}</div>
                </div>
                <div class="description">
                  <p v-if="po.mykey > 0">系统记录中你拥有{{ po.mykey }}把key</p>
                </div>
              </div>
            </div>
          </div>
          <!--<div class="title"><i class="dropdown icon"></i> 城市 </div>-->
          <!--<div class="content">-->
          <!--<div class="accordion">-->
          <!--&lt;!&ndash; 这里插入pos &ndash;&gt;-->
          <!--<div class="title"><i class="dropdown icon"></i> po名 </div>-->
          <!--<div class="content">-->
          <!--{{ type }}-->
          <!--</div>-->
          <!--</div>-->
          <!--</div>-->
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'PortalSet',
    props: {
      type: {
        type: String,
        default: 'error'
      }
    },
    data() {
      return {
        portals: []
      }
    },
    created () {
      this.loadData(this.$router.currentRoute.path)
    },
    watch: {
    // 侦听路由变化，加载数据
      '$route' (to, from) {
        this.loadData(to.path)
      }
    },
    methods: {
      loadData() {
        $('.ui.accordion').accordion()
        const self = this
        this.axios.get('/api/portals/?query=' + self.type, {})
          .then(response => {
            console.log(response)
            self.portals = response.data.results
            $('.ui.accordion').accordion('refresh')
          })
          .catch(error => {
            console.log(error)
        })
      }
    }
  }
</script>
