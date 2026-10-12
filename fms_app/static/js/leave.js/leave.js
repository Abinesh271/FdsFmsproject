// leave page javaScript

document.addEventListener('DOMContentLoaded', function () {

    // Apply leave form
    const leaveForm = document.querySelector('.leave-form');

    if (leaveForm) {
        leaveForm.addEventListener('submit', function () {

            const submitButton = leaveForm.querySelector(
                '.submit-leave-btn'
            );

            if (submitButton) {
                submitButton.disabled = true;
                submitButton.innerHTML = 'Submitting...';
            }

        });
    }


    // Approve leave confirmation
    const approveButtons = document.querySelectorAll('.approve-btn');

    approveButtons.forEach(function (button) {

        button.addEventListener('click', function (event) {

            const confirmAction = confirm(
                'Are you sure you want to approve this leave?'
            );

            if (!confirmAction) {
                event.preventDefault();
            }

        });

    });


    // Reject leave confirmation
    const rejectButtons = document.querySelectorAll('.reject-btn');

    rejectButtons.forEach(function (button) {

        button.addEventListener('click', function (event) {

            const confirmAction = confirm(
                'Are you sure you want to reject this leave?'
            );

            if (!confirmAction) {
                event.preventDefault();
            }

        });

    });


    console.log('Leave page ready');

});