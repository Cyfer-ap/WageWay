document.addEventListener("DOMContentLoaded", function () {
    const categorySelect = document.getElementById("id_category");
    const customCategoryWrapper = document.getElementById("customCategoryWrapper");

    const jobTypeRadios = document.querySelectorAll("input[name='job_type']");
    const oneTimeFields = document.getElementById("oneTimeFields");
    const recurringFields = document.getElementById("recurringFields");

    // Show/hide custom category input
    function toggleCustomCategory() {
        if (categorySelect.value === "Other") {
            customCategoryWrapper.style.display = "block";
        } else {
            customCategoryWrapper.style.display = "none";
        }
    }

    // Show/hide date/day fields based on job type
    function toggleJobFields() {
        const selected = document.querySelector("input[name='job_type']:checked");
        if (!selected) return;

        if (selected.value === "one_time") {
            oneTimeFields.style.display = "block";
            recurringFields.style.display = "none";
        } else {
            oneTimeFields.style.display = "none";
            recurringFields.style.display = "block";
        }
    }

    // Initial check
    toggleCustomCategory();
    toggleJobFields();

    // Event listeners
    categorySelect.addEventListener("change", toggleCustomCategory);
    jobTypeRadios.forEach(radio => {
        radio.addEventListener("change", toggleJobFields);
    });
});
