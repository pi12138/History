/* 通用功能：
 * 学生： 上传毕业论文 + 下载毕业论文
 * 教师： 下载毕业论文 + 审阅毕业论文
 * 管理员： 下载毕业论文 + 查看毕业论文结果
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


let thesisForm = new Vue({
    el: "#thesisForm",
    data: {
        subject: "",
        subjectName: "",
        keyWords: "",
        summary: "",
        thesisId: "",
        uploadTime: "",
        reviewOption: "",
        reviewTime: "",

        file: "",
        filename: "",
        downloadFileUrl: ""
    },
    methods: {
        showThesisForm(thesisId, subjectName){
            if (thesisId){
                this.getThesisForm(thesisId)
            }else{
                this.thesisId = thesisId
                this.subjectName = subjectName
            }

            this.$refs.thesisForm.classList.remove('hidden')
        },

        hiddenThesisForm(){
            this.$refs.thesisForm.classList.add('hidden')
        },

        submitThesisForm(){
            if (this.thesisId){
                this.alterThesisForm()
            }else{
                this.createThesisForm()
            }
        },

        createThesisForm(){
            /* 创建毕业论文 */
            const url = 'http://127.0.0.1:8000/api/design/thesis/'
            let headers = getHeaders()
            headers['Content-Type'] = 'multipart/form-data'
            let formData = new FormData()
            formData.append('file', this.file)
            formData.append('words', this.keyWords)
            formData.append('summary', this.summary)

            axios.post(url, formData, {headers: headers})
                .then(res => {
                    console.log(res.data.data)
                    alert("提交成功")
                })
                .catch(err => {
                    handleError(err)
                })
        },

        alterThesisForm(){
            /* 修改毕业论文 */
            const url = 'http://127.0.0.1:8000/api/design/thesis/' + this.thesisId + '/'
            let headers = getHeaders()
            headers['Content-Type'] = 'multipart/form-data'
            let formData = new FormData()
            formData.append('file', this.file)
            formData.append('words', this.keyWords)
            formData.append('summary', this.summary)

            axios.put(url, formData, {headers:headers})
                .then(res => {
                    console.log(res.data.data)
                    alert("修改成功")
                })
                .catch(err => {
                    handleError(err)
                })
        },

        getThesisForm(thesisId){
            const url = 'http://127.0.0.1:8000/api/design/thesis/' + thesisId + '/'
            axios.get(url)
                .then(res => {
                    let data = res.data.data
                    console.log(data)

                    this.subject = data.subject
                    this.subjectName = data.subject_name
                    this.keyWords = data.words
                    this.summary = data.summary
                    this.thesisId = data.id
                    this.uploadTime = data.upload_time
                    this.reviewOption = data.review_option
                    this.reviewTime = data.review_time
                    this.filename = data.filename
                    this.downloadFileUrl = data.thesis
                })
                .catch(err => {
                    handleError(err)
                })
        },

        reviewThesisForm(){
            /* 审核毕业设计论文 */
            const url = 'http://127.0.0.1:8000/api/design/thesis/' + this.thesisId + '/'
            let headers = getHeaders()
            let data = {
                review_option: this.reviewOption,
                words: this.keyWords,
                subject: this.subject
            }

            axios.patch(url, data, {headers: headers})
                .then(res => {
                    console.log(res.data.data)
                    alert("审核成功")
                })
                .catch(err => {
                    handleError(err)
                })

        },

        downloadFile(){
            window.open(this.downloadFileUrl)
        },

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
        },
    }
})