/*
* 公告功能
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

const announcement = new Vue({
    el: "#announcement",
    data: {
        announcementList: "",
        title: "",
        publisher: "",
        publisher_name: "",
        publish_time: "",
        publish_content: "",
        file: "",
        filename: "",
        fileUrl: "",
        announcementId: "",

        nextUrl: "",
        previousUrl: "",
        page: ""
    },
    methods: {

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

        getAnnouncementList(url){

            if (!url){
                alert("当前页不存在")
                return
            }

            axios.get(url)
                .then(res => {
                    console.log(res)
                    let data = res.data
                    this.announcementList = data.results
                    this.nextUrl = data.next
                    this.previousUrl = data.previous
                    this.page = data.page
                })
        },

        createAnnouncement(){
            /* 创建公告 */
            let url = 'http://127.0.0.1:8000/api/announcement/'
            let headers = getHeaders()
            headers['Content-Type'] = 'multipart/form-data'
            let formData = new FormData()
            formData.append('title', this.title)
            formData.append('publish_content', this.publish_content)

            if (this.file){
                formData.append('file', this.file)
            }

            axios.post(url, formData, {headers: headers})
                .then(res => {
                    console.log(res.data)
                    alert("创建公告成功")
                })
                .catch(err => {
                    handleError(err)
                })
        },

        getAnnouncement(announcementId){
            /* 获取指定公告 */
            let url = `http://127.0.0.1:8000/api/announcement/${announcementId}/`

            axios.get(url)
                .then(res => {
                    console.log(res)
                    let data = res.data.data

                    this.title = data.title
                    this.publisher = data.publisher_name
                    this.publish_time = data.publish_time
                    this.publish_content = data.publish_content
                    this.filename = data.filename
                    this.announcementId = data.id
                })
                .catch(err => {
                    handleError(err)
                })
        },

        deleteAnnouncement(announcementId){
            /* 删除公告 */
            let url = `http://127.0.0.1:8000/api/announcement/${announcementId}/`
            let headers = getHeaders()

            axios.delete(url, {headers: headers})
                .then(res => {
                    console.log(res)
                    alert("删除成功")
                    location.reload()
                })
                .catch(err => {
                    handleError(err)
                })
        },

        downloadFile(){
            /* 下载文件 */
            if (!this.fileUrl){
                alert("没有文件不可下载")
                return
            }
            window.open(this.fileUrl)
        },

        hiddenAnnouncementForm(){
            this.$refs.announcementForm.classList.add('hidden')
            // this.title = this.publisher_name = this.publish_time = this.file = this.filename = this.publish_content = ""
            location.reload()
        },

        showAnnouncement(index){
            /* 查看公告详情 */

            let data = this.announcementList[index]

            this.title = data.title
            this.publish_content = data.publish_content
            this.publisher_name = data.publisher_name
            this.publish_time = data.publish_time
            this.fileUrl = data.publish_file
            this.filename = data.filename

            this.$refs.submitBtn.setAttribute('disabled', 'disabled')
            this.$refs.announcementForm.classList.remove('hidden')
        },

        writeAnnouncement(){
            /* 填写公告 */
            this.$refs.announcementForm.classList.remove('hidden')
        }
    },

    beforeMount(){
        const url = 'http://127.0.0.1:8000/api/announcement/'
        this.getAnnouncementList(url)
    }
})