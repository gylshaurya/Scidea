document.addEventListener("DOMContentLoaded", function () {
    // Tag Selection Logic
    const tags = document.querySelectorAll(".tag");
    const selectedTagsInput = document.getElementById("selected_tags");

    tags.forEach(tag => {
        tag.addEventListener("click", function () {
            tag.classList.toggle("selected");
            updateSelectedTags();
        });
    });

    function updateSelectedTags() {
        const selectedTags = Array.from(document.querySelectorAll(".tag.selected"))
                               .map(tag => tag.dataset.value);
        selectedTagsInput.value = selectedTags.join(",");
    }

    // Save Draft Button Logic (Temporary Alert for now)
    document.querySelector(".save-draft").addEventListener("click", function () {
        alert("Draft saved! (Implement backend logic here)");
    });

    const postContent = document.querySelector(".post-content");

    postContent.addEventListener("input", function () {
        this.style.height = "auto"; // Reset height
        this.style.height = this.scrollHeight + "px"; // Set to new height
    });

});
