const teacherInfo = new Vue({
    el: '#teacherInfo',
    data: {
        formData: "",
        officeList: "",
    },
    methods: {
        getFormData(){
            const url = 'http://127.0.0.1:8000/api/user/teacher_settings/'

            axios.get(url)
                .then(res => {
                    console.log(res)
                    this.formData = res.data

                    this.getOfficeList(res.data.faculty)
                })
                .catch(error => {
                    console.log(error)
                    console.log(error.response)
                    alert("Error")
                })
        },

        getOfficeList(faculty){
            const url = 'http://127.0.0.1:8000/organization/offices/?faculty=' + faculty

            axios.get(url)
                .then(res => {
                    console.log(res)
                    this.officeList = res.data
                })
                .catch(error => {
                    console.log(error)
                    console.log(error.response)
                    alert("Error")
                })
        },

        submitFormData(){
            const url = 'http://127.0.0.1:8000/api/user/teacher_settings/' + this.formData.id + '/'
            const csrfToken = getCookie('csrftoken')
            const headers = {
                headers: {
                    'X-CSRFToken': csrfToken
                }
            }
            axios.put(url, this.formData, headers)
                .then(res => {
                    this.formData = res.data

                    this.getOfficeList(res.data.faculty)

                    alert("提交成功")
                })
                .catch(error => {
                    console.log(error)
                    console.log(error.response)
                    alert("Error")
                })
        }
    },

    beforeMount(){
        this.getFormData()
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


var app = new Vue({
            el: "#app",
            data: {
                is_show: false,
                oldPassword: "",
                newPassword1: "",
                newPassword2: ""
            },
            methods: {

                canelChange(){
                    /* 取消修改密码 */
                    this.oldPassword = ""
                    this.newPassword1 = ""
                    this.newPassword2 = ""
                    this.is_show = false
                },
                changePassword(){
                    if (!this.oldPassword){
                        alert("请填写原密码")
                        return
                    }

                    if (!this.newPassword1){
                        alert("请填写新密码")
                        return
                    }

                    if (this.newPassword1 !== this.newPassword2){
                        alert("新密码不一样")
                        return
                    }

                    if (this.newPassword1 === this.oldPassword){
                        alert("新旧密码一样")
                        return
                    }

                    var url = "http://127.0.0.1:8000/user/change_password/"
                    var params = {
                        old_password: this.oldPassword,
                        new_password1: this.newPassword1,
                        new_password2: this.newPassword2,
                    }

                    axios.post(url, params)
                    .then(function(res){
                        alert(res.data + "请重新登录")
                        window.location.href = "/"
                    })
                    .catch(function(error){
                        alert(error.response.data)
                    })
                }

            },

        })