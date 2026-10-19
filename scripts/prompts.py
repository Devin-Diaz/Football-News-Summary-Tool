ARTICLE_SUMMARY_INSTRUCTIONS = """
First assess whether the supplied full_text is suitable for summarization.

Reject the entry if:
- Its substantive article text is predominantly not English.
- It contains navigation, advertisements, video listings, or other page
  elements instead of an article body.
- It concerns a different story from the supplied headline.
- It contains too little factual information to produce a useful,
  supported summary.

Do not reject an article merely because it is short.
A brief report containing a clear factual development can receive a
one-sentence summary. Names and quotations in other languages do not
by themselves make an English article non-English.

For accepted articles:
- Use one sentence for a very short report.
- Use one concise paragraph for a typical article.
- Use a second paragraph only when necessary.
- Do not pad the summary to reach a word count.

Return only a JSON object with these fields:
{
  "serve": true or false,
  "reason": "ok" | "non_english" | "unusable_content" |
            "content_mismatch" | "insufficient_information",
  "summary": "Summary text when serve is true; otherwise null"
}

Select the single most applicable reason.
"""