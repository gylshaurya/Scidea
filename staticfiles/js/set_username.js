document.addEventListener("DOMContentLoaded", function() {
    let usernameInput = document.getElementById("username");
    let statusElement = document.getElementById("username-status");
    let saveButton = document.querySelector(".save");
    let profileInput = document.getElementById("profile_picture");
    let profilePreview = document.getElementById("profile_preview");
    let removeImageContainer = document.getElementById("remove-image-container");
    let removeImageBtn = document.getElementById("remove-image-btn");

    function validateUsername() {
        let username = usernameInput.value.trim();
        let regex = /^[a-zA-Z0-9_.]+$/; // ✅ Allows A-Z, a-z, 0-9, _ and .
        let minLength = 4;
        let maxLength = 20;

        // Reset Status
        statusElement.textContent = "";
        statusElement.style.color = "black";

        if (username.length === 0) {
            disableSaveButton();
            return;
        }

        if (username.length < minLength) {
            statusElement.textContent = `❌ Username must be at least ${minLength} characters`;
            statusElement.style.color = "red";
            disableSaveButton();
            return;
        }

        if (username.length > maxLength) {
            statusElement.textContent = `❌ Username must be at most ${maxLength} characters`;
            statusElement.style.color = "red";
            disableSaveButton();
            return;
        }

        if (!regex.test(username)) {
            statusElement.textContent = "❌ Only alpha numeric characters underscore and dot are allowed";
            statusElement.style.color = "red";
            disableSaveButton();
            return;
        }

        checkUsername(username);
    }

    function checkUsername(username) {
        fetch(`/users/check-username/?username=${encodeURIComponent(username)}`)
            .then(response => response.json())
            .then(data => {
                if (data.available) {
                    statusElement.textContent = "✅ Username is available";
                    statusElement.style.color = "green";
                    enableSaveButton();
                } else {
                    statusElement.textContent = "❌ Username is already taken";
                    statusElement.style.color = "red";
                    disableSaveButton();
                }
            })
            .catch(error => {
                console.error("Error checking username:", error);
                statusElement.textContent = "⚠️ Error checking username";
                statusElement.style.color = "orange";
                disableSaveButton();
            });
    }

    function previewImage(event) {
        let reader = new FileReader();
        reader.onload = function() {
            profilePreview.src = reader.result;
            removeImageContainer.style.visibility = "visible";
        };
        reader.readAsDataURL(event.target.files[0]);
    }

    function removeImage() {
        let defaultImage = profilePreview.getAttribute("data-default");  // Get the default avatar
        profilePreview.src = defaultImage;
        profileInput.value = "";  // Clear file input
        removeImageContainer.style.visibility = "hidden";
    }

    // Attach event listeners
    profileInput.addEventListener("change", previewImage);
    removeImageBtn.addEventListener("click", removeImage);

    // If user has a Google profile picture, show remove button initially
    let googleImage = profilePreview.getAttribute("data-google");
    if (googleImage && googleImage !== profilePreview.getAttribute("data-default")) {
        removeImageContainer.style.visibility = "visible";
    }

    function disableSaveButton() {
        saveButton.disabled = true;
        saveButton.style.backgroundColor = "#ccc"; // Gray out the button
        saveButton.style.cursor = "not-allowed";
    }

    function enableSaveButton() {
        saveButton.disabled = false;
        saveButton.style.backgroundColor = "#000"; // Set to active color
        saveButton.style.cursor = "pointer";
    }

    // Attach event listeners
    usernameInput.addEventListener("input", validateUsername);
    profileInput.addEventListener("change", previewImage);
    removeImageBtn.addEventListener("click", removeImage);

    // Initially disable save button
    disableSaveButton();
});
