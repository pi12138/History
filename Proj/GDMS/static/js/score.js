/* 学生功能
    - 查询论文成绩
* */

let score = new Vue({
    el: '#score',
    data(){
        return {
            subjectName: "",
            score: ""
        }
    },
    methods: {
        getScore(thesisId){
            let url = '/api/design/thesis/score/' + '?theseId=' + thesisId

            axios.get(url)
                .then(res => {
                    this.score = res.data.data
                })
                .catch(err =>{
                    console.log(err)
                    console.log(err.response)
                })
        },

        showScore(subjectName, thesisId){
            /* 显示课题成绩 */
            this.subjectName = subjectName
            this.getScore(thesisId)

            this.$refs.score.classList.remove('hidden')
        },

        hiddenScore(){
            /* 隐藏课题成绩框 */
            this.$refs.score.classList.add('hidden')
        }
    }
})