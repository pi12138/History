/* 任务书js代码 */

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