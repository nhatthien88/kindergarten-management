
if (!requireAuth()) {
    throw new Error('Authentication required');
}


async function loadUserData() {
    try {

        let user = getUserData();


        if (!user) {
            user = await getCurrentUser();
        }

        displayUserInfo(user);

    } catch (error) {
        console.error('Error loading user data:', error);


        if (error.status === 401) {
            clearTokens();
            redirectTo('/api/auth/login-page');
        } else {
            showError('errorMessage', 'Không thể tải thông tin người dùng');
        }
    }
}


function displayUserInfo(user) {

    document.getElementById('userName').textContent = user.full_name || user.email;


    document.getElementById('userEmail').textContent = user.email || 'N/A';
    document.getElementById('userRole').textContent = formatRole(user.role) || 'N/A';
    document.getElementById('userPhone').textContent = user.phone || 'Chưa cập nhật';

    const statusElement = document.getElementById('userStatus');
    if (user.is_active) {
        statusElement.textContent = '✅ Đang hoạt động';
        statusElement.style.color = '#4caf50';
    } else {
        statusElement.textContent = '❌ Không hoạt động';
        statusElement.style.color = '#f44336';
    }
}


const logoutBtn = document.getElementById('logoutBtn');

logoutBtn.addEventListener('click', async () => {
    const confirmLogout = confirm('Bạn có chắc muốn đăng xuất? ');

    if (!confirmLogout) return;


    logoutBtn.disabled = true;
    logoutBtn.textContent = 'Đang đăng xuất...';

    try {

        await logout();


        redirectTo('/api/auth/login-page');

    } catch (error) {
        console.error('Logout error:', error);


        clearTokens();
        redirectTo('/api/auth/login-page');
    }
});


document.addEventListener('DOMContentLoaded', () => {
    loadUserData();
});

console.log('📊 Dashboard page loaded');
console.log('👤 Current user:', getUserData());