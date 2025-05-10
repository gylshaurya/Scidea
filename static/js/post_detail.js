document.addEventListener("DOMContentLoaded", () => {
  const upvoteBtn = document.querySelector(".upvote-button");
  if (!upvoteBtn) return;

  let isProcessing = false;

  // Grab the post ID from a data attribute instead
  const postId = upvoteBtn.dataset.postId;
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;

  upvoteBtn.addEventListener("click", async function (e) {
    e.preventDefault();
    if (isProcessing || !csrfToken) return;
    isProcessing = true;

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
        upvoteBtn.innerHTML = data.upvoted
          ? `<i class="bi bi-shift-fill"></i> ${data.count}`
          : `<i class="bi bi-shift"></i> ${data.count}`;
      } else {
        console.error("Upvote request failed");
      }
    } catch (err) {
      console.error("Upvote error:", err);
    }

    isProcessing = false;
  });
});
