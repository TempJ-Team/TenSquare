/*
 * @Descripition: 
 * @Version: 
 * @Author: SmartFox97
 * @Date: 2020-10-12 16:13:37
 * @LastEditors: SmartFox97
 * @LastEditTime: 2020-10-15 11:59:41
 */
var vm = new Vue({
    el: "#app",
    data: {
        token: sessionStorage.token || localStorage.token
    },
    mounted() {
    },
    methods: {
        publish_spit() {
            var content = CKEDITOR.instances.editor2.getData()
            if (content == '') {
                this.$message({
                    message: '内容不允许为空',
                    type: 'error'
                })
                return;
            }
            var url = host + 'spit/'
            axios.post(url, {
                content: content
            }, {
                    headers: {
                        'Authorization': 'JWT ' + this.token
                    }
                }).then(response => {
                    this.$message({
                        message: '吐槽成功~',
                        type: 'success'
                    })
                    setTimeout(function () {
                        location.href = '/spit-index.html'
                    }, 1000);
                }).catch(error => {
                    this.$message({
                        message: "吐槽失败",
                        type: 'error'
                    })
                });
        }
    },
});