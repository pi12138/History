/* 教师功能： 申报课题  */

var app = new Vue({
    el:"#app",
    data:{
        subjectName: "",
        teacher: "",
        office: "",
        number: "",
        student: "",
        subjectDesc:"",
        expectGoal: "",
        require: "",
        requiredConditions: "",
        references:""
    },
    methods:{
        showTable(){
            var div = document.getElementById('hidden_subject_table')
            var btn = document.getElementById('hidden_btn')
            div.classList.remove('hidden')
            btn.classList.remove('hidden')
        },

        hiddenTable(){
            var div = document.getElementById('hidden_subject_table')
            var btn = document.getElementById('hidden_btn')
            div.classList.add('hidden')
            btn.classList.add('hidden')
        },

        declareSubject(){
            var msg = this.verifyData()
            if (msg != true){
                alert(msg)
                return
            }

            var url = "http://127.0.0.1:8000/subject/declare_subject/"
            axios.post(url, this.$data)
                .then(function (res) {
                    alert(res.data)
                    // window.location.href = '/subject/declare_subject/'
                    location.reload()
                })
                .catch(function (error) {
                    // console.log(error.response)
                    alert(error.response.data)
                })
        },

        getData(){
            this.teacher = document.getElementsByName('teacher-id')[0].value
            this.office = document.getElementsByName('office-id')[0].value
        },

        verifyData(){
            if (this.subjectName === ""){
                return "课题名为空"
            }

            if (this.number === ""){
                return "课题人数为空"
            }

            if (this.subjectDesc === ""){
                return "课题描述为空"
            }

            if (this.expectGoal === ""){
                return "预期目标为空"
            }

            if (this.require === ""){
                return "对学生知识能力要求为空"
            }

            if (this.requiredConditions === ""){
                return "所需条件为空"
            }

            if (this.references === ""){
                return "参考资料为空"
            }

            return true
        }
    },
    beforeMount(){
        this.getData()
    }
})


var subjectList = new Vue({
    el: "#subject_list",
    data: {},
    methods: {
        showSubjectInfo(subjectId){
            /* 获取指定课题的数据 */
            // console.log(subjectId)
            var url = "http://127.0.0.1:8000/subject/alter_subject/" + "?subject_id=" + subjectId

            axios.get(url)
                .then(function (res) {
                    if (res.status !== 200){
                        console.log(res)
                        return
                    }

                    var data = res.data
                    mark_form.setMarkFormData(data)
                    mark_form.setMarkFormShow()

                })
                .catch(function (error) {
                    console.log(error)
                    console.log(error.response)
                    alert(error.response.data.msg)
                })
        },
    }
})


var mark_form = new Vue({
    el: "#mark_form",
    data: {
        subjectName: "",
        teacher: "",
        office: "",
        number: "",
        student: "",
        subjectDesc:"",
        expectGoal: "",
        require: "",
        requiredConditions: "",
        references:"",
        review_result: "",
        review_reason: "",
        review_result_number: "",

        teacher_id: "",
        student_id: "",
        subject_id: ""
    },
    methods: {
        setMarkFormData(data){
            /* 给mark_form 的data实例赋值 */
            this.subjectName = data.subject_name
            this.teacher = data.teacher_name
            this.office = data.office_name
            this.number = data.number_of_people
            this.student = data.student_name
            this.subjectDesc = data.subject_description
            this.expectGoal = data.expected_goal
            this.require = data.require
            this.requiredConditions = data.required_conditions
            this.references = data.references
            this.review_result = data.review_result
            this.review_reason = data.review_reason
            this.review_result_number = data.review_result_number

            this.teacher_id = data.questioner
            this.student_id = data.select_student
            this.subject_id = data.id

            this.setHiddenDiv()
        },

        setMarkFormShow(){
            /* 显示mark_form 实例 */
            this.$refs.mark_form.classList.remove('hidden')

            if (this.review_result === "审核通过"){
                this.$refs.submitBtn.classList.add('disabled')
            }
        },

        setMarkFormHidden(){
            /* 隐藏mark_form实例 */
            this.$refs.mark_form.classList.add('hidden')
            location.reload()

            return
        },

        alterSubject(){
            /* 提交修改课题表单 */
            var url = "http://127.0.0.1:8000/subject/alter_subject/"
            var data = {
                subject_name: this.subjectName,
                number_of_people: this.number,
                subject_description: this.subjectDesc,
                expected_goal: this.expectGoal,
                require: this.require,
                required_conditions: this.requiredConditions,
                references: this.references,
                subject_id: this.subject_id,
                review_result_number: this.review_result_number
            }
            axios.post(url, data)
                .then(function (res) {
                    if (res.status !== 200){
                        console.log(res)
                    }
                    const data = res.data.data
                    mark_form.subjectName = data.subject_name
                    mark_form.number = data.number_of_people
                    mark_form.subjectDesc = data.subject_description
                    mark_form.expectGoal = data.expected_goal
                    mark_form.require = data.require
                    mark_form.requiredConditions = data.required_conditions
                    mark_form.references = data.references

                    alert("修改成功")
                })
                .catch(function (error) {
                    console.log(error)
                    console.log(error.response)
                    alert('修改失败，发生错误')
                })
        },

        setHiddenDiv(){
            /* 设置 未通过原因 div 是否需要隐藏 */
            if (this.review_result_number === 2){
                this.$refs.hidden_div.classList.remove('hidden')

                return
            }

            return
        }
    }
})