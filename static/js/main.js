// Main JavaScript for 3D Printing Hub

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add fade-in animation to cards on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe all cards
    document.querySelectorAll('.print-card, .category-card').forEach(card => {
        observer.observe(card);
    });

    // Like button functionality
    document.querySelectorAll('.like-btn').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            if (!this.dataset.printId) return;
            
            const printId = this.dataset.printId;
            const heartIcon = this.querySelector('i');
            const likeCount = this.querySelector('.like-count');
            const originalText = this.innerHTML;
            
            // Add loading state
            this.classList.add('loading');
            this.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Loading...';
            
            // Get CSRF token
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
            if (!csrfToken) {
                console.error('CSRF token not found');
                this.classList.remove('loading');
                this.innerHTML = originalText;
                return;
            }
            
            fetch(`/prints/${printId}/like/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken.value,
                    'Content-Type': 'application/json',
                },
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                // Update UI based on response
                if (data.liked) {
                    heartIcon.classList.remove('far');
                    heartIcon.classList.add('fas');
                    this.classList.remove('btn-outline-danger');
                    this.classList.add('btn-danger');
                } else {
                    heartIcon.classList.remove('fas');
                    heartIcon.classList.add('far');
                    this.classList.remove('btn-danger');
                    this.classList.add('btn-outline-danger');
                }
                
                if (likeCount) {
                    likeCount.textContent = data.likes_count;
                }
                
                // Add success animation
                this.style.transform = 'scale(1.1)';
                setTimeout(() => {
                    this.style.transform = 'scale(1)';
                }, 200);
            })
            .catch(error => {
                console.error('Error:', error);
                // Show error message
                showNotification('Error liking print. Please try again.', 'error');
            })
            .finally(() => {
                this.classList.remove('loading');
            });
        });
    });

    // Search form enhancement
    const searchForm = document.querySelector('form[method="get"]');
    if (searchForm) {
        const searchInput = searchForm.querySelector('input[name="search"]');
        if (searchInput) {
            // Add search suggestions (placeholder for future implementation)
            searchInput.addEventListener('input', function() {
                // Debounce search suggestions
                clearTimeout(this.searchTimeout);
                this.searchTimeout = setTimeout(() => {
                    // Future: Implement search suggestions
                }, 300);
            });
        }
    }

    // Filter form auto-submit
    const filterForm = document.querySelector('form[method="get"]');
    if (filterForm) {
        const filterSelects = filterForm.querySelectorAll('select');
        filterSelects.forEach(select => {
            select.addEventListener('change', function() {
                // Auto-submit form when filters change
                filterForm.submit();
            });
        });
    }

    // Image lazy loading
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });

    images.forEach(img => imageObserver.observe(img));

    // Print detail page specific functionality
    if (document.querySelector('.print-detail-page')) {
        // Add print specifications tooltips
        document.querySelectorAll('.spec-item').forEach(item => {
            item.addEventListener('mouseenter', function() {
                this.style.transform = 'scale(1.02)';
            });
            
            item.addEventListener('mouseleave', function() {
                this.style.transform = 'scale(1)';
            });
        });
    }

    // Comment form enhancement
    const commentForm = document.querySelector('form[action*="comment"]');
    if (commentForm) {
        const textarea = commentForm.querySelector('textarea[name="content"]');
        if (textarea) {
            // Auto-resize textarea
            textarea.addEventListener('input', function() {
                this.style.height = 'auto';
                this.style.height = this.scrollHeight + 'px';
            });
            
            // Character counter
            const maxLength = 1000;
            const counter = document.createElement('small');
            counter.className = 'text-muted';
            counter.style.display = 'block';
            counter.style.textAlign = 'right';
            counter.style.marginTop = '5px';
            
            textarea.parentNode.appendChild(counter);
            
            function updateCounter() {
                const remaining = maxLength - textarea.value.length;
                counter.textContent = `${remaining} characters remaining`;
                counter.style.color = remaining < 100 ? '#dc3545' : '#6c757d';
            }
            
            textarea.addEventListener('input', updateCounter);
            updateCounter();
        }
    }

    // Mobile menu enhancement
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    if (navbarToggler && navbarCollapse) {
        // Close mobile menu when clicking on a link
        navbarCollapse.addEventListener('click', function(e) {
            if (e.target.classList.contains('nav-link')) {
                const bsCollapse = new bootstrap.Collapse(navbarCollapse, {
                    toggle: false
                });
                bsCollapse.hide();
            }
        });
    }

    // Back to top button
    const backToTopButton = document.createElement('button');
    backToTopButton.innerHTML = '<i class="fas fa-arrow-up"></i>';
    backToTopButton.className = 'btn btn-primary position-fixed';
    backToTopButton.style.cssText = `
        bottom: 20px;
        right: 20px;
        z-index: 1000;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        display: none;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    `;
    
    document.body.appendChild(backToTopButton);
    
    // Show/hide back to top button
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            backToTopButton.style.display = 'block';
        } else {
            backToTopButton.style.display = 'none';
        }
    });
    
    // Back to top functionality
    backToTopButton.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });

    // Notification system
    window.showNotification = function(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        notification.style.cssText = `
            top: 100px;
            right: 20px;
            z-index: 1050;
            min-width: 300px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        `;
        
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(notification);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
    };

    // Print statistics animation
    const statNumbers = document.querySelectorAll('.stat-item h3, .stat-item h6');
    statNumbers.forEach(stat => {
        const finalNumber = parseInt(stat.textContent.replace(/,/g, ''));
        if (!isNaN(finalNumber)) {
            animateNumber(stat, 0, finalNumber, 2000);
        }
    });

    function animateNumber(element, start, end, duration) {
        const startTime = performance.now();
        
        function updateNumber(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            const current = Math.floor(start + (end - start) * progress);
            element.textContent = current.toLocaleString();
            
            if (progress < 1) {
                requestAnimationFrame(updateNumber);
            }
        }
        
        requestAnimationFrame(updateNumber);
    }

    // Keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + K for search focus
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            const searchInput = document.querySelector('input[name="search"]');
            if (searchInput) {
                searchInput.focus();
            }
        }
        
        // Escape to close modals/alerts
        if (e.key === 'Escape') {
            const activeAlert = document.querySelector('.alert.show');
            if (activeAlert) {
                const closeBtn = activeAlert.querySelector('.btn-close');
                if (closeBtn) {
                    closeBtn.click();
                }
            }
        }
    });

    // Performance optimization: Debounce scroll events
    let scrollTimeout;
    window.addEventListener('scroll', function() {
        clearTimeout(scrollTimeout);
        scrollTimeout = setTimeout(function() {
            // Scroll-based functionality here
        }, 100);
    });

    console.log('3D Printing Hub initialized successfully!');
});
