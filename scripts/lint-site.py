#!/usr/bin/env python3
"""The site's gate: run it before every commit that touches a word or a file.

    python3 scripts/lint-site.py              everything, offline
    python3 scripts/lint-site.py --self-test  proves every pattern catches what it should

It needs nothing but Python 3 and macOS's `sips` (for image sizes), and it never touches the network.
What it fails on, and why each one is here:

  WORDS (every text file in the repository, this one included, README and comments included):
  - an em or en dash, as a character or as an HTML entity. The game's house rule: no em or en dash in
    any user-facing string, and a website is nothing but user-facing strings.
  - a protected name: the arcade machine and alley game trademarks the brief warns about, the league
    abbreviations, the catch phrase, and the names of the developer's other games (guideline 2.3.7
    for the store; on a website the same names are what a search engine indexes and a lawyer reads).
    The patterns are the game repository's own (Scripts/lint-store-copy.py), spelled in pieces so
    this file does not trip its own scan.
  - the device's name anywhere in the published files, and the game's first name. App Review
    rejected the first name under guideline 5.2.5 for trading on the device's name, and the store
    copy now names no Apple product in any field a customer sees (the game repository's decisions
    340 and 341), so the site does not either: it says "a phone that folds".

  THE PUBLISHED FILES (everything _config.yml does not exclude):
  - a Liquid tag opener or YAML front matter. Jekyll copies a page byte for byte only while it has
    neither (see _config.yml); with either, Jekyll starts rewriting the privacy policy.
  - a <script>, an inline event handler, an iframe, a web font, or any stylesheet, script or image
    loaded from another host. The site runs no code and fetches nothing from anyone else, which is
    the privacy policy's promise made true of the website too.
  - an external link to a host not on the short allowlist below.
  - a root relative link or source that does not resolve to a file in this repository, and an <img>
    whose width and height attributes are not the file's real pixel size.
  - a page without the doctype, a viewport, a title, the stylesheet, a canonical URL on
    https://hingehoops.com (except the 404), or an og:image naming a file that does not exist.
  - an og:image whose og:image:width and height are not the file's, and a page without exactly one
    <link rel=icon> and one <link rel=apple-touch-icon> whose sizes attribute is the file's real size
    (both are the site's logo; README.md, "The pictures").

  THE FILES THAT ARE CONTRACTS:
  - CNAME, app-ads.txt (OWNERDOMAIN and the Google line), robots.txt, sitemap.xml (exactly the four
    pages, with the trailing slashes the app and the listing use).
  - privacy/index.html against docs/PRIVACY-POLICY.md in the game repository, WORD FOR WORD, when the
    game repository sits beside this one (../half_court_duo): the policy is that file's text and
    only that file's text. Skipped, and said so, when the game repository is not there.
"""

from __future__ import annotations

import html
import html.parser
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
GAME = ROOT.parent / "half_court_duo"
DOMAIN = "hingehoops.com"
PAGES = ["index.html", "privacy/index.html", "support/index.html", "terms/index.html"]
NOT_PUBLISHED = {"scripts", "README.md"}            # must agree with _config.yml's exclude list
TEXT_SUFFIXES = {".html", ".css", ".txt", ".xml", ".yml", ".md", ".py", ".sh", ""}
SELLER_LINE = "google.com, pub-5706069574815967, DIRECT, f08c47fec0942fa0"

# Hosts a page may link out to. Each is somewhere a player is sent on purpose: Apple's licence,
# privacy policy and refund page, and Google's two privacy pages the policy cites.
LINK_HOSTS = {"www.apple.com", "reportaproblem.apple.com", "policies.google.com"}

