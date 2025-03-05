document.addEventListener("DOMContentLoaded", function() {
    flatpickr("#date_of_grant", {
        dateFormat: "Y-m-d",
        allowInput: false
    });

    document.querySelector("form").addEventListener("submit", function(e) {
        let fecha = document.getElementById("date_of_grant").value;
        if (!fecha) {
            alert("Por favor, selecciona una fecha.");
            e.preventDefault();
        }
    });
});