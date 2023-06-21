/* 教师功能: 审核学生选题申请 */

var applySubjectList = new Vue({
    el: "#applySubjectList",
    data: {
        url: "http://127.0.0.1:8000/api/subject/approval_application/",
        applyList: "",
        nextUrl: "",
        previousUrl: "",
        count: "",
        numPages: "",
        page: ""
    },
    methods: {
        getApplyList(url){
            /* 获取申请列表 */

            axios.get(url)
                .then(res => {
                    const data = res.data
                    console.log(data)

                    this.applyList = data.results

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

        handleApplyResult(value){
            /* 处理value值的三种情况 */
            if (value == 0){
                return "待审核"
            }else if(value == 1){
                return "申请通过"
            }else if(value == 2){
                return "申请未通过"
            }else{
                return ""
            }
        },

        approvalApplication(applyId, status){
            /* 提交申请 同意/拒绝 */
            const url = 'http://127.0.0.1:8000/api/subject/approval_application/' + applyId + '/'
            const csrfToken = getCookie('csrftoken')
            const headers = {
                'X-CSRFToken': csrfToken
            }
            const data = {}

            if (status == true){
                data['apply_result'] = 1
            }else if(status == false){
                data['apply_result'] = 2
            }else{
                alert("非法参数")
                return
            }

            axios.patch(url, data, {headers: headers})
                .then(res => {
                    console.log(res)
                    location.reload()
                })
                .catch(error => {
                    console.log(error)
                    console.log(error.response)
                    alert("Error")
                })

        }
    },

    beforeMount(){
        this.getApplyList(this.url)
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