// 简单的JavaScript功能

// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    // 为提示消息添加自动关闭功能
    setTimeout(function() {
        const flashMessages = document.querySelectorAll('.flash-message');
        flashMessages.forEach(function(message) {
            message.style.transition = 'opacity 0.5s ease-out';
            message.style.opacity = '0';
            setTimeout(function() {
                message.remove();
            }, 500);
        });
    }, 3000);

    // 确认删除操作
    const deleteButtons = document.querySelectorAll('.btn-danger');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            if (!confirm('确定要删除吗？此操作不可撤销。')) {
                e.preventDefault();
            }
        });
    });

    // 表单验证
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            const formInputs = form.querySelectorAll('.form-input');
            let isValid = true;
            
            formInputs.forEach(function(input) {
                if (input.required && !input.value.trim()) {
                    isValid = false;
                    input.classList.add('is-invalid');
                    // 添加错误提示
                    if (!input.nextElementSibling || !input.nextElementSibling.classList.contains('invalid-feedback')) {
                        const errorMsg = document.createElement('div');
                        errorMsg.classList.add('invalid-feedback');
                        errorMsg.textContent = '此字段为必填项';
                        input.parentNode.insertBefore(errorMsg, input.nextSibling);
                    }
                } else {
                    input.classList.remove('is-invalid');
                    const errorElement = input.nextElementSibling;
                    if (errorElement && errorElement.classList.contains('invalid-feedback')) {
                        errorElement.remove();
                    }
                }
            });
            
            // 如果表单验证失败，阻止提交
            if (!isValid) {
                e.preventDefault();
            }
        });
    });

    // 监听输入框变化，实时移除错误提示
    const inputs = document.querySelectorAll('.form-input');
    inputs.forEach(function(input) {
        input.addEventListener('input', function() {
            if (this.classList.contains('is-invalid')) {
                this.classList.remove('is-invalid');
                const errorElement = this.nextElementSibling;
                if (errorElement && errorElement.classList.contains('invalid-feedback')) {
                    errorElement.remove();
                }
            }
        });
    });

    // 平滑滚动
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 80, // 减去头部高度
                    behavior: 'smooth'
                });
            }
        });
    });

    // 响应式菜单
    const menuToggle = document.querySelector('.menu-toggle');
    const nav = document.querySelector('.nav ul');
    
    if (menuToggle) {
        menuToggle.addEventListener('click', function() {
            nav.classList.toggle('active');
        });
    }

    // 主题切换功能
    const themeToggle = document.getElementById('theme-toggle');

    // 检查本地存储中的主题偏好
    const savedTheme = localStorage.getItem('theme');
    const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)');

    // 设置初始主题
    if (savedTheme === 'dark' || (!savedTheme && prefersDarkScheme.matches)) {
        document.body.classList.add('dark-theme');
        if (themeToggle) themeToggle.checked = true;
    } else {
        document.body.classList.remove('dark-theme');
        if (themeToggle) themeToggle.checked = false;
    }

    // 主题切换事件处理
    if (themeToggle) {
        themeToggle.addEventListener('change', function() {
            const isDark = this.checked;
            
            // 切换主题类
            if (isDark) {
                document.body.classList.add('dark-theme');
            } else {
                document.body.classList.remove('dark-theme');
            }
            
            // 保存主题偏好到本地存储
            localStorage.setItem('theme', isDark ? 'dark' : 'light');
            
            // 如果用户已登录，保存主题偏好到服务器
            if (window.isAuthenticated) {
                fetch('/api/update-theme', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ theme: isDark ? 'dark' : 'light' })
                })
                .then(response => response.json())
                .then(data => {
                    console.log('Theme updated on server:', data);
                })
                .catch(error => {
                    console.error('Error updating theme on server:', error);
                });
            }
        });
    }

    // 界面设置实时生效功能
    const blurEffectToggle = document.getElementById('blur-effect-toggle');
    const themePreferenceOptions = document.querySelectorAll('input[name="theme_preference"]');
    
    // 初始化界面设置
    if (blurEffectToggle) {
        // 检查本地存储中的毛玻璃效果设置
        const savedBlurEffect = localStorage.getItem('blurEffect');
        if (savedBlurEffect === 'false') {
            blurEffectToggle.checked = false;
            document.body.classList.add('no-blur-effect');
        } else {
            blurEffectToggle.checked = true;
            document.body.classList.remove('no-blur-effect');
        }
        
        // 毛玻璃效果切换事件
        blurEffectToggle.addEventListener('change', function() {
            if (this.checked) {
                document.body.classList.remove('no-blur-effect');
                localStorage.setItem('blurEffect', 'true');
            } else {
                document.body.classList.add('no-blur-effect');
                localStorage.setItem('blurEffect', 'false');
            }
            
            // 强制重新渲染所有毛玻璃元素以确保效果立即应用
            const blurElements = document.querySelectorAll('.header, .glass-container, .posts-container, .post-card');
            blurElements.forEach(el => {
                // 触发重排以确保样式立即更新
                const originalDisplay = el.style.display;
                el.style.display = 'none';
                setTimeout(() => {
                    el.style.display = originalDisplay;
                }, 0);
            });
            
            // 如果用户已登录，保存毛玻璃效果设置到服务器
            if (window.isAuthenticated) {
                fetch('/api/update-blur-effect', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ blur_effect: this.checked })
                })
                .then(response => response.json())
                .catch(error => {
                    console.error('Error updating blur effect on server:', error);
                });
            }
        });
    }
    
    // 主题偏好选择事件
    themePreferenceOptions.forEach(option => {
        option.addEventListener('change', function() {
            const themePreference = this.value;
            localStorage.setItem('themePreference', themePreference);
            
            // 根据主题偏好更新界面
            if (themePreference === 'system') {
                // 系统主题
                if (prefersDarkScheme.matches) {
                    document.body.classList.add('dark-theme');
                    if (themeToggle) themeToggle.checked = true;
                } else {
                    document.body.classList.remove('dark-theme');
                    if (themeToggle) themeToggle.checked = false;
                }
            } else if (themePreference === 'dark') {
                // 强制深色主题
                document.body.classList.add('dark-theme');
                if (themeToggle) themeToggle.checked = true;
            } else {
                // 强制浅色主题
                document.body.classList.remove('dark-theme');
                if (themeToggle) themeToggle.checked = false;
            }
            
            // 如果用户已登录，保存主题偏好设置到服务器
            if (window.isAuthenticated) {
                fetch('/api/update-theme-preference', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ theme_preference: themePreference })
                })
                .then(response => response.json())
                .catch(error => {
                    console.error('Error updating theme preference on server:', error);
                });
            }
        });
    });
});