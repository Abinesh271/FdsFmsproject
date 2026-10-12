// Performance page JavaScript

document.addEventListener('DOMContentLoaded', function () {

    // Evaluation form
    const evaluationForm = document.querySelector('.form-page form');

    if (evaluationForm) {

        evaluationForm.addEventListener('submit', function () {

            const saveButton = evaluationForm.querySelector(
                'button[type="submit"], button:not([type])'
            );

            if (saveButton) {
                saveButton.disabled = true;
                saveButton.innerHTML = 'Saving...';
            }

        });

    }


    // Delete evaluation confirmation
    const deleteForms = document.querySelectorAll('.delete-form');

    deleteForms.forEach(function (form) {

        form.addEventListener('submit', function (event) {

            const confirmDelete = confirm(
                'Are you sure you want to delete this evaluation?'
            );

            if (!confirmDelete) {
                event.preventDefault();
            }

        });

    });


    console.log('Performance page ready');

});