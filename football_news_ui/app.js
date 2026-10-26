const articleList = document.querySelector('#article-list');
const articleTemplate = document.querySelector('#article-template');
const status = document.querySelector('#status');
const reloadButton = document.querySelector('#reload-button')

function formatDate(value) {
    if (!value) return 'Date unavailable';

    const date = new Date(value);

    if(Number.isNaN(date.getTime())) {
        return "Date Unavailable";
    }

    return date.toLocaleDateString(undefined, {
        year: "numeric",
        month: "short",
        day: "numeric",
    });
}

function createArticleElement(article) {
    const fragment = articleTemplate.content.cloneNode(true);
    fragment.querySelector('.article-title').textContent = article.title;
    fragment.querySelector(".publisher").textContent = article.publisher || "Unknown publisher";
    fragment.querySelector(".published-date").textContent = formatDate(article.published_at);
    fragment.querySelector(".article-summary").textContent = article.summary;

    const sourceLink = fragment.querySelector('.source-link');

    try {
        const url = new URL(article.publisher_url);

        if (!["http:", "https:"].includes(url.protocol)) {
            throw new Error("Unsupported URL");
        }

    sourceLink.href = url.href;
    } catch {
        sourceLink.remove();
    }

    return fragment;
}

const previousButton = document.querySelector("#previous-page");
const nextButton = document.querySelector("#next-page");
const pageLabel = document.querySelector("#page-label");
const competitionButtons = document.querySelectorAll("#competition-filters button");
let selectedCompetition = "";
let currentPage = 1;
let totalPages = 0;
let loading = false;
let loadFailed = false;
const pageSize = 10;

// Keep missing logos usable until their image files are added.
for (const button of competitionButtons) {
  const image = button.querySelector("img");
  if (image) {
    const showFallback = () => {
      const label = document.createElement("span");
      label.className = "logo-fallback";
      label.textContent = button.getAttribute("aria-label");
      image.replaceWith(label);
    };
    image.addEventListener("error", showFallback, { once: true });
    if (image.complete && image.naturalWidth === 0) showFallback();
  }
  button.addEventListener("click", () => {
    if (loading) return;
    selectedCompetition = button.dataset.competition;
    currentPage = 1;
    for (const other of competitionButtons) {
      other.setAttribute("aria-pressed", String(other === button));
    }
    loadArticles();
  });
}

function updateControls() {
  previousButton.disabled = loading || loadFailed || currentPage <= 1;
  nextButton.disabled = loading || loadFailed || currentPage >= totalPages;
  reloadButton.disabled = loading;
  for (const button of competitionButtons) button.disabled = loading;
}

async function loadArticles() {
  loading = true;
  loadFailed = false;
  updateControls();
  status.textContent = "Loading articles…";
  pageLabel.textContent = "";
  articleList.replaceChildren();
  try {
    // Repeat only if a refresh removed the requested page.
    while (true) {
      const parameters = new URLSearchParams({
        page: String(currentPage), page_size: String(pageSize),
      });
      if (selectedCompetition) parameters.set("competition", selectedCompetition);
      const response = await fetch(`/v1/articles/all?${parameters}`);
      if (!response.ok) throw new Error(`Request failed: ${response.status}`);
      const data = await response.json();
      if (!Array.isArray(data.items) || !Number.isInteger(data.total_pages)) {
        throw new Error("Expected paginated API response with items and total_pages. Update the backend first.");
      }
      if (data.total_pages > 0 && currentPage > data.total_pages) {
        currentPage = data.total_pages;
        continue;
      }
      currentPage = data.page;
      totalPages = data.total_pages;
      const feed = document.createDocumentFragment();
      for (const article of data.items) feed.append(createArticleElement(article));
      articleList.replaceChildren(feed);
      status.textContent = data.total ? `${data.total} matching articles` : "No summaries available for this selection.";
      pageLabel.textContent = totalPages ? `Page ${currentPage} of ${totalPages}` : "No pages";
      break;
    }
  } catch (error) {
    console.error(error);
    loadFailed = true;
    status.textContent = "Could not load articles. Check the browser console and API response.";
  } finally {
    loading = false;
    updateControls();
  }
}
previousButton.addEventListener("click", () => {
  if (!loading && currentPage > 1) { currentPage--; loadArticles(); }
});
nextButton.addEventListener("click", () => {
  if (!loading && currentPage < totalPages) { currentPage++; loadArticles(); }
});
reloadButton.addEventListener("click", loadArticles);
loadArticles();
