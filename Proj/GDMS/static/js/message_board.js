/*
* 留言板功能
* */

function handleError(error){
    console.log(error)
    console.log(error.response)
    alert("Error")
}

function getCookie(name){
    /* 获取cookie中的csrftoken */
    var name = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0; i<ca.length; i++){
        var c = ca[i].trim();
        if (c.indexOf(name)==0) return c.substring(name.length,c.length);
    }
    return "";
}

function getHeaders() {
    /* 为获取post, put, patch请求获取headers*/
    let csrfToken = getCookie('csrftoken')
    let headers = {
        'X-CSRFToken': csrfToken
    }

    return headers
}


let messageBoard = new Vue({
    el: "#messageBoard",
    data: {
        title: "",
        content: "",
        annex: "",
        publisher: "",
        receiver: "",
        publish_time: "",
        is_read: false,

        publisher_name: "",
        receiver_name: "",
        filename: "",
        file: "",
        receiveMessageList: "",
        publishMessageList: "",
        guidedStudentList: "",
        messageList: "",

        page1: "",
        page2: "",
        previousUrl1: "",
        previousUrl2: "",
        nextUrl1: "",
        nextUrl2: "",

    },
    methods: {
        hiddenMessageBoardForm(){
            /* 关闭留言板表单 */
            this.$refs.messageBoardForm.classList.add('hidden')
            this.title = this.content = this.annex = this.publisher = this.receiver = this.publish_time = ""
            this.publisher_name = this.receiver_name = this.filename = this.file = ""
            this.$refs.submitBtn.removeAttribute('disabled')
            this.$refs.uploadBtn.removeAttribute('disabled')
        },

        showMessageBoardForm(){
            /* 显示留言板表单 */
            this.getUserInfo()
            this.$refs.messageBoardForm.classList.remove('hidden')
        },

        uploadFile(){
            /* 上传文件 */
            let uploadBtn = this.$refs.uploadFile
            uploadBtn.click()
        },

        getFileInfo(event){
            /* 获取文件数据 */
            let file = event.target.files[0]
            this.file = file
            this.filename = file.name
        },

        downloadFile(){
            if (this.annex){
                window.open(this.annex)
            }else{
                alert("当前没有文件")
            }
        },

        createMessage(){
            /* 创建留言 */
            let url = 'http://127.0.0.1:8000/api/message_board/'
            let headers = getHeaders()
            headers['Content-Type'] = 'multipart/form-data'

            let formData = new FormData()
            formData.append('title', this.title)
            formData.append('content', this.content)
            formData.append('publisher', this.publisher)
            formData.append('receiver', this.receiver)

            if (this.file){
                formData.append('file', this.file)
            }

            axios.post(url, formData, {headers: headers})
                .then(res => {
                    console.log(res)
                    alert("创建留言成功")
                    location.reload()
                })
                .catch(err => {
                    handleError(err)
                })
        },

        getReceiveMessage(url){
            /* 获取接收到的消息 */
            if (!url){
                alert('没有当前页')
                return
            }

            axios.get(url)
                .then(res => {
                    console.log(res)
                    let data = res.data
                    this.receiveMessageList = data.results
                    this.previousUrl1 = data.previous
                    this.nextUrl1 = data.next
                    this.page1 = data.page
                })
                .catch(err => {
                    handleError(err)
                })
        },

        getPublishMessage(url){
            /* 获取发送的消息 */
            if (!url){
                alert('没有当前页')
                return
            }

            axios.get(url)
                .then(res => {
                    console.log(res)
                    let data = res.data
                    this.publishMessageList = data.results
                    this.previousUrl2 = data.previous
                    this.nextUrl2 = data.next
                    this.page2 = data.page
                })
                .catch(err => {
                    handleError(err)
                })
        },

        submitMessageForm(){
            if (this.publisher && this.receiver){
                this.createMessage()
            }else{
                alert("没有发信人信息或接收人信息")
                return
            }

        },

        getUserInfo(){
            /* 获取用户身份信息 */
            let url = 'http://127.0.0.1:8000/api/user/user_info/'

            axios.get(url)
                .then(res => {
                    console.log(res)
                    this.handleInfo(res.data)

                })
                .catch(err => {
                    handleError(err)
                })
        },

        handleInfo(data){
            /* 根据用户身份,处理用户信息 */
            if (data.role == 'student'){
                this.publisher = data.user_id
                this.publisher_name = data.student_name
                this.receiver = data.guide_teacher_user_id
                this.receiver_name = data.guide_teacher_name
            }else if(data.role == 'teacher'){
                this.publisher = data.user_id
                this.publisher_name = data.teacher_name
                this.guidedStudentList = data.guided_students
            }else if(data.role == 'administrator'){
                studentList.getStudentList(studentList.url)
            }
        },

        viewMessageForm(item, type){
            /* 展示单个留言信息 */
            this.title = item.title
            this.content = item.content
            this.publisher_name = item.publisher_info.name
            this.receiver_name = item.receiver_info.name
            this.receiver = item.receiver
            this.publish_time = item.publish_time
            this.annex = item.annex
            this.filename = item.filename

            this.$refs.submitBtn.setAttribute('disabled', 'disabled')
            this.$refs.uploadBtn.setAttribute('disabled', 'disabled')
            this.$refs.messageBoardForm.classList.remove('hidden')

            if (type == 0){
                this.setMessageIsRead(item)
            }
        },

        viewMessageForm2(item, type){
            /* 展示单个留言信息 */
            this.title = item.title
            this.content = item.content
            this.publisher_name = item.publisher_info.name
            this.receiver_name = item.receiver_info.name
            this.publish_time = item.publish_time
            this.annex = item.annex
            this.filename = item.filename

            this.$refs.submitBtn2.setAttribute('disabled', 'disabled')
            this.$refs.uploadBtn2.setAttribute('disabled', 'disabled')
            this.$refs.messageBoardForm2.classList.remove('hidden')

            if (type == 0){
                this.setMessageIsRead(item)
            }
        },

        setMessageIsRead(item){
            /* 设置消息已读 */
            let url = `http://127.0.0.1:8000/api/message_board/${item.id}/read_message/`

            axios.get(url)
                .then(res => {
                    console.log(res)
                    item.is_read = true
                })
                .catch(err => {
                    handleError(err)
                })
        },

        is_read_text(is_read){
            if (is_read == true){
                return "已读"
            }else{
                return "未读"
            }
        },

        hiddenMessageBoardForm2(){
            /* 关闭留言板表单 */
            this.$refs.messageBoardForm2.classList.add('hidden')
            this.title = this.content = this.annex = this.publisher = this.receiver = this.publish_time = ""
            this.publisher_name = this.receiver_name = this.filename = this.file = ""
            this.$refs.submitBtn2.removeAttribute('disabled')
        },

        getMessageList(studentId){
            /* 根据学生获取交流列表 */
            let url = 'http://127.0.0.1:8000/api/message_board/?user_id=' + studentId

            axios.get(url)
                .then(res => {
                    console.log(res)
                    this.messageList = res.data.results

                    this.$refs.messageList.classList.remove('hidden')
                })
                .catch(err => {
                    handleError(err)
                })
        },

        hiddenMessageList(){
            this.$refs.messageList.classList.add('hidden')
        }

    },

    beforeMount() {
        let url1 = 'http://127.0.0.1:8000/api/message_board/receive_message/'
        let url2 = 'http://127.0.0.1:8000/api/message_board/publish_message/'

        this.getUserInfo()
        this.getReceiveMessage(url1)
        this.getPublishMessage(url2)
    }
})


let studentList = new Vue({
    el: "#studentList",
    data: {
        studentList: "",
        url: "http://127.0.0.1:8000/api/user/selected_students/",
        nextUrl: "",
        previousUrl: "",
        page: "",
    },
    methods: {
        getStudentList(url){
            axios.get(url)
                .then(res => {
                    console.log(res)
                    let data = res.data
                    this.studentList = data.results
                    this.nextUrl = data.next
                    this.previousUrl = data.previous
                    this.page = data.page
                })
                .catch(err => {
                    handleError(err)
                })
        },

        viewMessageList(studentId){
            messageBoard.getMessageList(studentId)
        }
    }
})