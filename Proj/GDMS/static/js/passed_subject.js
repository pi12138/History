/* 管理员功能： 查看已通过课题 */

var passedList = new Vue({
    el: "#passedList",
    data: {
        passedList: [],
        count: "",
        nextUrl: "",
        previousUrl: "",
        page: "",
        numPages: ""
    },
    methods: {
        getPassedList(url){
            axios.get(url)
                .then(res => {
                    console.log(res)
                    const data = res.data
                    this.passedList = data.results
                    this.count = data.count
                    this.nextUrl = data.next_url
                    this.previousUrl = data.previous_url
                    this.page = data.page
                    this.numPages = data.num_pages
                    this.setBtnDisable()
                })
        },

        setBtnDisable(){
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
            const subject = this.passedList[index]
            markForm.setFormShow(subject)
        },
    },
    beforeMount(){
        const url = 'http://127.0.0.1:8000/api/subject/passed_subject/'
        this.getPassedList(url)
    }
})


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

        closeForm(){
            this.$refs.markForm.classList.add('hidden')
        }

    },

})