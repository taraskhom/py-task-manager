document.addEventListener("DOMContentLoaded", function () {

    let sidebarLinks = document.querySelectorAll(".sidebar-link");
    sidebarLinks.forEach(link => {
        link.addEventListener("click", function () {
            sidebarLinks.forEach(l => l.classList.remove("active"));
            this.classList.add("active");
        });
    });

    let taskCards = document.querySelectorAll(".task-container");
    taskCards.forEach(card => {
        card.addEventListener("mouseenter", function () {
            this.style.boxShadow = "0 6px 12px rgba(0, 0, 0, 0.15)";
        });
        card.addEventListener("mouseleave", function () {
            this.style.boxShadow = "0 4px 8px rgba(0, 0, 0, 0.1)";
        });
    });
});
