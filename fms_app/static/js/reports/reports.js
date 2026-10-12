// Reports page JavaScript

document.addEventListener('DOMContentLoaded', function () {

    // Check whether the reports page is loaded
    console.log('Reports page loaded successfully.');

    // Get the department summary table
    const departmentTable = document.querySelector('.table');

    if (departmentTable) {

        // Count the department rows
        const departmentRows = departmentTable.querySelectorAll('tbody tr');

        console.log('Department rows:', departmentRows.length);

    }

});