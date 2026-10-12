// Subject page JavaScript

document.addEventListener('DOMContentLoaded', function () {

    // Subject form
    const subjectForm = document.querySelector('.form-page form');

    if (subjectForm) {

        subjectForm.addEventListener('submit', function () {

            const saveButton = subjectForm.querySelector(
                'button[type="submit"], button:not([type])'
            );

            if (saveButton) {
                saveButton.disabled = true;
                saveButton.innerHTML = 'Saving...';
            }

        });

    }


    // Delete subject confirmation
    const deleteForms = document.querySelectorAll('.delete-form');

    deleteForms.forEach(function (form) {

        form.addEventListener('submit', function (event) {

            const confirmDelete = confirm(
                'Are you sure you want to delete this subject?'
            );

            if (!confirmDelete) {
                event.preventDefault();
            }

        });

    });


    console.log('Subject page ready');

});