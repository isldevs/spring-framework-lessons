#!/usr/bin/env python3
"""Fetch version-matched official Spring/JUnit API evidence for dependency resolution."""
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
    ("autowired", SPRING + "org/springframework/beans/factory/annotation/Autowired.html"),
    ("bean", SPRING + "org/springframework/context/annotation/Bean.html"),
    ("bean-factory", SPRING + "org/springframework/beans/factory/BeanFactory.html"),
    ("default-listable-bean-factory", SPRING + "org/springframework/beans/factory/support/DefaultListableBeanFactory.html"),
    ("qualifiers-reference", "https://docs.spring.io/spring-framework/reference/6.2/core/beans/annotation-config/autowired-qualifiers.html"),
    ("primary-reference", "https://docs.spring.io/spring-framework/reference/6.2/core/beans/annotation-config/autowired-primary.html"),
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
        ("autowired", "For a Spring bean with a single constructor, Spring uses that constructor without requiring @Autowired.", "If a class only declares a single constructor to begin with, it will always be used, even if not annotated."),
        ("bean", "@Bean(autowireCandidate=false) removes this bean from consideration for autowiring.", "autowireCandidate boolean autowireCandidate Is this bean a candidate for getting autowired into some other bean at all? Default is true ; set this to false for internal delegates that are not meant to get in the way of beans of the same type in other places."),
        ("qualifiers-reference", "Qualifiers narrow compatible type matches; selection is not solely a bean-name lookup.", "You can associate qualifier values with specific arguments, narrowing the set of type matches so that a specific bean is chosen for each argument."),
        ("qualifiers-reference", "Bean-name fallback does not make an incompatible type into a matching dependency.", "qualifier values, even with the bean name fallback, always have narrowing semantics within the set of type matches. They do not semantically express a reference to a unique bean id"),
        ("qualifiers-reference", "Spring6.2 can use a matching-name shortcut; the example's observed full candidate route is not a universal ordering claim.", "As of 6.2, the container applies fast shortcut resolution for bean name matches, bypassing the full type matching algorithm when the parameter name matches the bean name and no type, qualifier, primary, or fallback conditions override the match."),
        ("primary-reference", "@Primary can choose among candidates for a single-valued dependency.", "If exactly one primary bean exists among the candidates, it becomes the autowired value."),
        ("bean-factory", "Typed getBean returns the bean instance that uniquely matches the requested type, if any.", "Return the bean instance that uniquely matches the given object type, if any."),
    ]
    by_slug = {record["slug"]: record for record in results}
    claims = []
    for slug, claim, needle in specifications:
        doc_text = (E / f"java-doc-{slug}.txt").read_text()
        offset = doc_text.find(needle)
        assert offset >= 0, (slug, needle)
        record = by_slug[slug]
        claims.append({"claim": claim, "page": slug, "source_url": record["resolved_url"],
                       "source_html_sha256": record["sha256"],
                       "exact_excerpt": needle, "text_offset": offset})
    for record in results:
        assert record["http_status"] == 200
        assert sha256((E / record["html_file"]).read_bytes()).hexdigest() == record["sha256"]
        assert sha256((E / record["text_file"]).read_bytes()).hexdigest() == record["text_sha256"]
    evidence = {
        "scope": "Official documentation supports required-type compatibility, candidate eligibility, optional qualifiers/primary/name matching and implicit single-constructor injection. Actual candidate discovery, filtering, injection identity and startup failures are separately verified by compiled JUnit tests and a delegated Spring observer.",
        "version_scope": "Four Spring API pages pinned to6.2.11; qualifiers and primary reference pages are the6.2 branch. Source-code inspection separately pins implementation details to the checksum-verified6.2.11 source JAR.",
        "claims": claims,
        "limits": ["The controlled test follows Spring's full candidate enumeration path, not every dependency-resolution path.", "No qualifier or primary selection is executed in these tests; those features are documented context only.", "A registered bean can be retrievable explicitly while excluded from autowiring; the actual test verifies that distinction.", "No real payment or standalone app run is claimed."]
    }
    for name in ["java-doc-claim-verification.json", "java-doc-claims.json"]:
        (E / name).write_text(json.dumps(evidence, indent=2) + "\n")

def main():
    with ThreadPoolExecutor(max_workers=6) as pool:
        results = list(pool.map(fetch, PAGES))
    write_claims(results)
    (E / "java-doc-official-documentation.json").write_text(json.dumps(results, indent=2) + "\n")

if __name__ == "__main__":
    main()
