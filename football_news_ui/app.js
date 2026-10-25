const articleList = document.querySelector('#article-list');
const articleTemplate = document.querySelector('#article-template');
const status = document.querySelector('#status');
const reloadButton = document.querySelector('#reload-button')

function formatDate(value) {
    if (!value) return 'Data Unavailable';

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

async function loadArticles() {
  reloadButton.disabled = true;
  status.textContent = "Loading articles…";
  articleList.replaceChildren();

  try {
    const response = await fetch("/v1/articles/all");

    if (!response.ok) {
      throw new Error(`Request failed: ${response.status}`);
    }

    const articles = await response.json();

    if (!Array.isArray(articles)) {
      throw new Error("Expected a list of articles");
    }

    const feed = document.createDocumentFragment();

    for (const article of articles) {
      feed.append(createArticleElement(article));
    }

    articleList.replaceChildren(feed);

    status.textContent = articles.length
      ? `${articles.length} articles`
      : "No summaries available yet.";
  } catch (error) {
    console.error(error);
    status.textContent =
      "Could not load articles. Please try reloading the feed.";
  } finally {
    reloadButton.disabled = false;
  }
}

reloadButton.addEventListener("click", loadArticles);

loadArticles();
