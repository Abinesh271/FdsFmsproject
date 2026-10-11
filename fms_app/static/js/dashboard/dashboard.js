document.addEventListener("DOMContentLoaded", function () {

  

    const userForms = document.querySelectorAll(".user-form");

    userForms.forEach(function (form) {

        form.addEventListener("submit", function (event) {

            
            if (form.dataset.submitting === "true") {
                event.preventDefault();
                return;
            }

       
            if (!form.checkValidity()) {
                return;
            }

            const submitButton = form.querySelector(
                ".create-user-btn"
            );

            if (!submitButton) {
                return;
            }

            
            form.dataset.submitting = "true";
            submitButton.disabled = true;
            submitButton.textContent = "Creating User...";

        });

    });


   

    const evaluationRows = document.querySelectorAll(
        ".evaluation-table tbody tr"
    );

    evaluationRows.forEach(function (row) {

        
        if (row.querySelector("td[colspan]")) {
            return;
        }

        row.setAttribute("tabindex", "0");

    });

});