<template>
  <div class="home container">
    <!-- <img alt="Vue logo" src="../assets/logo.png"> -->
    <!-- <HelloWorld msg="Welcome to Your Vue.js App"/> -->
    <Task></Task>
  </div>
</template>

<script>
// @ is an alias to /src
// import HelloWorld from '@/components/HelloWorld.vue'
import Task from '../components/Task.vue'

export default {
  name: 'Home',
  components: {
    // HelloWorld
    Task
  }
}
</script>