# Spelled in pieces, as the game repository's Scripts/lint-store-copy.py spells them, so that this
# file does not fail its own scan (it is scanned like every other file).
PROTECTED = [
    (re.compile(r"pop[\s-]?a[\s-]?" + "shot", re.I), "a registered trademark (the brief's 'avoid' list)"),
    (re.compile(r"skee[\s-]?" + "ball", re.I), "a registered trademark (PLATFORM.md 1)"),
    (re.compile(r"\b(" + "N" + "BA|W" + "N" + "BA|N" + "CAA" + r")\b"), "a league name"),
    (re.compile(r"he['\u2019]?s on " + "fire", re.I), "a catch phrase the house forbids"),
    (re.compile(r"\b(" + "muta" + "bloom|crater" + "gut|turf" + "storm|wen" + "dra" + r")\b", re.I),
     "another of the developer's apps (2.3.7; the site names none of them)"),
    (re.compile(r"\bduo[\s-]?(" + r"shoot" + r"out|al" + r"ley)\b", re.I),
     "another of the developer's apps (the sibling Duo games)"),
]
DASH = re.compile("[\u2013\u2014]|&[mn]dash;|&#(8211|8212|x201[34]);", re.I)
DEVICE = re.compile(r"iphone\s+duo", re.I)
# The first name, in prose or as the old domain. Spelled in pieces like the patterns above; it may
# still appear where nobody visiting the site reads it (the repository's own name in README.md).
OLD_NAME = re.compile(r"half[\s_-]?" + r"court[\s_-]?" + r"duo", re.I)


def published_files() -> list[pathlib.Path]:
    out = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT)
        top = rel.parts[0]
        if top.startswith(".") or top.startswith("_") or top in NOT_PUBLISHED:
            continue
        out.append(path)
    return out


def text_files() -> list[pathlib.Path]:
    out = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or ".git" in path.relative_to(ROOT).parts[:1]:
            continue
        if path.name == ".DS_Store" or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        out.append(path)
    return out


def rel(path: pathlib.Path) -> str:
    return str(path.relative_to(ROOT))


def check_words(problems: list[str]) -> None:
    published = set(published_files())
    for path in text_files():
        for number, line in enumerate(path.read_text(encoding="utf-8").split("\n"), 1):
            if DASH.search(line):
                problems.append(f"{rel(path)}:{number}: an em or en dash")
            for pattern, why in PROTECTED:
                if pattern.search(line):
                    problems.append(f"{rel(path)}:{number}: {why}")
            if path in published and DEVICE.search(line):
                problems.append(f"{rel(path)}:{number}: the device's name (guideline 5.2.5)")
            if path in published and OLD_NAME.search(line):
                problems.append(f"{rel(path)}:{number}: the game's first name (it is Hinge Hoops now)")
    # File names too: a name is as public as a sentence.
    for path in ROOT.rglob("*"):
        if ".git" in path.relative_to(ROOT).parts[:1]:
            continue
        for pattern, why in PROTECTED:
            if pattern.search(path.name):
                problems.append(f"{rel(path)}: {why}, in the file name")


class Page(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.tags: list[tuple[str, dict[str, str]]] = []
        self.main_text: list[str] = []
        self.in_main = 0

    def handle_starttag(self, tag, attrs):
        a = {k: (v or "") for k, v in attrs}
        self.tags.append((tag, a))
        if tag == "main":
            self.in_main += 1

    def handle_endtag(self, tag):
        if tag == "main":
            self.in_main -= 1

    def handle_data(self, data):
        if self.in_main:
            self.main_text.append(data)


_sizes: dict[pathlib.Path, tuple[int, int]] = {}


def pixel_size(path: pathlib.Path) -> tuple[int, int] | None:
    if path not in _sizes:
        try:
            out = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(path)],
                                 capture_output=True, text=True, check=True).stdout
        except (OSError, subprocess.CalledProcessError):
            return None
        w = re.search(r"pixelWidth: (\d+)", out)
        h = re.search(r"pixelHeight: (\d+)", out)
        if not (w and h):
            return None
        _sizes[path] = (int(w.group(1)), int(h.group(1)))
    return _sizes[path]


def resolve(url: str) -> pathlib.Path | None:
    """A root relative URL to the file GitHub Pages would serve for it, or None."""
    path = url.split("#", 1)[0].split("?", 1)[0]
    if not path.startswith("/"):
        return None
    target = ROOT / path.lstrip("/")
    if path.endswith("/"):
        target = target / "index.html"
    return target if target.is_file() else None


