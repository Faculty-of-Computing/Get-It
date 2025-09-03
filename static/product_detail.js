// Toastify JS CDN
// <script src="https://cdn.jsdelivr.net/npm/toastify-js"></script>
// Drift.js CDN
// <script src="https://cdn.jsdelivr.net/npm/drift-zoom/dist/Drift.min.js"></script>
// Add custom product detail JS below

document.addEventListener('DOMContentLoaded', function() {
    // --- Product Image Gallery ---
    const mainImg = document.getElementById('main-product-img');
    const thumbnails = document.querySelectorAll('.product-thumbnail');
    thumbnails.forEach(function(thumb) {
        thumb.addEventListener('click', function() {
            mainImg.src = this.src;
        });
    });

    // --- Tabs ---
    const tabLinks = document.querySelectorAll('.tab-link');
    const tabContents = document.querySelectorAll('.tab-content');
    tabLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            tabLinks.forEach(l => l.classList.remove('active'));
            tabContents.forEach(c => c.classList.remove('active'));
            this.classList.add('active');
            document.getElementById(this.dataset.tab).classList.add('active');
        });
    });

    // --- Toast Example ---
    window.showToast = function(msg) {
        Toastify({
            text: msg,
            duration: 2500,
            gravity: "top",
            position: "right",
            backgroundColor: "#3498db",
            stopOnFocus: true
        }).showToast();
    };

    // --- Micro-animations ---
    document.querySelectorAll('.btn-animate').forEach(btn => {
        btn.addEventListener('mouseenter', () => btn.classList.add('hovered'));
        btn.addEventListener('mouseleave', () => btn.classList.remove('hovered'));
    });
});
