document.querySelectorAll(".upvote-button").forEach(button => {
  if (button.dataset.listenerAttached) return;

  button.dataset.listenerAttached = "true";
  button.classList.add("prevent-click");

  let isProcessing = false;

  button.addEventListener("click", async function () {
    if (isProcessing) return;
    isProcessing = true;

    const postId = this.dataset.postId;
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    try {
      const response = await fetch(`/ideas/post/${postId}/upvote/`, {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrfToken,
          'X-Requested-With': 'XMLHttpRequest'
        }
      });

      if (response.ok) {
        const data = await response.json();
        this.innerHTML = data.upvoted
          ? `<i class="bi bi-shift-fill"></i> ${data.count}`
          : `<i class="bi bi-shift"></i> ${data.count}`;
      }
    } catch (err) {
      console.error("Upvote error:", err);
    }

    isProcessing = false;
  });
});


document.querySelectorAll(".post-card").forEach(card => {
  card.addEventListener("click", e => {
    if (e.target.closest(".prevent-click")) return; // Don't navigate if inside button container
    const url = card.dataset.url;
    if (url) {
      window.location.href = url;
    }
  });
});