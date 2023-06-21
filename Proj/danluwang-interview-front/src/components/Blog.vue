<template>
  <div class="container">
      <ul class="list-group list-group-flush col-md-10 offset-md-1">
        <router-link class="list-group-item" v-for="(item, index) in blogList" :key="index" :to="articleUrl(item.id)">
            <div v-text="item.title" class="text-left float-left"></div>
            <div v-text="item.create_time" class="float-right text-dark"></div>
        </router-link>
      </ul>
  </div>

 
</template>

<script>
// @ is an alias to /src
// import HelloWorld from '@/components/HelloWorld.vue'

export default {
  name: 'Blog',
  data(){
      return {
        blogList: [
            // {'title': '第一篇文章', id: 1},
            // {'title': '第二篇文章', id: 2}
        ],
        baseUrl: 'http://120.79.87.64:9999/api/blog/article/'
      }
  },
  methods: {
      getBlogList(){
          let url = this.baseUrl

          this.$axios.get(url)
          .then((result) => {
              this.blogList = result.data
          }).catch((err) => {
              console.log(err.response)
          });
      },

      articleUrl(articleId){
          return `/article/${articleId}`
      }
  },

  beforeMount(){
      this.getBlogList()
  }
}
</script>
