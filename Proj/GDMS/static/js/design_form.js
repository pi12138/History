/* 通用功能：
 * 学生： 上传毕业设计 + 下载毕业设计
 * 教师： 下载毕业设计 + 审阅毕业设计
 * 管理员： 下载毕业设计 + 查看毕业设计结果
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


let designForm = new Vue({
    el: "#designForm",
    data: {
        filename: "",
        fileSize: "",
        file: "",

        subjectName: "",
        subject: "",
        uploadTime: "",
        downloadFileUrl: "",
        design: "",
        reviewOption: "",
        reviewTime: "",

    },
    methods: {
        uploadFile(){
            /* 上传文件到 input[type="file"] */
            let uploadBtn = this.$refs.uploadFile
            uploadBtn.click()
        },

        getFileInfo(event){
            /* 获取一些文件信息 */
            let file = event.target.files[0]
            this.file = file
            this.filename = file.name
            this.fileSize = file.size
        },

        showDesignForm(design, subjectName){
            if (design){
                this.getDesignData(design)
            }else{
                this.design = design
                this.subjectName = subjectName
            }

            this.$refs.designForm.classList.remove('hidden')
        },

        hiddenDesignForm(){
            this.$refs.designForm.classList.add('hidden')
        },

        submitDesignData(){
            /* 提交毕业设计表单 */
            if (this.design){
                this.alterDesignData()
            }else{
                this.createDesignData()
            }
        },

        createDesignData(){
            let url = 'http://127.0.0.1:8000/api/design/design/'
            let headers = getHeaders()
            headers['Content-Type'] = 'multipart/form-data'
            let formData = new FormData()
            formData.append('file', this.file)

            axios.post(url, formData, {headers: headers})
                .then(res => {
                    console.log(res.data.data)
                    alert("创建成功")
                })
                .catch(err => {
                    handleError(err)
                })

        },

        alterDesignData(){
            const url = 'http://127.0.0.1:8000/api/design/design/' + this.design + '/'
            let headers = getHeaders()
            headers['Content-Type'] = 'multipart/form-data'
            let formData = new FormData()
            formData.append('file', this.file)

            axios.put(url, formData, {headers: headers})
                .then(res => {
                    console.log(res.data.data)
                    alert("更新成功")
                    location.reload()
                })
                .catch(err => {
                    handleError(err)
                })
        },

        getDesignData(designId){
            const url = 'http://127.0.0.1:8000/api/design/design/' + designId + '/'
            axios.get(url)
                .then(res => {
                    let data = res.data.data
                    console.log(data)
                    this.subject = data.subject
                    this.subjectName = data.subject_name
                    this.design = data.id
                    this.downloadFileUrl = data.design
                    this.uploadTime = data.upload_time
                    this.reviewOption = data.review_option
                    this.reviewTime = data.review_time
                    this.filename = data.filename
                })
                .catch(err => {
                    handleError(err)
                })
        },

        downloadFile(){
            window.open(this.downloadFileUrl)
        },

        reviewDesignData(){
            const url = 'http://127.0.0.1:8000/api/design/design/' + this.design + '/'
            let headers = getHeaders()
            let data = {
                review_option: this.reviewOption,
                review_option: this.reviewOption,
                subject: this.subject
            }

            axios.patch(url, data, {headers: headers})
                .then(res => {
                    console.log(res.data.data)
                    alert("审核成功")
                    location.reload()
                })
                .catch(err => {
                    handleError(err)
                })
        }
    },
    computed: {
        fileInfo: function(){
            return `文件名: ${this.filename}`
        }
    }
})
