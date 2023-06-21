/*
* 管理员功能： 添加系统用户
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


let facultyId = document.getElementById('facultyId').value


let addUser = new Vue({
    el: '#addUser',
    data: {
        type: 0,
        file: '',
    },
    methods: {
        addAdminUser(){
            adminUser.showUserForm()
            teacherUser.hiddenUserForm()
            studentUser.hiddenUserForm()
        },

        addStudentUser(){
            studentUser.showUserForm()
            teacherUser.hiddenUserForm()
            adminUser.hiddenUserForm()
        },

        addTeacherUser(){
            teacherUser.showUserForm()
            studentUser.hiddenUserForm()
            adminUser.hiddenUserForm()
        },

        importUser(){
            if (this.type == 0){
                alert('必须选择用户类型')
                return
            }

            let url = '/api/user/user_info/import_user/'
            let headers = getHeaders()
            let formData = new FormData()
            formData.append('file', this.file)
            formData.append('type', this.type)

            axios.post(url, formData, {'headers': headers})
                .then(res => {
                    console.log(res.data)
                })
                .catch(err => {
                    handleError(err)
                })

        },

        getFile(event){
            this.file = event.target.files[0]
        }

    }
});


let adminUser = new Vue({
    el: '#adminUser',
    data: {
        username: "",
        password: "",
        name: "",
        role: 'admin'

    },
    methods: {
        createUser(){
            if (this.username == "" || this.password == "" || this.name == ""){
                alert("请补全必要信息")
                return
            }

            let url = '/api/user/user_info/'
            let headers = getHeaders()

            axios.post(url, this.$data, {headers: headers})
                .then(res => {
                    console.log(res.data)
                    alert('新建管理员用户成功')
                })
                .catch(err => {
                    handleError(err)
                })
        },

        showUserForm(){
            this.$refs.adminUser.classList.remove('hidden')
        },

        hiddenUserForm(){
            this.$refs.adminUser.classList.add('hidden')
        }
    }
});


let teacherUser = new Vue({
    el: '#teacherUser',
    data: {
        username: "",
        password: "",
        name: "",
        gender: "",
        education: "",
        teacher_title: "",
        phone: "",
        qq: '',
        office: '',
        role: 'teacher',
        officeList: "",
    },
    methods: {
        createUser(){
            if (this.username == "" || this.password == "" || this.name == '' || this.gender == ''
                || this.education == '' || this.teacher_title == '' || this.phone == '' || this.qq == ''
                || this.office == ''){
                alert('请补全必要信息')
                return
            }

            let url = '/api/user/user_info/'
            let headers = getHeaders()
            let data = Object.assign({}, this.$data)
            delete data.officeList

            axios.post(url, data, {headers: headers})
                .then(res => {
                    console.log(res.data)
                    alert('创建教师用户成功')
                })
                .catch(err => {
                    handleError(err)
                })
        },

        showUserForm(){
            this.$refs.teacherUser.classList.remove('hidden')
        },

        hiddenUserForm(){
            this.$refs.teacherUser.classList.add('hidden')
        },

        get_office(){
            /* 获取教研室 */
            let url = '/organization/offices/?faculty=' + facultyId

            axios.get(url)
                .then(res => {
                    this.officeList = res.data
                })
                .catch(err => {
                    handleError(err)
                })
        }
    },

    beforeMount(){
        this.get_office()
    }
});


let studentUser = new Vue({
    el: '#studentUser',
    data: {
        username: '',
        password: '',
        name: '',
        gender: '',
        klass: '',
        direction: '',
        profession: '',
        phone: '',
        qq: '',
        role: 'student',

        professionList: "",
        directionList: "",
        klassList: "",

    },
    methods: {
        createUser(){
            let url = '/api/user/user_info/'
            let headers = getHeaders()
            let data = Object.assign({}, this.$data)
            delete data.professionList
            delete data.directionList
            delete data.klassList

            axios.post(url, data, {headers: headers})
                .then(res => {
                    console.log(res.data)
                    alert('新建学生用户成功')
                })
                .catch(err => {
                    handleError(err)
                })
        },

        showUserForm(){
            this.$refs.studentUser.classList.remove('hidden')
        },

        hiddenUserForm(){
            this.$refs.studentUser.classList.add('hidden')
        },

        get_profession(){
            let url = '/organization/professions/?faculty_id=' + facultyId

            axios.get(url)
                .then(res => {
                    this.professionList = res.data
                })
                .catch(err => {
                    handleError(err)
                })
        },

        get_direction(){
            if (this.profession == ""){
                return
            }

            let url = '/organization/directions/?profession_id=' + this.profession

            axios.get(url)
                .then(res => {
                    this.directionList = res.data
                })
                .catch(err => {
                    handle(err)
                })
        },

        get_klass(){
            if (this.direction == ''){
                return
            }

            let url = '/organization/klasses/?direction_id=' + this.direction

            axios.get(url)
                .then(res => {
                    this.klassList = res.data
                })
                .catch(err => {
                    handleError(err)
                })
        }
    },

    beforeMount(){
        this.get_profession()
    }
});