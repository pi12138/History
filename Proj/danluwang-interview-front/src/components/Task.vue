<template>
  <div class="task">
      <form @submit.prevent>
          <div class="row">
            <div class="form-group col-md-6 offset-md-3">
                <input type="text" class="form-control" v-on:keyup.enter="addTask" v-model="title" maxlength="30">
            </div>
          </div>
      </form>
    
      <ul class="list-group col-md-6 offset-md-3">
        <li class="list-group-item" v-for="(item, index) in taskList" :key="index" v-show="status==2 || item.status==status">
          <div class="row">
            <div v-text="item.title" class="col-md-7 text-left"></div>
            <button class="col-md-2 btn btn-primary btn-sm" v-text="btnInfo(item.status)" @click="alterTaskStatus(item)"></button>
            <button class="col-md-2 offset-md-1 btn btn-secondary btn-sm" @click="deleteTask(index)">delete</button>
          </div>
        </li>
      </ul>
      
      <br>
      <div class="btn-group btn-group-lg" role="group" v-if="taskList.length != 0">
        <button type="button" :class="{'btn': true, 'btn-primary': status==2}" @click="changeStatus(2)">All</button>
        <button type="button" :class="{'btn': true, 'btn-primary': status==0}" @click="changeStatus(0)">Active</button>
        <button type="button" :class="{'btn': true, 'btn-primary': status==1}" @click="changeStatus(1)">Completed</button>
        <button type="button" class="btn" v-if="completedTaskList.length" @click="deleteCompletedTask">clear completed</button>
      </div>

      <div class="row">
        <div class="alert alert-light col-md-6 offset-md-3" role="alert">
          {{ this.taskList.length - this.completedTaskList.length }} item left
        </div>
      </div>
  </div>
</template>

<script>
// @ is an alias to /src
// import HelloWorld from '@/components/HelloWorld.vue'

export default {
  name: 'Task',
  components: {
    // HelloWorld
    
  },
  data(){
    return {
        taskList: [{'title': "xxx"}],
        baseUrl: 'http://120.79.87.64:9999/api/todo_mvc/task/',
        title: "",
        status: 2,
        completedTaskList: []
    }
  },
  methods: {
      getTaskList(){
        // 获取任务列表
          let url = this.baseUrl

          this.$axios.get(url)
          .then((result) => {
              this.taskList = result.data
              
              this.appendCompletedTask()
          }).catch((err) => {
              console.log(err.response)
          });

      },
      
      addTask(){
        // 添加任务
          let url = this.baseUrl
          let data = {
              title: this.title
          }

          this.$axios.post(url, data)
          .then((result) => {
              this.taskList.push(result.data)
          }).catch((err) => {
              console.log(err.response)
          });
      },

      alterTaskStatus(item){
        // 修改任务状态
        let url = this.baseUrl + `${item.id}/`
        let statusDict = {
          "0": 1,
          "1": 0
        }

        this.$axios.patch(url, {status: statusDict[item.status]})
        .then((result) => {
          item.status = result.data.status

          if (item.status == 1){
            this.addCompletedTask(result.data.id)
          }
        }).catch((err) => {
          console.log(err.response)
        });
      },

      deleteTask(index){
        // 删除单个任务
        let item = this.taskList[index]
        let url = this.baseUrl + `${item.id}/`

        this.$axios.delete(url)
        .then((result) => {
          if (result.data.data === "ok"){
            this.taskList.splice(index, 1)
          }

          if (item.status == 1){
            // 如果任务已完成，删除已完成列表中的任务
            this.popCompletedTask(item.id)
          }

        }).catch((err) => {
          console.log(err.response)
        });

      },

      btnInfo(itemStatus){
        // 按钮文字显示
        if (itemStatus == 0){
          return `Done`
        }else if (itemStatus == 1){
          return `Undone`
        }
      },

      changeStatus(status){
        /* 改变status来改变显示列表
          status：0,1,2
          2：all
          1：compeleted
          0：active
        */
        this.status = status
      },

      deleteCompletedTask(){
        // 删除已完成的任务列表
        let url = this.baseUrl + 'clear_completed/'
        let data = {
          'pk_list': this.completedTaskList
        }

        this.$axios.post(url, data)
        .then((result) => {
          if (result.data.data == 'ok'){
            this.clearCompletedTask()
          }
        }).catch((err) => {
          console.log(err.response)
        });
      },

      addCompletedTask(itemId){
        // 添加已完成任务到已完成任务列表
        this.completedTaskList.push(itemId)
      },

      popCompletedTask(itemId){
        // 从已完成任务列表移除任务
        let index = -1
        for(let i=0; i<this.completedTaskList.length; i++){
          if (itemId == this.completedTaskList[i]){
            index = i
          }    
        }

        this.completedTaskList.splice(index, 1)
      },

      clearCompletedTask(){
        // 清空已完成任务列表
        this.completedTaskList = []
        this.getTaskList()
      },

      appendCompletedTask(){
        // 获取任务列表时，给已完成任务列表填充数据
        for (let i=0; i<this.taskList.length; i++){
          if(this.taskList[i].status == 1){
            this.completedTaskList.push(this.taskList[i].id)
          }
        }
        console.log(this.completedTaskList)
      }
  },

  beforeMount(){
      this.getTaskList()

  }
}
</script>
