from urllib.parse import quote

def social_share_links(title, link):
    text = quote(f"{title} | via DeCyberGuardian")
    url = quote(link)

    return {
        "x": f"https://twitter.com/intent/tweet?text={text}&url={url}",
        "linkedin": f"https://www.linkedin.com/sharing/share-offsite/?url={url}"
    }
