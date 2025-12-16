
redirectIfAuthenticated();


const registerForm = document.getElementById('registerForm');
const roleSelect = document.getElementById('role');
const parentFields = document.getElementById('parentFields');
const teacherFields = document.getElementById('teacherFields');


roleSelect.addEventListener('change', (e) => {
    const role = e.target.value;

    if (role === 'parent') {
        parentFields.style.display = 'block';
        teacherFields.style.display = 'none';
    } else if (role === 'teacher') {
        parentFields.style.display = 'none';
        teacherFields.style.display = 'block';
    } else {
        parentFields.style.display = 'none';
        teacherFields.style.display = 'none';
    }
});


registerForm.addEventListener('submit', async (e) => {
    e.preventDefault();


    hideMessage('errorMessage');
    hideMessage('successMessage');


    const formData = {
        email: document.getElementById('email').value.trim(),
        password: document.getElementById('password').value,
        full_name: document.getElementById('full_name').value.trim(),
        phone: document.getElementById('phone').value.trim(),
        role: document.getElementById('role').value
    };


    if (!formData.email || !formData.password || !formData.full_name || !formData.role) {
        showError('errorMessage', 'Vui lòng nhập đầy đủ thông tin bắt buộc');
        return;
    }

    if (formData.password.length < 6) {
        showError('errorMessage', 'Mật khẩu phải có ít nhất 6 ký tự');
        return;
    }


    if (formData.role === 'parent') {
        formData.address = document.getElementById('address').value.trim();
        formData.relationship = document.getElementById('relationship').value;
    } else if (formData.role === 'teacher') {
        formData.employee_id = document.getElementById('employee_id').value.trim();
        formData.qualification = document.getElementById('qualification').value.trim();
    }


    const submitBtn = registerForm.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    submitBtn.disabled = true;
    submitBtn.textContent = 'Đang đăng ký...';

    try {

        const data = await register(formData);


        showSuccess('successMessage', 'Đăng ký thành công!  Đang chuyển tới trang đăng nhập.. .');


        registerForm.reset();
        parentFields.style.display = 'none';
        teacherFields.style.display = 'none';


        setTimeout(() => {
            redirectTo('/api/auth/login-page');
        }, 2000);

    } catch (error) {
        console.error('Register error:', error);


        let errorMsg = 'Đăng ký thất bại';

        if (error.status === 400) {
            errorMsg = error.message || 'Thông tin không hợp lệ';
        } else if (error.message) {
            errorMsg = error.message;
        }

        showError('errorMessage', errorMsg);


        submitBtn.disabled = false;
        submitBtn.textContent = originalText;
    }
});

console.log('📝 Register page loaded');