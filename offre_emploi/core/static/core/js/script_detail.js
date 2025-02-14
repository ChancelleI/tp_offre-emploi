document.addEventListener("DOMContentLoaded", function () {
    // Initialisation de intl-tel-input
    var input = document.querySelector("#tel");
    var iti = window.intlTelInput(input, {
        initialCountry: "auto",  // Détecte automatiquement le pays
        preferredCountries: ["fr", "us", "gb"],  // Liste des pays préférés (ex. France, États-Unis, Royaume-Uni)
        utilsScript: "https://cdnjs.cloudflare.com/ajax/libs/intl-tel-input/17.0.8/js/utils.js" // Nécessaire pour valider le format
    });

    // Ajouter la logique de validation et de soumission du formulaire
    document.getElementById("applyForm").addEventListener("submit", function (event) {
        event.preventDefault(); // Empêche le rechargement de la page

        var phoneNumber = input.value;

        // Vérifier si le numéro est valide
        if (!iti.isValidNumber()) {
            alert("Numéro de téléphone invalide !");
            return false; // Empêche l'envoi du formulaire si le numéro est invalide
        }

        var formData = new FormData(this); // Récupère les données du formulaire

        // Envoi de la candidature via AJAX
        fetch("{% url 'apply_for_job' job_offer.id %}", {
            method: "POST",
            body: formData,
            headers: {
                "X-Requested-With": "XMLHttpRequest" // Indique que c'est une requête AJAX
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Ferme le modal
                var modal = document.getElementById("applyModal");
                var modalInstance = bootstrap.Modal.getInstance(modal);
                modalInstance.hide();

                // Supprime l'arrière-plan du modal (si nécessaire)
                document.querySelector(".modal-backdrop").remove();

                // Affiche le message de succès
                document.getElementById("successMessage").style.display = "block";
            } else {
                alert("❌ Erreur : " + data.error);
            }
        })
        .catch(error => console.error("Erreur:", error));
    });
});
