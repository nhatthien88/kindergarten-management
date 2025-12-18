// Admin Dashboard JavaScript

// Tab functionality
function initTabs() {
    const tabs = document.querySelectorAll('.tab');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const targetId = tab.getAttribute('data-target');
            
            // Remove active class from all tabs and contents
            tabs.forEach(t => t.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));
            
            // Add active class to clicked tab and its content
            tab.classList.add('active');
            document.getElementById(targetId).classList.add('active');
        });
    });
}

// Confirm dialog for destructive actions
function confirmAction(message) {
    return confirm(message || 'Bạn có chắc chắn muốn thực hiện hành động này?');
}

// Show loading state on button
function showLoading(button) {
    button.disabled = true;
    const originalText = button.innerHTML;
    button.setAttribute('data-original-text', originalText);
    button.innerHTML = '<span class="loading"></span> Đang xử lý...';
}

function hideLoading(button) {
    button.disabled = false;
    const originalText = button.getAttribute('data-original-text');
    if (originalText) {
        button.innerHTML = originalText;
    }
}

// AJAX approve teacher
async function approveTeacher(userId, button) {
    if (!confirmAction('Bạn có chắc muốn duyệt giáo viên này?')) {
        return;
    }
    
    showLoading(button);
    
    try {
        const response = await fetch(`/api/admin/users/${userId}/approve`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        if (response.ok) {
            alert('Duyệt giáo viên thành công!');
            location.reload();
        } else {
            alert('Lỗi: ' + (data.message || 'Không thể duyệt giáo viên'));
            hideLoading(button);
        }
    } catch (error) {
        alert('Lỗi kết nối: ' + error.message);
        hideLoading(button);
    }
}

// AJAX toggle user status
async function toggleUserStatus(userId, button) {
    const currentStatus = button.getAttribute('data-status');
    const action = currentStatus === 'true' ? 'vô hiệu hóa' : 'kích hoạt';
    
    if (!confirmAction(`Bạn có chắc muốn ${action} tài khoản này?`)) {
        return;
    }
    
    showLoading(button);
    
    try {
        const response = await fetch(`/api/admin/users/${userId}/toggle`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const data = await response.json();
        
        if (response.ok) {
            alert(`${action.charAt(0).toUpperCase() + action.slice(1)} tài khoản thành công!`);
            location.reload();
        } else {
            alert('Lỗi: ' + (data.message || 'Không thể thay đổi trạng thái'));
            hideLoading(button);
        }
    } catch (error) {
        alert('Lỗi kết nối: ' + error.message);
        hideLoading(button);
    }
}

// Delete confirmation with form submit
function confirmDelete(formId, message) {
    if (confirmAction(message || 'Bạn có chắc muốn xóa?')) {
        document.getElementById(formId).submit();
    }
}

// Format currency VND
function formatCurrency(amount) {
    return new Intl.NumberFormat('vi-VN', {
        style: 'currency',
        currency: 'VND'
    }).format(amount);
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initTabs();
    
    // Highlight active menu item
    const currentPath = window.location.pathname;
    const menuLinks = document.querySelectorAll('.sidebar-menu a');
    menuLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
});
