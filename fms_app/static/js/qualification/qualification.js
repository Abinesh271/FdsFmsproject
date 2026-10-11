document.addEventListener("DOMContentLoaded", function () {

    // ---------- Confirm qualification deletion ----------

    const deleteForms = document.querySelectorAll(".delete-form");

    deleteForms.forEach(function (form) {

        form.addEventListener("submit", function (event) {

            // Avoid showing the confirmation more than once.
            if (form.dataset.submitting === "true") {
                event.preventDefault();
                return;
            }

            const confirmed = window.confirm(
                "Are you sure you want to delete this qualification?"
            );

            if (!confirmed) {
                event.preventDefault();
                return;
            }

            const deleteButton = form.querySelector(
                'button[type="submit"]'
            );

            form.dataset.submitting = "true";

            if (deleteButton) {
                deleteButton.disabled = true;
                deleteButton.setAttribute("aria-busy", "true");
            }

        });

    });


    // ---------- Qualification form submission ----------

    const forms = document.querySelectorAll(
        ".form-page form[method='post']"
    );

    forms.forEach(function (form) {

        form.addEventListener("submit", function (event) {

            // Allow browser validation to work normally.
            if (!form.checkValidity()) {
                return;
            }

            // Prevent duplicate submissions.
            if (form.dataset.submitting === "true") {
                event.preventDefault();
                return;
            }

            const submitButton = form.querySelector(
                'button[type="submit"]'
            );

            if (!submitButton) {
                return;
            }

            form.dataset.submitting = "true";
            submitButton.disabled = true;
            submitButton.setAttribute("aria-busy", "true");
            submitButton.innerHTML =
                '<i class="bi bi-hourglass-split"></i> Saving...';

        });

    });

});