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

        handleTaskBook(taskId){
            /* 处理任务书字段 */

            if (taskId == null){
                return `<a href="#">填写</a>`
            }else{
                return `<a href="#">查看</a>`
            }
        },

        writeOrViewTaskBook(index){
            /* 填写课题任务书或者查看课题任务书 */
            const taskId = this.subjectList[index].task_book
            const subjectName = this.subjectList[index].subject_name
            const subjectId = this.subjectList[index].id
            taskBookForm.showTaskBook(taskId, subjectName, subjectId)
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
        showTaskBook(taskId, subjectName, subjectId){
            /* 展示课题任务书 */

            if (taskId != null){
                this.getTaskBookData(taskId)
            }else{
                this.subjectName = subjectName
                this.subject = subjectId
            }

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

        submitTaskBookData(){
            /* 提交课题任务书 */

            if (this.taskBookId && this.reviewResult == 2){           // 如果this.taskBookId不为空，则为修改任务书，否则为新建任务书
                this.alterTaskBookData()
                return
            }

            if (this.taskBookId && this.reviewResult == 0){
                alert("当前不需要提交")
                return
            }

            const url = 'http://127.0.0.1:8000/api/subject/task_book/'
            const csrfToken = getCookie('csrftoken')
            const headers = {
                'X-CSRFToken': csrfToken
            }
            const data = {
                subject: this.subject,
                subject_desc: this.subjectDesc,
                purpose_and_significance: this.purposeAndSignificance,
                content_and_technology: this.contentAndTechnology,
                data_and_information: this.dataAndInformation,
                schedule: this.schedule,
                references: this.references,
                information_in_English: this.informationInEnglish,
            }

            axios.post(url, data, {headers: headers})
                .then(res => {
                    console.log(res.data)
                    alert("提交任务书成功")
                })
                .catch(err => {
                    console.log(err)
                    console.log(err.response)
                    alert("Error")
                    return false
                })
        },

        alterTaskBookData(){
            /* 修改任务书, 当审核结果为“不合格”, 即 review_result = 2  */
            const url = 'http://127.0.0.1:8000/api/subject/task_book/' + this.taskBookId + '/'
            const csrfToken = getCookie('csrftoken')
            const headers = {
                'X-CSRFToken': csrfToken
            }
            const data = {
                subject: this.subject,
                subject_desc: this.subjectDesc,
                purpose_and_significance: this.purposeAndSignificance,
                content_and_technology: this.contentAndTechnology,
                data_and_information: this.dataAndInformation,
                schedule: this.schedule,
                references: this.references,
                information_in_English: this.informationInEnglish,
            }

            axios.put(url, data, {headers: headers})
                .then(res => {
                    const data = res.data.data
                    console.log(res.data.data)

                    // 修改任务书审核状态，避免其未刷新页面导致再次修改
                    this.reviewResult = data.review_result
                    if (data.reviewer != null){
                        this.reviewer = data.reviewer
                        this.reviewerName = data.reviewer_info.name
                    }

                    alert("修改任务书成功")
                })
                .catch(err => {
                    console.log(err)
                    console.log(err.response)
                    alert("Error")
                    return false
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