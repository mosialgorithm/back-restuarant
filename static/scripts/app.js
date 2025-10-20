
function login() {
    return {
        user: {
            mobile: null,
            password: null
        },
        userError: {
            mobile: null,
            mobile_message: null,
            password: null,
            password_message: null,
        },
        validateMobile() {
            if (this.user.mobile == null || this.user.mobile.trim() == '') {
                this.userError.mobile = true
                this.userError.mobile_message = 'لطفا شماره همراه خود را کامل و صحیح وارد نمایید'
                return false
            } else if (this.user.mobile.trim().length != 11) {
                this.userError.mobile = true
                this.userError.mobile_message = 'لطفا شماره همراه خود را کامل و صحیح وارد نمایید'
                return false
            } else if (this.user.mobile.trim()[0] != '0') {
                this.userError.mobile = true
                this.userError.mobile_message = 'شماره همراه باید با صفر شروع شود'
                return false
            }
            else {
                this.userError.mobile = false
                this.userError.mobile_message = ''
                return true
            }
        },
        validatePassword() {
            if (this.user.password == null || this.user.password.trim == '') {
                this.userError.password = true
                this.userError.password_message = 'گذرواژه شما باید بیشتر از ۸ کاراکتر باشد'
                return false
            } else if (this.user.password.trim().length <= 8) {
                this.userError.password = true
                this.userError.password_message = 'گذرواژه شما باید بیشتر از ۸ کاراکتر باشد'
                return false
            }
            else {
                this.userError.password = false
                this.userError.password_message = ''
                return true
            }
        },

        async checkMobile() {
            // await axios.post(`{{url_for('auth.check_mobile')}}`, {
            await axios.post('/auth/check-mobile', {
                mobile: this.user.mobile
            })
                .then((response) => {
                    console.log(response.data)
                    if (response.data.status == 'error') {
                        this.userError.mobile = true
                        this.userError.mobile_message = response.data.message
                        return false
                    } else if (response.data.status == 'success') {
                        this.userError.mobile = false
                        this.userError.mobile_message = null
                        return true
                    }
                })
                .catch((error) => console.log(error))
        },

        syncData(data) {
            Alpine.store('user').current_user = JSON.parse(data)
        },

        async loginForm() {
            this.validateMobile()
            this.validatePassword()
            await this.checkMobile()
            // await axios.post(`{{url_for('auth.login_view')}}`, {
            const response = await axios.post('/auth/login', {
                mobile: this.user.mobile,
                password: this.user.password
            })
            const result = response.data
            if (result.status == 'success') {
                // localStorage.setItem('current_user', JSON.stringify(result.data))
                // Alpine.store('user').user_current = this.current_user
                Alpine.store('user').init()

                Toast.fire({
                    icon: result.status,
                    title: result.message
                });
                setTimeout(() => {
                    // window.location.href = "{{url_for('admin.index_view')}}"
                    window.location.href = "/admin/"
                }, 3000);
            }

        }
    }
}

