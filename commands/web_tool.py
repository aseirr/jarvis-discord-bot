from duckduckgo_search import DDGS


def web_search(query: str):

    try:

        results = []

        with DDGS() as ddgs:

            search_results = ddgs.text(
                query,
                max_results=5
            )

            for r in search_results:

                results.append(
                    f"🔹 {r.get('title', 'No title')}\n"
                    f"{r.get('body', 'No description')}\n"
                    f"{r.get('href', '')}"
                )

        if not results:
            return "No web results found."

        return "\n\n".join(results)

    except Exception as e:
        return f"Web search error: {e}"