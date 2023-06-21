/* 教师功能: 毕业设计过程 */


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


const subjectList = new Vue({
    el: "#subjectList",
    data: {
        url: 'http://127.0.0.1:8000/api/subject/selected_subject/',
        subjectList: "",
        nextUrl: "",
        previousUrl: "",
        count:"",
        numPages: "",
        page: ""
    },
    methods: {
        getSubjectList(url){
            axios.get(url)
                .then(res => {
                    const data = res.data
                    console.log(data)

                    this.subjectList = data.results
                    this.nextUrl = data.next_url
                    this.previousUrl = data.previous_url
                    this.count = data.count
                    this.numPages = data.num_pages
                    this.page = data.page
                    this.setBtnDisable()
                })
                .catch(error => {

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

        handleTaskBook(taskId, taskStatus){
            /* 处理任务书字段 */

            if (taskId == null){
                return `<span>未填写</span>`
            }else if(taskId != null && taskStatus == 0){
                return `<a href="#">审核</a>`
            }else if(taskId != null && taskStatus == 1){
                return `<a>查看</a>`
            }else if(taskId != null && taskStatus == 2){
                return `<span>不合格</span>`
            }else{
                return `<span></span>`
            }
        },

        reviewOrViewTaskBook(index, taskStatus){
            /* 填写课题任务书或者查看课题任务书 */
            const taskId = this.subjectList[index].task_book

            if (taskId == null || taskStatus == 2){
                alert("非法操作")
                return
            }

            taskBookForm.showTaskBook(taskId)
        },

        handleReport(report){
            /* 处理 开题报告 字段 */
            if (report == null){
                return `<span>未填写</span>`
            }

            if (report.review_result == 0){
                return `<a href="#">待审核</a>`
            }else if (report.review_result == 1 || report.review_result == 2 ){
                return `<a href="#">查看</a>`
            }
        },

        reviewOrViewReport(index){
            const reportId = this.subjectList[index].report.id
            const subjectName = this.subjectList[index].subject_name
            reportForm.showReportForm(reportId, subjectName)
        },

        handleDesign(design){
            /* 处理毕业设计字段 */
            if (design == null){
                return `<span>未填写</span>`
            }

            if (design.review_option){
                return `<a href="#">查看</a>`
            }else{
                return `<a href="#">审阅</a>`
            }
        },

        reviewOrViewDesign(index){
            /* 审核或者查看毕业设计 */
            let designId = this.subjectList[index].design.id
            let subjectName = this.subjectList[index].subject_name
            designForm.showDesignForm(designId, subjectName)
        },

        handleThesis(thesis){
            /* 处理毕业论文字段 */
            if (thesis == null){
                return `<span>未填写</span>`
            }

            if (thesis.review_option){
                return `<a href="#">查看</a>`
            }else{
                return `<a href="#">审阅</a>`
            }
        },

        reviewOrViewThesis(index){
            /* 审核或者查看毕业论文 */
            let thesisId = this.subjectList[index].thesis.id
            let subjectName = this.subjectList[index].subject_name
            thesisForm.showThesisForm(thesisId, subjectName)
        }
    },

    beforeMount() {
        this.getSubjectList(this.url)
    }
})


const taskBookForm = new Vue({
    el: '#taskBookForm',
    data: {
        subject: "",
        releaseTime: "",
        subjectDesc: "",
        purposeAndSignificance: "",
        contentAndTechnology: "",
        dataAndInformation: "",
        schedule: "",
        references: "",
        informationInEnglish: "",
        reviewer: "",
        reviewTime: "",
        reviewResult: "",

        subjectName: "",
        reviewerName: "",
        taskBookId: ""

    },
    methods: {
        showTaskBook(taskId){
            /* 展示课题任务书 */

            if (taskId == null){
                return
            }

            this.getTaskBookData(taskId)

            this.$refs.taskBook.classList.remove('hidden')

            return true
        },

        hiddenTaskBook(){
            /* 隐藏课题任务书 */
            this.$refs.taskBook.classList.add('hidden')

            return true
        },

        getTaskBookData(taskId){
            /* 获取任务书数据 */
            const url = `http://127.0.0.1:8000/api/subject/task_book/${taskId}/`
            axios.get(url)
                .then(res => {
                    const data = res.data.data
                    console.log(data)

                    this.taskBookId = data.id
                    this.subject = data.subject
                    this.releaseTime = data.release_time
                    this.subjectDesc = data.subject_desc
                    this.purposeAndSignificance = data.purpose_and_significance
                    this.contentAndTechnology = data.content_and_technology
                    this.dataAndInformation = data.data_and_information
                    this.schedule = data.schedule
                    this.references = data.references
                    this.informationInEnglish = data.information_in_English
                    this.reviewTime = data.review_time
                    this.reviewResult = data.review_result

                    this.subjectName = data.subject_info.name

                    if (data.reviewer != null){
                        this.reviewer = data.reviewer
                        this.reviewerName = data.reviewer_info.name
                    }

                    return true
                })
                .catch(error => {
                    console.log(error)
                    console.log(error.response)
                    alert("Error")

                    return false
                })
        },

        submitReviewData(){
            /* 提交任务书审核结果 */

            if (this.reviewResult == 1){
                alert("已经审核,不需要再次提交")
                return
            }

            const url = 'http://127.0.0.1:8000/api/subject/task_book/' + this.taskBookId + '/'
            const csrfToken = getCookie('csrftoken')
            const headers = {
                'X-CSRFToken': csrfToken
            }
            const data = {
                'review_result': parseInt(this.reviewResult)
            }

            axios.patch(url, data, {headers: headers})
                .then(res => {
                    const data = res.data.data

                    this.reivewerName = data.reviewer.name
                    this.reviewTime = data.reivew_time

                    alert('审核成功')
                    return
                })
                .catch(err => {
                    console.log(err)
                    console.log(err.response)
                    alert("Error")
                    return
                })
        }
    },

    filters: {
        handleReviewResult(val){
            if (val == 0){
                return "待审核"
            }else if(val == 1){
                return "合格"
            }else if(val == 2){
                return "不合格"
            }else{
                return ""
            }
        }
    }
})