def check_pages(problems: list[str]) -> None:
    for path in published_files():
        if path.suffix != ".html":
            continue
        text = path.read_text(encoding="utf-8")
        name = rel(path)
        if text.startswith("---"):
            problems.append(f"{name}: YAML front matter (Jekyll would render this page)")
        if "{" + "{" in text or "{" + "%" in text:
            problems.append(f"{name}: a Liquid tag opener (Jekyll would rewrite this page)")
        if not text.lower().startswith("<!doctype html>"):
            problems.append(f"{name}: does not begin with <!doctype html>")
        if re.search(r"\son[a-z]+\s*=", text, re.I):
            problems.append(f"{name}: an inline event handler (the site runs no code)")
        if "fonts.googleapis" in text or "@font-face" in text or "@import" in text:
            problems.append(f"{name}: a web font or an imported stylesheet")

        page = Page()
        page.feed(text)
        tags = page.tags
        names = [t for t, _ in tags]
        for banned in ("script", "iframe", "object", "embed", "form"):
            if banned in names:
                problems.append(f"{name}: a <{banned}> (the site runs no code and collects nothing)")
        metas = {a.get("name") or a.get("property"): a.get("content", "") for t, a in tags if t == "meta"}
        if "viewport" not in metas:
            problems.append(f"{name}: no viewport meta")
        if "title" not in names:
            problems.append(f"{name}: no <title>")
        links = [a for t, a in tags if t == "link"]
        if not any(a.get("rel") == "stylesheet" and a.get("href") == "/style.css" for a in links):
            problems.append(f"{name}: does not link /style.css")
        canon = [a.get("href", "") for a in links if a.get("rel") == "canonical"]
        if name != "404.html":
            expected = f"https://{DOMAIN}/" + (name[: -len("index.html")] if name.endswith("index.html") else name)
            if canon != [expected]:
                problems.append(f"{name}: canonical is {canon}, expected [{expected!r}]")
        for key in ("og:image", "twitter:image"):
            if key in metas:
                prefix = f"https://{DOMAIN}/"
                url = metas[key]
                if not url.startswith(prefix) or resolve("/" + url[len(prefix):]) is None:
                    problems.append(f"{name}: {key} {url} does not name a file in this repository")
                elif key == "og:image":
                    size = pixel_size(resolve("/" + url[len(prefix):]))
                    declared = (metas.get("og:image:width"), metas.get("og:image:height"))
                    if size and declared != (str(size[0]), str(size[1])):
                        problems.append(f"{name}: og:image says {declared[0]} x {declared[1]}, the file is {size[0]} x {size[1]}")
        # The favicon and the home screen icon: the site's logo, on every page, at the size it claims.
        for kind in ("icon", "apple-touch-icon"):
            found = [a for a in links if a.get("rel") == kind]
            if len(found) != 1:
                problems.append(f"{name}: {len(found)} <link rel={kind}>, expected one")
                continue
            target, sizes = resolve(found[0].get("href", "")), found[0].get("sizes", "")
            size = pixel_size(target) if target is not None else None
            if size and sizes != f"{size[0]}x{size[1]}":
                problems.append(f"{name}: <link rel={kind}> says sizes={sizes!r}, the file is {size[0]}x{size[1]}")

        for tag, a in tags:
            for attr in ("href", "src"):
                url = a.get(attr)
                if url is None:
                    continue
                if url.startswith(("http://", "https://", "//")):
                    host = re.sub(r"^(https?:)?//", "", url).split("/", 1)[0]
                    if tag == "link" and a.get("rel") in ("canonical", "alternate"):
                        if host != DOMAIN:
                            problems.append(f"{name}: a canonical URL on another host: {url}")
                    elif tag != "a":
                        problems.append(f"{name}: <{tag} {attr}> loads from another host: {url}")
                    elif url.startswith("http://"):
                        problems.append(f"{name}: a plain http link: {url}")
                    elif host not in LINK_HOSTS:
                        problems.append(f"{name}: a link to {host}, which is not on LINK_HOSTS")
                elif url.startswith("mailto:"):
                    if not url.startswith("mailto:info@crindustries.xyz"):
                        problems.append(f"{name}: a mailto that is not the support address: {url}")
                elif url.startswith("#"):
                    ids = {b.get("id") for _, b in tags}
                    if url[1:] and url[1:] not in ids:
                        problems.append(f"{name}: a fragment link to #{url[1:]}, which no element has")
                elif url.startswith("/"):
                    if resolve(url) is None:
                        problems.append(f"{name}: {url} does not resolve to a file here")
                    elif url.endswith(".html") or (url.rstrip("/").split("/")[-1] in ("privacy", "support", "terms")
                                                   and not url.split("#")[0].endswith("/")):
                        problems.append(f"{name}: link {url} without the trailing slash (a redirect)")
                    frag = url.split("#", 1)[1] if "#" in url else ""
                    if frag:
                        target_text = resolve(url).read_text(encoding="utf-8")
                        if f'id="{frag}"' not in target_text:
                            problems.append(f"{name}: {url} points at #{frag}, which that page does not have")
                else:
                    problems.append(f"{name}: a relative URL {url!r} (use root relative: the 404 is served at any path)")
            if tag == "img":
                target = resolve(a.get("src", ""))
                if target is not None:
                    size = pixel_size(target)
                    declared = (a.get("width"), a.get("height"))
                    if size and declared != (str(size[0]), str(size[1])):
                        problems.append(f"{name}: <img {a.get('src')}> says {declared[0]} x {declared[1]}, the file is {size[0]} x {size[1]}")
                if "alt" not in a:
                    problems.append(f"{name}: <img {a.get('src')}> has no alt attribute")


