def filter_articles(articles, keyword=None, sources=None):
    filtered = articles

    if keyword:
        filtered = [
            a for a in filtered
            if keyword.lower() in a["title"].lower()
            or keyword.lower() in a["summary"].lower()
        ]

    if sources:
        filtered = [a for a in filtered if a["source"] in sources]

    return filtered
