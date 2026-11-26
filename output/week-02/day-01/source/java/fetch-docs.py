#!/usr/bin/env python3
"""Fetch version-matched official Spring/JUnit API evidence for implicit single-constructor injection."""
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
    ("spring-junit-config", SPRING + "org/springframework/test/context/junit/jupiter/SpringJUnitConfig.html"),
    ("import", SPRING + "org/springframework/context/annotation/Import.html"),
    ("bean-factory", SPRING + "org/springframework/beans/factory/BeanFactory.html"),
    ("junit-assertions", "https://docs.junit.org/5.12.2/api/org.junit.jupiter.api/org/junit/jupiter/api/Assertions.html"),
    ("autowired-reference", "https://docs.spring.io/spring-framework/reference/6.2/core/beans/annotation-config/autowired.html"),
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
        ("autowired", "For a Spring bean class with exactly one constructor, that constructor is used even without @Autowired.", "If a class only declares a single constructor to begin with, it will always be used, even if not annotated.", 164),
        ("autowired", "Autowired constructor resolution considers dependencies that can be satisfied by matching beans in the Spring container.", "The constructor with the greatest number of dependencies that can be satisfied by matching beans in the Spring container will be chosen.", 245),
        ("autowired-reference", "The documented single-constructor annotation omission has been supported since Spring Framework4.3.", "As of Spring Framework 4.3, an @Autowired annotation on such a constructor is no longer necessary if the target bean defines only one constructor to begin with.", 372),
        ("import", "@Import can register regular component classes, as used by the selected demo configuration.", "Allows for importing @Configuration classes, ImportSelector and ImportBeanDefinitionRegistrar implementations, as well as regular component classes", 282),
        ("spring-junit-config", "@SpringJUnitConfig combines the JUnit Jupiter SpringExtension with Spring context configuration metadata.", "@SpringJUnitConfig is a composed annotation that combines @ExtendWith(SpringExtension.class) from JUnit Jupiter with @ContextConfiguration from the Spring TestContext Framework", 292),
        ("bean-factory", "Typed getBean lookup returns the bean instance uniquely matching the requested object type.", "<T> T getBean ( Class <T> requiredType) Return the bean instance that uniquely matches the given object type, if any.", 190),
        ("junit-assertions", "assertSame verifies that expected and actual refer to the same object, not merely equal values.", "Assert that the expected object and the actual object are the same object.", 180),
    ]
    by_slug = {record["slug"]: record for record in results}
    claims = []
    for slug, claim, needle, length in specifications:
        text = (E / f"java-doc-{slug}.txt").read_text()
        offset = text.find(needle)
        assert offset >= 0, (slug, needle)
        record = by_slug[slug]
        claims.append({"claim": claim, "page": slug, "source_url": record["resolved_url"],
                       "source_html_sha256": record["sha256"],
                       "exact_excerpt": text[offset:offset + length].strip(),
                       "text_offset": offset})
    for record in results:
        assert record["http_status"] == 200
        assert sha256((E / record["html_file"]).read_bytes()).hexdigest() == record["sha256"]
        assert sha256((E / record["text_file"]).read_bytes()).hexdigest() == record["text_sha256"]
    evidence = {
        "scope": "Official API and reference evidence for implicit single-constructor injection into a Spring-managed bean. Actual configuration registration, injection identity, service execution and manually-created object control are separately verified by the compiled tests, not presumed from these documents.",
        "version_scope": "Four Spring API pages pinned to6.2.11 and JUnit Assertions pinned to5.12.2. The Spring autowired reference is the6.2 documentation branch; its explicit historical4.3 statement is retained with a content hash rather than falsely labeled a6.2.11-specific reference release.",
        "claims": claims,
        "limits": ["A single-constructor rule concerns Spring-managed beans, not arbitrary objects created with new.", "The demo has exactly one registered PaymentGateway candidate; multiple-candidate selection is outside this lesson.", "DemoPaymentGateway returns a deterministic demo string; the test does not process a real payment.", "These documentation excerpts do not claim any test passed; actual JUnit evidence records results separately."]
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