def check_contracts(problems: list[str]) -> None:
    cname = (ROOT / "CNAME").read_text().strip() if (ROOT / "CNAME").exists() else None
    if cname != DOMAIN:
        problems.append(f"CNAME is {cname!r}, expected {DOMAIN!r}")

    ads = (ROOT / "app-ads.txt").read_text() if (ROOT / "app-ads.txt").exists() else ""
    lines = [l.strip() for l in ads.splitlines() if l.strip() and not l.strip().startswith("#")]
    if f"OWNERDOMAIN={DOMAIN}" not in lines:
        problems.append(f"app-ads.txt: no OWNERDOMAIN={DOMAIN} line")
    if SELLER_LINE not in lines:
        problems.append("app-ads.txt: the Google seller line is missing or altered")
    extra = [l for l in lines if l not in (f"OWNERDOMAIN={DOMAIN}", SELLER_LINE)]
    if extra:
        problems.append(f"app-ads.txt: lines nobody pasted from a network's dashboard: {extra}")

    robots = (ROOT / "robots.txt").read_text() if (ROOT / "robots.txt").exists() else ""
    if re.search(r"^\s*Disallow:\s*\S", robots, re.M):
        problems.append("robots.txt: a Disallow (app-ads.txt must stay crawlable)")
    if f"Sitemap: https://{DOMAIN}/sitemap.xml" not in robots:
        problems.append("robots.txt: no Sitemap line")

    sitemap = (ROOT / "sitemap.xml").read_text() if (ROOT / "sitemap.xml").exists() else ""
    locs = re.findall(r"<loc>([^<]+)</loc>", sitemap)
    wanted = [f"https://{DOMAIN}/" + p[: -len("index.html")] for p in PAGES]
    if sorted(locs) != sorted(wanted):
        problems.append(f"sitemap.xml lists {locs}, expected {wanted}")

    config = (ROOT / "_config.yml").read_text() if (ROOT / "_config.yml").exists() else ""
    excluded = set(re.findall(r"^\s*-\s*(\S+)\s*$", config, re.M))
    if excluded != NOT_PUBLISHED:
        problems.append(f"_config.yml excludes {sorted(excluded)}; this script believes {sorted(NOT_PUBLISHED)}")
    if (ROOT / ".nojekyll").exists():
        problems.append(".nojekyll exists: with Jekyll off, _config.yml's exclude list is ignored")

    for page in PAGES + ["404.html", "style.css"]:
        if not (ROOT / page).is_file():
            problems.append(f"{page} is missing")


def words(text: str) -> list[str]:
    return re.findall(r"[^\s]+", text)


