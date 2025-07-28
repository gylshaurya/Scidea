document.addEventListener('DOMContentLoaded', () => {
    const tagElements = document.querySelectorAll('.tag');
    const selectedTagsInput = document.getElementById('selectedTags');
    const selectedIds = new Set();

    tagElements.forEach(tag => {
        tag.addEventListener('click', () => {
            const id = tag.dataset.id;
            if (selectedIds.has(id)) {
                selectedIds.delete(id);
                tag.classList.remove('selected');
            } else {
                selectedIds.add(id);
                tag.classList.add('selected');
            }
            selectedTagsInput.value = Array.from(selectedIds).join(',');
        });
    });
});