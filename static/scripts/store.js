
document.addEventListener('alpine:init', () => {
    Alpine.store('user', {
        // current_user: JSON.parse(localStorage.getItem('current_user')),
        current_user: null,

        async fetchData(){
            const result = await axios.get('/auth/whoami')
            this.current_user = result.data.data
        },
        
        init(){
            this.fetchData()
            // console.log('store user : ', result.data)
        },
    })
});
