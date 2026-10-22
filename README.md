# Football News Summary Tool
## MVP:
  A basic tool that will fetch me relevant football articles from past 1-2 days, and summarize each one for me. Like a newsletter.
  More on the technical side, will use google news API to fetch articles, LLM will then be invoked via custom prompt to summarize.

Run project: python -m uvicorn app.main:app --reload
