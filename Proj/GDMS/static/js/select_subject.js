/* 学生模块: 选择课题 */

var subjectList = new Vue({
    el: "#subjectList",
    data: {
        formData: "",
        tableData: "",
        subjectName: "",
        office: 0,
        officeList: "",
        questioner: "",
        nextUrl: "",
        previousUrl: "",
        count: "",
        numPages: "",
        page: "",

        url: 'http://127.0.0.1:8000/api/subject/select_subject/'
    },
    methods: {
        getSubjectList(url){
            /* 获取课题列表 */

            const params = {
                subject_name: this.subjectName,
                office: this.office,
                questioner: this.questioner
            }

            axios.get(url, {params: params})
                .then(res => {
                    console.log(res)
                    const data = res.data
                    this.tableData = data.results
                    this.nextUrl = data.next_url
                    this.previousUrl = data.previous_url
                    this.count = data.count
                    this.numPages = data.num_pages
                    this.page = data.page

                    this.setBtnDisable()
                })
                .catch(error => {
                    console.log(error)
                    console.log(error.response)
                    alert("Error")
                })
        },

        setBtnDisable(){
            /* 设置按钮是否可以点击 */

            if (this.nextUrl == null){
                this.$refs.nextBtn.classList.add('disabled')
            }else{
                this.$refs.nextBtn.classList.remove('disabled')
            }

            if (this.previousUrl == null){
                this.$refs.previousBtn.classList.add('disabled')
            }else{
                this.$refs.previousBtn.classList.remove('disabled')
            }
        },

        getSubjectInfo(index){
            const subject = this.tableData[index]
            markForm.setFormShow(subject)
        },

        selectSubject(subject){
            const url = `http://127.0.0.1:8000/api/subject/select_subject/`
            const csrfToken = getCookie('csrftoken')
            const headers = {
                headers: {
                    'X-CSRFToken': csrfToken
                }
            }
            const data = {
                'subject': subject.id
            }


            axios.post(url, data, headers)
                .then(res => {
                    console.log(res)
                    alert(res.data.msg)
                    location.reload()
                })
                .catch(error => {
                    console.log(error)
                    console.log(error.response)
                    // alert("Error")
                    alert(error.response.data)
                })
        },

        getOfficeList() {
            const url = 'http://127.0.0.1:8000/organization/offices/'
            const params = {
                'faculty': document.getElementsByName('facultyId')[0].value
            }
            axios.get(url, {params: params})
                .then(res => {
                    console.log(res)
                    const defaultData = {id: 0, name: "请选择教研室"}
                    res.data.push(defaultData)

                    this.officeList = res.data
                })
                .catch(error => {
                    console.log(error.response)
                })
        },

        showMySubject(){
            mySubject.showSubject()
        }

    },

    filters: {
        getInfo: function (value) {
            /* 获取课题老师的个人联系方式 */
            return `联系方式: ${value.teacher_phone}\nQQ: ${value.teacher_qq}\n邮箱: ${value.teacher_email}`
        },

        getApplyInfo: function (value) {
            /* 获取课题的申请状况并且给以提示 */
            if (value.apply_student == null){
                return "当前课题还无人申请"
            }else{
                return `当前课题已经有人申请\n申请人: ${value.apply_student}`
            }
        }
    },

    beforeMount(){
        const url = this.url
        this.getSubjectList(url)
        this.getOfficeList()
    }

})


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


const markForm = new Vue({
    el: "#markForm",
    data: {
        formData: "",
    },
    methods: {
        setFormShow(formData){
            console.log(formData)
            this.formData = formData
            this.$refs.markForm.classList.remove('hidden')
        },

        submitForm(subjectId){
            const url = "http://127.0.0.1:8000/api/subject/pending_subject/" + subjectId + '/'
            const csrfToken = getCookie('csrftoken')
            const headers = {
                headers: {
                    'X-CSRFToken': csrfToken
                }
            }
            axios.patch(url, this.formData, headers)
                .then(res => {
                    console.log(res)
                    alert(res.data.msg)
                })
                .catch(error => {
                    console.log(error)
                    console.log(error.response)
                    alert('Error')
                })
        },

        closeForm(){
            this.$refs.markForm.classList.add('hidden')
            location.reload()
        }

    },

})


const mySubject = new Vue({
    el: "#mySubject",
    data: {
        selectSubject: "",
        applySubject: ""
    },
    methods: {
        showSubject(){
            this.$refs.mySubject.classList.remove('hidden')

        },

        getMySubject(){
            const url = 'http://127.0.0.1:8000/api/subject/my_subject/'

            axios.get(url)
                .then(res => {
                    const data = res.data
                    console.log(data)

                    this.selectSubject = data.select_subject
                    this.applySubject = data.apply_subject
                    // mySubject.showSubject()

                })
                .catch(error => {
                    console.log(error)
                    console.log(error.response)
                    alert("Error")
                })
        }
    },

    beforeMount() {
        this.getMySubject()
    }
})