

document.addEventListener('DOMContentLoaded', function () {

    const form = document.querySelector('.form-page form');

    if (form) {

        form.addEventListener('submit', function (event) {

            const saveButton = form.querySelector(
                'button[type="submit"], button:not([type])'
            );

            if (saveButton) {
                saveButton.disabled = true;
                saveButton.innerHTML = 'Saving...';
            }

        });

    }

    console.log('Form page ready');

});