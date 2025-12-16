
redirectIfAuthenticated();


const loginForm = document.getElementById('loginForm');


loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();


    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('password').value;


    if (!email || !password) {
        showError('errorMessage', 'Vui lòng nhập đầy đủ thông tin');
        return;
    }


    const submitBtn = loginForm.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    submitBtn.disabled = true;
    submitBtn.textContent = 'Đang đăng nhập...';

    try {

        const data = await login(email, password);

        console.log('✅ Login successful:', data);


        showSuccess('errorMessage', 'Đăng nhập thành công!  Đang chuyển trang...');


        setTimeout(() => {
            redirectTo('/api/auth/dashboard-page');
        }, 1000);

    } catch (error) {
        console.error('❌ Login error:', error);


        let errorMsg = 'Đăng nhập thất bại';

        if (error.status === 401) {
            errorMsg = 'Email hoặc mật khẩu không đúng';
        } else if (error.message) {
            errorMsg = error.message;
        }

        showError('errorMessage', errorMsg);


        submitBtn.disabled = false;
        submitBtn.textContent = originalText;
    }
});

console.log('📝 Login page loaded');