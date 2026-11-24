#!/usr/bin/env python3
"""Fetch official Spring 6.2.11 API pages and preserve evidence for this lesson."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from hashlib import sha256
from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.request import Request, urlopen

E = Path(__file__).resolve().parent.parent / "evidence"
E.mkdir(exist_ok=True)
BASE = "https://docs.spring.io/spring-framework/docs/6.2.11/javadoc-api/"
PAGES = [
    ("bean-factory", "org/springframework/beans/factory/BeanFactory.html"),
    ("hierarchical-bean-factory", "org/springframework/beans/factory/HierarchicalBeanFactory.html"),
    ("listable-bean-factory", "org/springframework/beans/factory/ListableBeanFactory.html"),
    ("configurable-context", "org/springframework/context/ConfigurableApplicationContext.html"),
    ("annotation-context", "org/springframework/context/annotation/AnnotationConfigApplicationContext.html"),
]

class Text(HTMLParser):
    def __init__(self):
        super().__init__()
        self.bits = []
        self.skip = 0
    def handle_starttag(self, tag, attrs):
        if tag in ("style", "script"):
            self.skip += 1
    def handle_endtag(self, tag):
        if tag in ("style", "script") and self.skip:
            self.skip -= 1
    def handle_data(self, value):
        if not self.skip:
            self.bits.append(value)

def fetch(page):
    slug, path = page
    url = BASE + path
    with urlopen(Request(url, headers={"User-Agent": "iSLDevs-technical-verification/1.0"}), timeout=60) as r:
        data = r.read()
        result = {"slug": slug, "requested_url": url, "resolved_url": r.url,
                  "http_status": r.status, "content_type": r.headers.get("Content-Type"),
                  "sha256": sha256(data).hexdigest(), "bytes": len(data),
                  "fetched_at_utc": datetime.now(timezone.utc).isoformat()}
    assert result["http_status"] == 200
    parser = Text()
    parser.feed(data.decode("utf-8"))
    text = " ".join(" ".join(parser.bits).split())
    (E / f"java-doc-{slug}.html").write_bytes(data)
    (E / f"java-doc-{slug}.txt").write_text(text + "\n")
    result["html_file"] = f"java-doc-{slug}.html"
    result["text_file"] = f"java-doc-{slug}.txt"
    print(slug, result["http_status"], result["sha256"])
    return result

with ThreadPoolExecutor(max_workers=5) as pool:
    results = list(pool.map(fetch, PAGES))
(E / "java-doc-official-documentation.json").write_text(json.dumps(results, indent=2) + "\n")
