#!/usr/bin/env python3
"""Fetch version-matched official Spring/JUnit API evidence for context smoke tests."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from hashlib import sha256
from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.request import Request, urlopen

E = Path(__file__).resolve().parent.parent / "evidence"
E.mkdir(exist_ok=True)
SPRING = "https://docs.spring.io/spring-framework/docs/6.2.11/javadoc-api/"
PAGES = [
    ("spring-junit-config", SPRING + "org/springframework/test/context/junit/jupiter/SpringJUnitConfig.html"),
    ("spring-extension", SPRING + "org/springframework/test/context/junit/jupiter/SpringExtension.html"),
    ("context-configuration", SPRING + "org/springframework/test/context/ContextConfiguration.html"),
    ("dirties-context", SPRING + "org/springframework/test/annotation/DirtiesContext.html"),
    ("bean-factory", SPRING + "org/springframework/beans/factory/BeanFactory.html"),
    ("junit-assertions", "https://docs.junit.org/5.12.2/api/org.junit.jupiter.api/org/junit/jupiter/api/Assertions.html"),
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
    slug, url = page
    request = Request(url, headers={"User-Agent": "iSLDevs-technical-verification/1.0"})
    with urlopen(request, timeout=60) as response:
        data = response.read()
        result = {"slug": slug, "requested_url": url, "resolved_url": response.url,
                  "http_status": response.status,
                  "content_type": response.headers.get("Content-Type"),
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
    result["text_sha256"] = sha256((text + "\n").encode()).hexdigest()
    print(slug, result["http_status"], result["sha256"])
    return result

def write_claims(results):
    specifications = [
        ("spring-junit-config", "@SpringJUnitConfig combines JUnit Jupiter extension registration with Spring context configuration.", "@SpringJUnitConfig is a composed annotation", 330),
        ("spring-extension", "SpringExtension integrates Spring TestContext support with JUnit Jupiter.", "SpringExtension integrates the Spring TestContext Framework", 330),
        ("spring-extension", "The extension delegates preparation of the JUnit test instance to TestContextManager.", "void postProcessTestInstance", 240),
        ("context-configuration", "@ContextConfiguration provides metadata determining which ApplicationContext is loaded for the integration test.", "@ContextConfiguration is an annotation", 440),
        ("dirties-context", "@DirtiesContext can close and evict the test context.", "the ApplicationContext associated with a test is dirty", 350),
        ("dirties-context", "AFTER_CLASS is an after-current-class lifecycle mode.", "After current test class", 190),
        ("bean-factory", "Typed getBean lookup selects a uniquely matching bean instance.", "<T> T getBean ( Class <T> requiredType) Return the bean instance", 220),
        ("junit-assertions", "assertSame checks that the expected and actual references identify the same object.", "Assert that the expected object and the actual object are the same object.", 180),
    ]
    claims = []
    for slug, claim, needle, length in specifications:
        text = (E / f"java-doc-{slug}.txt").read_text()
        offset = text.find(needle)
        assert offset >= 0, (slug, needle)
        claims.append({"claim": claim, "page": slug,
                       "exact_excerpt": text[offset:offset + length].strip(),
                       "text_offset": offset})
    for record in results:
        assert record["http_status"] == 200
        assert sha256((E / record["html_file"]).read_bytes()).hexdigest() == record["sha256"]
        record["text_sha256"] = sha256((E / record["text_file"]).read_bytes()).hexdigest()
    evidence = {
        "scope": "Version-matched official API excerpts; application behavior coverage is determined by the actual test assertions, not by this API documentation.",
        "claims": claims,
        "cleanup_note": "DirtiesContext docs recommend it when a test has modified the context. Explicit AFTER_CLASS cleanup is supported, but normal non-mutating smoke tests can retain the TestContext cache.",
    }
    (E / "java-doc-claims.json").write_text(json.dumps(evidence, indent=2) + "\n")

def main():
    with ThreadPoolExecutor(max_workers=6) as pool:
        results = list(pool.map(fetch, PAGES))
    write_claims(results)
    (E / "java-doc-official-documentation.json").write_text(json.dumps(results, indent=2) + "\n")

if __name__ == "__main__":
    main()
