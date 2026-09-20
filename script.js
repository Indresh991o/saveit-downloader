// Shared logic for every platform page.
// Each HTML page sets `window.PLATFORM` before loading this file
// (e.g. "instagram", "pinterest", "youtube", "facebook").

const API_BASE = ""; // same-origin. Point this at your backend URL if hosted separately, e.g. "https://api.yourdomain.com"

function initDownloader() {
  const form = document.getElementById("dl-form");
  const input = document.getElementById("dl-url");
  const button = document.getElementById("dl-submit");
  const status = document.getElementById("dl-status");
  const resultCard = document.getElementById("dl-result");
  const resultThumb = document.getElementById("dl-thumb");
  const resultTitle = document.getElementById("dl-title");
  const resultSub = document.getElementById("dl-sub");
  const resultLink = document.getElementById("dl-link");

  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const url = input.value.trim();

    resultCard.classList.remove("visible");
    status.classList.remove("error", "success");

    if (!url) {
      status.textContent = "Pehle link paste karo.";
      status.classList.add("error");
      return;
    }

    button.disabled = true;
    button.textContent = "Fetching...";
    status.textContent = "Link check ho raha hai...";

    try {
      const res = await fetch(`${API_BASE}/api/download`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url, platform: window.PLATFORM }),
      });

      const data = await res.json();

      if (!res.ok || !data.success) {
        throw new Error(data.error || "Video fetch nahi ho paya. Link check karo.");
      }

      status.textContent = "Mil gaya! Neeche download karo.";
      status.classList.add("success");

      resultThumb.src = data.thumbnail || "";
      resultTitle.textContent = data.title || "Untitled";
      resultSub.textContent = data.duration ? `Duration: ${data.duration}` : (data.author || "");
      resultLink.href = data.download_url;
      resultLink.setAttribute("download", "");
      resultCard.classList.add("visible");
    } catch (err) {
      status.textContent = err.message || "Kuch galat ho gaya, dobara try karo.";
      status.classList.add("error");
    } finally {
      button.disabled = false;
      button.textContent = "Download";
    }
  });
}

document.addEventListener("DOMContentLoaded", initDownloader);
