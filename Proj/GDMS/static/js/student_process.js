/*  学生模块： 毕业设计管理  */

const process = new Vue({
    el: "#process",
    data: {
        'subject': "",
        'taskBook': "",
        'report': "",
        'subjectName': "",
        design: "",
        thesisId: ""
    },
    methods: {
        viewTaskBook(){
            if (this.taskBook){
                taskBookForm.showTaskBook(this.taskBook)
            }else{
                alert("不存在任务书")
            }
        },

        viewOrWriteReport(){
            reportForm.showReportForm(this.report, this.subjectName)
        },

        viewOrWriteDesign(){
            designForm.showDesignForm(this.design, this.subjectName)
        },

        viewOrWriteThesis(){
            thesisForm.showThesisForm(this.thesisId, this.subjectName)
        },

        viewOrSelectLocation(){
            /* 查看或选择答辩地点 */
            locationForm.showLocationForm()
        },

        viewScore(){
            /* 查看答辩成绩 */
            score.showScore(this.subjectName, this.thesisId)
        },

        getInfo(){
            /* 获取学生的课题ID、任务书ID、开题报告等... */

            const url = 'http://127.0.0.1:8000/api/user/student_info/related_info/'

            axios.get(url)
                .then(res => {
                    console.log(res)
                    const data = res.data

                    this.subject = data.subject_id
                    this.taskBook = data.task_book_id
                    this.report = data.report_id
                    this.subjectName = data.subject_name
                    this.design = data.design_id
                    this.thesisId = data.thesis_id
                })
                .catch(err => {
                    handleError(err)
                })
        },
    },

    beforeMount(){
        this.getInfo()
    }
})

function handleError(error){
    console.log(error)
    console.log(error.response)
    alert("Error")
}

