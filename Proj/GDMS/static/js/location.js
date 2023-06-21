/*
* 学生功能：选择答辩地点
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


let locationForm = new Vue({
    el: '#location',
    data: {
        location: '',
        location_number: '',
        location_desc: '',
        locationList: "",
    },
    methods: {
        get_location_list(){
            let url = '/api/design/reply/'

            axios.get(url)
                .then(res => {
                    this.locationList = res.data
                    console.log(this.locationList)
                })
                .catch(err => {
                    handleError(err)
                })
        },

        selectLocation(){
            if (this.location_number != ""){
                alert("已选择答辩地点，不可再次选择！")
                return
            }

            let url = '/api/design/reply/'
            let headers = getHeaders()
            let data = {
                'location': this.location,
            }
            axios.post(url, data, {headers: headers})
                .then(res => {
                    console.log(res.data)
                    alert("选择答辩地点成功")
                    location.reload()
                })
                .catch(err => {
                    handleError(err)
                })
        },

        get_location(){
            let url = '/api/design/reply/location/'

            axios.get(url)
                .then(res => {
                    let data = res.data
                    console.log(data)

                    if (data.data == ''){
                        return
                    }else{
                        data = data.data

                        this.location = data.id
                        this.location_number = data.location_number
                        this.location_desc = data.location_desc
                    }
                })
                .catch(err => {
                    handleError(err)
                })
        },

        showLocationForm(){
            this.$refs.location.classList.remove('hidden')

            this.get_location()
            this.get_location_list()
        },

        hiddenLocationForm(){
            this.$refs.location.classList.add('hidden')
        }
    }
});