function login_by_sms(){
    return{
        status: false,
        disabled: true,

        toggle(){
            this.status = ! this.status
            console.log(this.status)
        },
        user:{
            mobile: null,
            code: null
        },
        userError: {
            mobile: null,
            mobile_message: null,
            code: null,
            code_message: null,
        },
        validateMobile() {
            if (this.user.mobile == null || this.user.mobile.trim() == '') {
                this.userError.mobile = true
                this.userError.mobile_message = 'لطفا شماره همراه خود را کامل و صحیح وارد نمایید'
                return false
            } 
            else if (this.user.mobile.trim().length != 11) {
                this.userError.mobile = true
                this.userError.mobile_message = 'لطفا شماره همراه خود را کامل و صحیح وارد نمایید'
                return false
            } 
            else if (this.user.mobile.trim()[0] != '0') {
                this.userError.mobile = true
                this.userError.mobile_message = 'شماره همراه باید با صفر شروع شود'
                return false
            }
            else {
                this.userError.mobile = false
                this.userError.mobile_message = ''
                this.disabled = false
                return true
            }
        },
        validateCode() {
            if (this.user.code == null || this.user.code.trim == '') {
                this.userError.code = true
                this.userError.code_message = 'کد ورودی باید دقیقا ۶ کاراکتر باشد'
                return false
            } else if (this.user.code.trim().length != 6) {
                this.userError.code = true
                this.userError.code_message = 'کد ورودی باید دقیقا ۶ کاراکتر باشد'
                return false
            }
            else {
                this.userError.code = false
                this.userError.code_message = ''
                this.disabled = true
                return true
            }
        },

        init(){
            // this.status = false
        },

        async sendSms(){
            console.log('code recieved : ', this.code_recieved)
            this.validateMobile()
            const response = await axios.post('/auth/send-sms', {
                mobile: this.user.mobile
            })
            const result = response.data
            console.log(result)
            if (result.status == 'success'){
                Toast.fire({
                    icon: result.status,
                    title: result.message
                });
                // setTimeout(() => {this.toggle()}, 200)
                this.status = true
                console.log('code status : ', this.status)
            } else{
                Toast.fire({
                    icon: result.status,
                    title: result.message
                });
                this.status = false
            }
        },
        
        async loginSms() {
            this.validateCode()
            const response = await axios.post('/auth/login-by-sms', {
                mobile: this.user.mobile,
                code: this.user.code
            })
            const result = response.data
            if (result.status == 'success') {
                // localStorage.setItem('current_user', JSON.stringify(result.data))
                // Alpine.store('user').user_current = this.current_user
                Alpine.store('user').init()

                Toast.fire({
                    icon: result.status,
                    title: result.message
                });
                setTimeout(() => {
                    // window.location.href = "{{url_for('admin.index_view')}}"
                    window.location.href = "/admin/"
                }, 3000);
            } else if(result.status == 'error_expire'){
                Toast.fire({
                    icon: 'error',
                    title: result.message
                });
                setTimeout(() => {
                    // window.location.href = "{{url_for('admin.index_view')}}"
                    window.location.href = "/auth/login-by-sms"
                }, 3000);
            }
            else{
                Toast.fire({
                    icon: result.status,
                    title: result.message
                });
                // setTimeout(() => {
                //     // window.location.href = "{{url_for('admin.index_view')}}"
                //     window.location.href = "/auth/login-by-sms"
                // }, 3000);
            }

        }
    }
}

function logout(){
    return{
        async logout(){
            console.log('logout btn is clicked !!')
            // const response = await axios.get(Flask.url_for('auth.logout_view'))
            const response = await axios.get('/auth/logout')
            if(response.data.status == 'success'){
                // localStorage.removeItem('current_user')
                Alpine.store('user').current_user = null
                setTimeout(() => {
                    // window.location.href = Flask.url_for('auth.login_view')
                    // location.href = Flask.url_for('index', {});
                    window.location.href = "/auth/login"
                }, 500);
            }
        }
    }
}


// .then((response) => {
//     console.log(response.data)
//     if (response.data.status == 'success') {
//         console.log(' response data : ', response.data.data, typeof (response.data.data))
//         // this.syncData(JSON.stringify(response.data.data))
//         // Alpine.store('user').current_user = JSON.stringify(response.data.data)
//         // Alpine.store('user').current_user = response.data.data
//         // Alpine.store('user').add_item(JSON.stringify(response.data.data)) 
//         Alpine.store('user').current_user = Object.values(response.data.data)
//         localStorage.setItem('current_user', JSON.stringify(response.data.data))
//         Toast.fire({
//             icon: response.data.status,
//             title: response.data.message
//         });
//         setTimeout(() => {
//             // window.location.href = "{{url_for('admin.index_view')}}"
//             window.location.href = "/admin/"
//         }, 3000);
//     }
// })
