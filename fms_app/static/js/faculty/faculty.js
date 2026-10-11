document.addEventListener("DOMContentLoaded", function () {

    // ---------- Confirm faculty deletion ----------

    const deleteForms = document.querySelectorAll(".delete-form");

    deleteForms.forEach(function (form) {

        form.addEventListener("submit", function (event) {

            const confirmed = window.confirm(
                "Are you sure you want to delete this faculty record?"
            );

            if (!confirmed) {
                event.preventDefault();
                return;
            }

            const deleteButton = form.querySelector(
                'button[type="submit"]'
            );

            if (deleteButton) {
                deleteButton.disabled = true;
                deleteButton.setAttribute(
                    "aria-label",
                    "Deleting faculty record"
                );
            }

        });

    });


    // ---------- Faculty add/edit form ----------

    const facultyForms = document.querySelectorAll(
        ".form-page form"
    );

    facultyForms.forEach(function (form) {

        form.addEventListener("submit", function (event) {

            // Allow Django/browser validation to run first.
            if (!form.checkValidity()) {
                return;
            }

            // Prevent repeated submissions.
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

            // Keep the original button label for reference.
            if (!submitButton.dataset.originalText) {
                submitButton.dataset.originalText =
                    submitButton.innerText.trim();
            }

            submitButton.innerText = "Saving...";

        });

    });


    // ---------- Search form feedback ----------

    const searchForm = document.querySelector(
        'form.card.card-body[method="get"]'
    );

    if (searchForm) {

        searchForm.addEventListener("submit", function () {

            const searchButton = searchForm.querySelector(
                'button[type="submit"]'
            );

            if (!searchButton) {
                return;
            }

            // Do not disable the button; allow normal GET navigation.
            searchButton.setAttribute("aria-busy", "true");

        });

    }

});