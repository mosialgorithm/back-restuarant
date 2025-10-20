document.addEventListener('alpine:init', () => {
    Alpine.data('register', () => ({
        open: false,

        registerForm() {
            console.log('btn is clicked !!');
        }
    }))
})