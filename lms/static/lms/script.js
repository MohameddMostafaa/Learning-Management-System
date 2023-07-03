document.addEventListener('DOMContentLoaded', function() {
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const dropdownToggle = document.getElementById('dropdown-toggle');
    const sidebar = document.getElementById('sidebar');
    const dropdownMenu = document.querySelector('.dropdown-menu');

    // Add event listeners to the toggle buttons
    sidebarToggle.addEventListener('click', function(event) {
        event.stopPropagation();
        sidebar.classList.toggle('show');
    });

    dropdownToggle.addEventListener('click', function() {
        if(dropdownMenu.classList.contains('show')) {
            dropdownMenu.classList.remove('show');
            dropdownMenu.classList.add('hide');
        } else {
            dropdownMenu.classList.add('show');
            dropdownMenu.classList.remove('hide');
        }
    });

    document.addEventListener('click', function(event) {
        // Check if the clicked element is inside the sidebar
        if (!event.target.closest('#sidebar') && sidebar.classList.contains('show')) {
            sidebar.classList.remove('show');
        }
    });
});