def check_policy(problems: list[str], notes: list[str]) -> None:
    source = GAME / "docs" / "PRIVACY-POLICY.md"
    if not source.is_file():
        notes.append(f"SKIP the privacy page against the policy: {source} is not here")
        return
    md = source.read_text(encoding="utf-8")
    md = re.sub(r"<!--.*?-->", "", md, flags=re.S)            # the file's own note to the reader
    md = re.sub(r"^#+\s*", "", md, flags=re.M)                # headings
    md = re.sub(r"^\s*-\s+", "", md, flags=re.M)              # list markers
    md = md.replace("**", "").replace("`", "")
    page = Page()
    page.feed((ROOT / "privacy" / "index.html").read_text(encoding="utf-8"))
    ours = html.unescape("".join(page.main_text))
    a, b = words(md), words(ours)
    if a == b:
        notes.append(f"privacy/index.html is docs/PRIVACY-POLICY.md word for word ({len(a)} words)")
        return
    i = 0
    while i < min(len(a), len(b)) and a[i] == b[i]:
        i += 1
    problems.append(
        "privacy/index.html differs from docs/PRIVACY-POLICY.md at word "
        f"{i + 1}: the policy has {' '.join(a[max(0, i - 6):i + 8])!r}, "
        f"the page has {' '.join(b[max(0, i - 6):i + 8])!r}")


def self_test() -> list[str]:
    caught = {
        "pop": ["Pop-A-" + "Shot", "pop a " + "shot"],
        "skee": ["Skee-" + "Ball", "skee" + "ball"],
        "league": ["the N" + "BA finals", "a W" + "N" + "BA star", "NC" + "AA bracket"],
        "phrase": ["He's on " + "fire!", "he\u2019s on " + "fire"],
        "apps": ["like crater" + "gut", "muta" + "bloom's lesson", "Turf" + "storm", "wen" + "dra",
                 "Duo Shoot" + "out", "duo al" + "ley"],
    }
    missed = ["ABBA", "nbattery", "unbalanced", "on fire", "a mutable bloom", "cratered", "stormy turf",
              "Daily Shootout", "a bowling alley"]
    problems = []
    for group, needles in caught.items():
        for needle in needles:
            if not any(p.search(needle) for p, _ in PROTECTED):
                problems.append(f"self-test: no pattern catches {needle!r} ({group})")
    for text in missed:
        for p, why in PROTECTED:
            if p.search(text):
                problems.append(f"self-test: {text!r} is caught as {why}, and should not be")
    for needle in ["an em \u2014 dash", "1\u20132", "&m" + "dash;", "&n" + "dash;", "&#82" + "12;", "&#x20" + "13;"]:
        if not DASH.search(needle):
            problems.append(f"self-test: the dash pattern misses {needle!r}")
    if DASH.search("a hyphen-minus is fine, and &middot; too"):
        problems.append("self-test: the dash pattern catches a hyphen")
    for needle in ["Designed for iP" + "hone Duo", "the iP" + "hone  duo game"]:
        if not DEVICE.search(needle):
            problems.append(f"self-test: the device's name is not caught in {needle!r}")
    for needle in ["Half Court " + "Duo", "half" + "courtduo.com", "HALF COURT " + "DUO"]:
        if not OLD_NAME.search(needle):
            problems.append(f"self-test: the first name is not caught in {needle!r}")
    for text in ["Hinge Hoops", "a half court shot", "a phone that folds"]:
        if DEVICE.search(text) or OLD_NAME.search(text):
            problems.append(f"self-test: {text!r} is caught, and should not be")
    return problems


def main() -> int:
    problems = self_test()
    if "--self-test" in sys.argv:
        for p in problems:
            print(f"FAIL {p}")
        print("self-test: " + ("failed" if problems else "clean"))
        return 1 if problems else 0
    notes: list[str] = []
    check_words(problems)
    check_pages(problems)
    check_contracts(problems)
    check_policy(problems, notes)
    for note in notes:
        print(f"     {note}")
    for p in problems:
        print(f"FAIL {p}")
    print("lint-site: " + (f"{len(problems)} problem(s)" if problems else "clean"))
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
