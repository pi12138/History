<template>
  <div class="container">
      <div id="article">
        
        <div v-html="compiledMarkdown" class="text-left"></div>
      </div>

      <Comment></Comment>
  </div>
</template>

<script>
// @ is an alias to /src
// import HelloWorld from '@/components/HelloWorld.vue'
import marked from 'marked'
import Comment from '../components/Comment.vue'

export default {
  name: 'Article',
  data(){
      return {
        id: 0,
        title: '',
        create_time: '',
        content: '',
        baseUrl: 'http://120.79.87.64:9999/api/blog/article/'
      }
  },
  components: {
    Comment
  },
  methods: {
      getArticle(){
          let url = `${this.baseUrl}${this.$route.params.id}`

          this.$axios.get(url)
          .then((result) => {
              let data = result.data
              this.id = data.id
              this.title = data.title
              this.create_time = data.create_time
              this.content = data.content
          }).catch((err) => {
              console.log(err.response)
          });
      }
  },
  computed: {
    compiledMarkdown: function() {
    return marked(this.content);
    },
  },

  beforeMount(){
      this.getArticle()
  }
}
</script>
