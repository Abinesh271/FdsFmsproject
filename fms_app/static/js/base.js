document.addEventListener("DOMContentLoaded", function () {

    const sidebar = document.getElementById("sidebar");
    const menuButton = document.getElementById("menuButton");

    if (!sidebar) {
        return;
    }

   
    const overlay = document.createElement("div");
    overlay.className = "sidebar-overlay";
    document.body.appendChild(overlay);

   
    function openSidebar() {
        sidebar.classList.add("show");
        overlay.classList.add("show");
        document.body.style.overflow = "hidden";
    }

    function closeSidebar() {
        sidebar.classList.remove("show");
        overlay.classList.remove("show");
        document.body.style.overflow = "";
    }

    // mobile menu button
    if (menuButton) {
        menuButton.addEventListener("click", function () {
            if (sidebar.classList.contains("show")) {
                closeSidebar();
            } else {
                openSidebar();
            }
        });
    }

   
    overlay.addEventListener("click", closeSidebar);


    const menuLinks = sidebar.querySelectorAll(".side-nav a");

    menuLinks.forEach(function (link) {
        link.addEventListener("click", function () {
            if (window.innerWidth < 992) {
                closeSidebar();
            }
        });
    });

    // highlight current page
    const currentPage = window.location.pathname.replace(/\/+$/, "");

    menuLinks.forEach(function (link) {
        const linkPage = new URL(link.href).pathname.replace(/\/+$/, "");

        if (currentPage === linkPage) {
            link.classList.add("active");
        }
    });

   
    document.addEventListener("keydown", function (event) {
        if (event.key === "Escape") {
            closeSidebar();
        }
    });

  
    window.addEventListener("resize", function () {
        if (window.innerWidth >= 992) {
            closeSidebar();
        }
    });

    
    if (window.bootstrap) {
        const alerts = document.querySelectorAll(".alert-dismissible");

        alerts.forEach(function (alert) {
            setTimeout(function () {
                if (document.body.contains(alert)) {
                    bootstrap.Alert.getOrCreateInstance(alert).close();
                }
            }, 5000);
        });
    }

});

