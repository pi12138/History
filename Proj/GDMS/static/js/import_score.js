/*管理员功能:
    - 导入论文成绩
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


let importScore = new Vue({
    el: "#importScore",
    data() {
        return {
            file: ""
        }
    },

    methods: {
        getFile(event){
            this.file = event.target.files[0]
        },

        importScore(){
            let url = '/api/user/user_info/import_score/'
            let headers = getHeaders()
            let formData = new FormData()
            formData.append('file', this.file)
            formData.append('type', this.type)

            axios.post(url, formData, {'headers': headers})
                .then(res => {
                    console.log(res.data)
                    alert('导入成功')
                })
                .catch(err => {
                    handleError(err)
                })
        }
    }
})