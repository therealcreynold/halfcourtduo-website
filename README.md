# hingehoops.com

The website for Hinge Hoops, served by GitHub Pages. Four pages, a 404, one stylesheet, no build
step, no framework and no JavaScript: everything here is the file that gets served.

**The game was renamed on 27 October 2026.** It was Half Court Duo, at halfcourtduo.com, until App
Review rejected 1.0 (6) under guideline 5.2.5: "Duo" in the name traded on Apple's device name. The
owner chose Hinge Hoops and the domain hingehoops.com (the game repository's decisions 340 to 343), and
this repository says so everywhere a visitor or a crawler reads. The repository keeps its name
(`therealcreynold/halfcourtduo-website`), as the game keeps its bundle id, because neither is shown to
a player; the old name may appear only in places like this one, which are not published.

This is also the **only** copy. It does not live inside the game repository under `site/`, because the
two would drift the first time either was edited, and here that matters more than usual: the privacy
URL is compiled into the app binary, and the privacy page is a document Apple and Google hold the owner
to.

| Path | Why it exists |
|---|---|
| `index.html` | Landing page. Also the App Store Connect **Marketing URL**, which is the path ad network crawlers walk to reach `app-ads.txt` |
| `privacy/index.html` | App Store Connect **Privacy Policy URL**, and the link in the game's Settings, Ads, Privacy policy (`MoneyLinks.privacyPolicy`). Required before the app can be submitted, and named in the AdMob consent messages |
| `support/index.html` | App Store Connect **Support URL**. Required at submission. The app itself does not link here; its Settings emails the support address |
| `terms/index.html` | Terms of use on top of Apple's standard licence. Goes into no App Store Connect field, and the app does not link it |
| `404.html` | Served by GitHub Pages for anything else, at whatever path was asked for |
| `app-ads.txt` | Must sit at the domain root, as `text/plain`. Holds `OWNERDOMAIN` and Google's seller line; see below |
| `style.css` | Every page's styles, in the game's own palette (`ArtPalette`) |
| `assets/` | The site's logo, the share card, the screenshots, the badges: all drawn by the game; see "The pictures" |
| `robots.txt`, `sitemap.xml` | Allow everything; list the four pages |
| `CNAME` | The custom domain, for GitHub Pages |
| `_config.yml` | The list of things this repository is **not** allowed to publish |
| `scripts/` | The lint, the image and share card generators, the page photographer, the live checks and the DNS helper. Not published |

## Where the words come from

**Every claim on these pages is a claim about the build**, checked against the game's code and
`docs/DECISIONS.md` in the game repository (`../half_court_duo`), not against the brief:

- **The privacy page is `docs/PRIVACY-POLICY.md`, word for word.** Every heading, sentence and list item
  is that file's, in its order, turned into HTML; links were added to the two Google URLs it cites, to
  the words "Apple's privacy policy" (Apple's own page), and to the contact address, and nothing else. The game repository keeps the policy beside the privacy label and
  the privacy manifest and moves all three in one commit, so **the policy changes there first**, then
  here. `scripts/lint-site.py` compares the two word by word whenever the game repository sits beside
  this one, and fails on any difference.
- **The home page is the App Store listing's own words** (`docs/APP-STORE-LISTING.md`, the description,
  whose every claim has a row in that file's table naming the code that proves it). A few sentences are
  the listing's review notes or captions, and "Fold it. Flick it. Swish." is the brief's subtitle variant
  and the game's own share card tagline.
- **The support page is written from the code**, and quotes the words a player sees exactly as the code
  spells them ("Restore Purchases", "Ads are removed on this device. Thank you.", "Fold to continue",
  "Free to play, paid for by ads", "Watch for +30 s"), so a player can find the row it names.
- **The contact address is info@crindustries.xyz**, the one every sibling game and the app itself use
  (`MoneyLinks.supportAddress`). Nothing here needs email at hingehoops.com, so no forwarding address
  is configured. The old domain carried Namecheap's default email forwarding records (five
  `eforward*.registrar-servers.com` MX records and an SPF `TXT`, seen with `dig` on 25 October 2026);
  they are not GitHub's business and are left alone.

If the game changes, these pages change in the same pass, and each page's "Last updated" moves only when
the page was re-read against the code: a fresh date over stale prose asserts a re-read that did not
happen.

## Why the pages are directories, with the trailing slash

`privacy/index.html` rather than `privacy.html`, and every link written as `/privacy/`, because the app
links to `https://hingehoops.com/privacy/` and that exact string, slash included, is compiled into the
binary and typed into App Store Connect. A directory with an `index.html` serves at that URL on every
static host there is; `/privacy` without the slash is a 301 to it on GitHub Pages, which is harmless but
is a redirect, so nothing here links that way. If `/privacy/` ever 404s, the app ships with a dead
privacy link, which is a guideline 5.1.1 and 2.1 rejection.

Every link and asset is **root relative** (`/style.css`, `/assets/...`), because `404.html` is served at
whatever path was asked for, where a relative path would point nowhere.

## The two files that are not decoration

**`app-ads.txt`** is how advertising networks confirm that whoever sells advertising inside the game is
allowed to. It must be served from the root of the domain, as `text/plain`, HTTP 200, with no redirect
to another domain. Google crawls it by following the **Marketing URL** on the App Store listing, so
verification cannot begin until both the listing and this site are live; allow about 24 hours after
that.

**Its Google line is the same one the sibling games' sites carry, byte for byte, because it is the same
owner and the same AdMob publisher account**, pub-5706069574815967. `app-ads.txt` authorises a seller
account, not an app, and the game (then Half Court Duo) was added to that account on 2026-10-25 as AdMob app
`ca-app-pub-5706069574815967~8638154791` (the game repository's decision 220). Once that AdMob app is
linked to the live store listing, open AdMob's "Set up app-ads.txt" dialog for it and confirm the line;
if it ever differs, the dialog wins. A wrong `DIRECT` line authorises a seller that is not used, which
is worse than a missing one, because it looks verified and is not. Add another network's lines only when
that network is genuinely enabled in the shipping build; the game ships on AdMob alone, with no
mediation. The file's comments name no other property of the owner's: it is served as text at the root
and every ad network is guaranteed to read it.

**`privacy/index.html`** is described above. Its URL is in the app, in App Store Connect, and in the
AdMob GDPR and US state consent messages, which were published on 25 October 2026 naming it (the game
repository's decision 220). The app and App Store Connect say `https://hingehoops.com/privacy/` from
build 1.0 (7) (decision 343); the consent messages were published naming the old domain's
`https://halfcourtduo.com/privacy/`, and must be edited in AdMob to the new URL once this site serves it.

## Words that must never appear on this site

The game's house rules, and they hold here because a web page is what a search engine reads and what a
lawyer is shown:

- **No em or en dash**, anywhere, as a character or an entity.
- **No protected name**: the arcade basketball machine and alley game trademarks the brief warns about,
  the league abbreviations, the catch phrase, any team, league or player name, or another app's name.
- **None of the owner's other games**, by name or by link, the sibling games included.
  Cross-promotion belongs in AdMob house campaigns, not on a legal page.
- **The device's name nowhere, and the game's first name nowhere** (nor the old domain). App Review
  rejected the first name under guideline 5.2.5, and the store copy now names no Apple product in any
  field a customer sees (decision 341), so the site says "a phone that folds" or "your phone folded
  like a laptop". The old rule allowed the device's name as a platform statement; it does not any more.

`scripts/lint-site.py` enforces all four: the first three over every text file in the repository, this
README and its own source included, and the last over the published files. Its patterns are the game repository's (`Scripts/lint-store-copy.py`), spelled in
pieces so the script does not fail its own scan, and `--self-test` proves each one still catches what it
should. Run it before every commit that touches a word:

    python3 scripts/lint-site.py

It also fails on: a `<script>`, an iframe, a form, an inline handler or a web font (the site runs no code
and fetches nothing from anybody else, which is the privacy policy's promise made true of the website
too); an asset loaded from another host; an external link outside a short allowlist (Apple's licence,
privacy and refund pages, and the two Google pages the policy cites); a root relative link or fragment
that does not resolve; an `<img>`, an `og:image` or an icon link whose declared size is not the file's
real size; a page without exactly one favicon and one apple-touch-icon link; a page missing its
canonical URL, title, viewport or stylesheet; Liquid syntax or front matter; and `CNAME`, `app-ads.txt`,
`robots.txt`, `sitemap.xml` or `_config.yml` drifting from what this README says.

## The pictures

Every image here was drawn by the game: the site's logo, rendered from the game's code by its own
`hcd-art` (below); and, from art committed in the game repository's `marketing/`, the fifteen
achievement badges (`swift run hcd-art badges`) and the store screenshots, each a `-halfcourt-showcase`
launch of the real app frozen on one scripted moment and seated in a folded phone the game repository's
composer draws in HTML and CSS. Nothing was downloaded, traced, painted over or generated by a model.

    scripts/make-images.sh      re-derives assets/ from ../half_court_duo (the logo by hcd-art, the rest
                                from its marketing/); it builds hcd-art with the Xcode seed, as the game does
    scripts/make-og.sh          re-renders the share card, assets/og-3.jpg, from scripts/og-card.html

`make-images.sh` cuts each screenshot just below its store caption: those words would repeat the page's
own prose, and words inside a picture are invisible to the lint and to a diff. The cut is done by
headless Brave on a local file (`sips --cropOffset` is unreliable), at pixel rows measured on the
committed pictures and written at the top of the script. The share card's words are text in
`og-card.html`, and it says nothing about availability, so it cannot go stale on launch day. **If its
wording or its logo ever changes, write it to a new file name** (`og-4.jpg` next) and point the pages
at that: messaging apps and social sites cache a card by its URL for days, and keep the old file
published for a release cycle so links already in the wild keep their picture. Two exceptions, both
deleted the day they were replaced. `og-1.jpg`, the first card, showed option A, an icon option the
owner did not choose, and had been public for about an hour. `og-2.jpg` carried the game's first name
and the device's, the words App Review rejected, and every link to it in the wild names the old
domain, which this site stops answering on once `CNAME` names the new one; `og-3.jpg` carries Hinge Hoops. `scripts/check-live.sh`
holds every URL that served option A (the first card, `favicon-32.png`, `apple-touch-icon.png`,
`icon-256.png`) and `og-2.jpg` at 404, and holds the logo and the card it serves now to this
repository's bytes.

**Still to redraw after the rename: the screenshots.** Every picture under `assets/shots/` and
`assets/poses/`, and the hero picture inside `og-3.jpg`, is a capture of the app from before the
rename, and its cabinet sign reads the first name. They come from the game repository's committed
`marketing/` captures, which are recaptured there with the new sign; then run `scripts/make-images.sh`
here, then `scripts/make-og.sh`. Until hingehoops.com has first been pushed, `og-3.jpg` can be
overwritten in place, since no cache holds it yet; after that, the redrawn card is `og-4.jpg`. The
logo and the badges carry no name and were unchanged by the rename (re-rendered by `hcd-art`
on 27 October 2026, byte for byte the same).

### The site's logo is not the app's icon

The game draws five icon options in code (`IconDesign.options`), and on 25 October 2026 the owner chose
two of them (the game repository's decision 240):

| Option | Is | Where |
|---|---|---|
| 3, "Across the Fold" | **the app's icon** and the App Store icon | the game's `AppIcon.icon` and `marketing/app-icon-1024.png`. **Not pictured on this site** |
| 4, "Neon Swish" | **this site's logo**: a neon ball dropping into a neon hoop | the favicon, the home screen icon a visitor saves (apple-touch-icon), the mark beside the name in every page's header, the home page hero, and the share card |

`scripts/make-images.sh` renders option 4 with `swift run hcd-art marketing-icon <png> --design 4` (its
`LOGO_DESIGN`), opaque RGB at 1024, byte for byte the picture the owner chose from, and writes one
size per job: `logo-32.png` (favicon), `logo-96.png` (the header mark, drawn at 30 css px),
`logo-180.png` (apple-touch-icon; iOS rounds the corners itself) and `logo-256.png` (the hero at 88 css
px, and the share card). The game ships option 4 nowhere, so there is no committed file to copy, and
`marketing/app-icon-1024.png` is the other picture: never copy it here as the logo. Every page's alt
text and comment calls option 4 the logo, never the icon, because a visitor who installs the game sees
option 3 on the home screen. If the site's logo changes, change `LOGO_DESIGN`, run both scripts here
with the share card written to a new name, and fix this table; if the app's icon changes (the game's
`IconDesign.committed`), nothing here is drawn from it, so only this table changes.

## Looking at it

A lint asserts what a file holds; a defect is a fact about what a page draws. Every page is photographed
before a commit:

    scripts/shoot.sh /tmp/hingehoops-shots

That renders the five pages with headless Brave from local files (the root relative URLs are rewritten
in a temporary copy, never here), at 1280 px and at a 390 px phone width drawn at 2x, in light and dark,
each at the page's full height, cut into slices and downscaled to 1100 px. It reports any page wider than
its window, since sideways scrolling is invisible in a capture. A headless window is never narrower than
500 px, so the phone width is an iframe of exactly 390 px; a "390 px window" silently lays the page out
at 500 and clips it. Then open every slice and read it.

## Setting it up

**hingehoops.com is NOT set up yet** (27 October 2026). The repository, `CNAME`, `app-ads.txt`, the
pages, `scripts/dns.py` and `scripts/check-live.sh` all say hingehoops.com, but nothing has been pushed,
and the Pages custom domain, the DNS and the certificate are still to do: steps 3 to 6 below, for the
new domain. Until then the live site is the previous commit at halfcourtduo.com, which was set up on 25
October 2026 exactly as below (Pages from `main` at the root, Namecheap DNS, the certificate approved
for the apex and `www`, HTTPS enforced, `scripts/check-live.sh` clean).

**Mind the order.** GitHub Pages serves one custom domain per repository, so the push that carries this
`CNAME` stops halfcourtduo.com serving the site; the TestFlight build 1.0 (6), App Store Connect's URLs
and the AdMob consent messages still name halfcourtduo.com until they are moved (the game repository's
decision 343 moves the app and App Store Connect together with build 1.0 (7), once hingehoops.com
serves). Have hingehoops.com's DNS in place before the push, and decide what halfcourtduo.com does
afterwards (a registrar redirect to `https://hingehoops.com` keeps old links landing somewhere).

Read what is there before redoing anything (`dig +short hingehoops.com A`,
`dig +short www.hingehoops.com CNAME`, or `scripts/dns.py` without `--apply`). In order:

1. **Create the repository** `therealcreynold/halfcourtduo-website`, **public** (GitHub Pages on a free
   account serves only public repositories), with no README or licence from GitHub, then push:

       git remote add origin git@github.com:therealcreynold/halfcourtduo-website.git
       git push -u origin main

2. **Settings, Pages**: source "Deploy from a branch", branch `main`, folder `/ (root)`.
3. **Settings, Pages, Custom domain**: `hingehoops.com`. GitHub writes a `CNAME` file; one is already
   committed here, so it should simply agree.
4. **DNS at Namecheap**, assuming hingehoops.com is registered there as halfcourtduo.com was (done for
   halfcourtduo.com on 25 October 2026; not yet for hingehoops.com). Delete the parking records Namecheap adds
   to a new domain (on the siblings' domains they were a `CNAME www` to `parkingpage.namecheap.com` and a
   `URL Redirect @`), then add these nine. An apex domain needs A and AAAA records rather than a CNAME:

   | Type | Host | Value |
   |---|---|---|
   | A | @ | 185.199.108.153 |
   | A | @ | 185.199.109.153 |
   | A | @ | 185.199.110.153 |
   | A | @ | 185.199.111.153 |
   | AAAA | @ | 2606:50c0:8000::153 |
   | AAAA | @ | 2606:50c0:8001::153 |
   | AAAA | @ | 2606:50c0:8002::153 |
   | AAAA | @ | 2606:50c0:8003::153 |
   | CNAME | www | therealcreynold.github.io |

   All four A records and all four AAAA records, not one of each: they are GitHub's edge addresses, and
   dropping some costs availability rather than breaking the site outright, which shows up as an
   intermittent App Review failure. Leave any other record alone (email forwarding's MX and SPF records
   are not GitHub's business). `scripts/dns.py` does exactly this through Namecheap's API, reading and
   merging first, because Namecheap's `setHosts` replaces every record on the domain; it changes nothing
   without `--apply`.
5. **Enforce HTTPS**, back in Settings, Pages, once GitHub has issued the certificate (it can take up to
   24 hours to offer the checkbox; on the siblings it took about a minute). Apple will not accept a plain
   HTTP privacy policy URL.
6. Run `scripts/check-live.sh` until it is clean.

## Checking it actually works

    scripts/check-live.sh

It is the list below, made a script, plus four checks a browser cannot do: the served privacy page, the
site's logo at all four sizes and the share card are byte for byte this repository's, the URLs that once
served an icon option the owner did not choose are 404, `README.md`, `scripts/` and `_config.yml` are
NOT served, and the home page agrees with the App Store about whether the game is on sale (see "Launch
day"). By hand:

    curl -sSI https://hingehoops.com/                 # 200
    curl -sSI https://hingehoops.com/privacy/         # 200
    curl -sSI https://hingehoops.com/support/         # 200
    curl -sSI https://hingehoops.com/terms/           # 200
    curl -sSI https://hingehoops.com/privacy          # 301 to /privacy/
    curl -sSI https://hingehoops.com/nope             # 404, and the styled page ("Off the rim")
    curl -sSI https://hingehoops.com/app-ads.txt      # 200, content-type text/plain
    curl -sS  https://hingehoops.com/app-ads.txt      # OWNERDOMAIN and the Google line
    curl -sSI http://hingehoops.com/ | grep -i location        # https://hingehoops.com/
    curl -sSI https://www.hingehoops.com/ | grep -i location   # https://hingehoops.com/
    curl -sSI https://hingehoops.com/README.md        # 404: not published

The game repository's archive gate checks the privacy, support and `app-ads.txt` URLs too
(`Scripts/preflight-release.sh`, which `ci_post_clone.sh` requires). It fetches the served privacy
page and compares it with `docs/PRIVACY-POLICY.md` word for word, with the same normalisation as
`scripts/lint-site.py`, so a page that passes the lint here passes it there once deployed.

| App Store Connect field | Value |
|---|---|
| Privacy Policy URL | `https://hingehoops.com/privacy/` |
| Support URL | `https://hingehoops.com/support/` |
| Marketing URL | `https://hingehoops.com`, the **apex**, not a page |

`/terms/` goes into no App Store Connect field.

### Why Marketing URL must be the apex

Because it is the entry point of the `app-ads.txt` crawl. An ad network starts at the store listing,
reads the Marketing URL, takes the domain of it, and fetches `app-ads.txt` from the root of that domain.
Pointed at a page, the whole verification depends on the crawler reducing that to the apex rather than
looking for a `/privacy/app-ads.txt` that does not exist. Set it to the apex and there is nothing to
reduce and nothing to get wrong. Getting it wrong produces no error anywhere: the pages still work, the
listing looks fine, and AdMob verification simply never completes. The same reasoning is why
`OWNERDOMAIN` in `app-ads.txt` is `hingehoops.com` with no scheme and no path.

## What this repository publishes

**Only what `_config.yml` allows.** GitHub Pages deploys every file in a repository by default, so
without it this README and `scripts/` (with the lint's list of protected names) would be public pages.
`.nojekyll` does not help and cannot: with Jekyll off there is no ignore list at all. On another of the
owner's properties, the word list a lint existed to keep off the site was itself served as prose on the
domain the store listing pointed at. So Jekyll is on, and `exclude:` names `README.md` and `scripts`.
Jekyll copies these pages byte for byte because none has front matter or Liquid syntax, and the lint
fails if one ever does.

**Anything added to this repository is public the moment it is pushed unless it is named in
`_config.yml`. Add it there first**, and re-run `scripts/check-live.sh` after any change to that file:
an excluded page and a broken page look the same from a terminal.

## Launch day

The home page says **"Coming to the App Store."** in the hero, and nothing else on the site mentions
availability or a date. The game is not submitted yet (App Store Connect app `6826691353`). On the day it
goes on sale, in one commit:

- replace the hero's status line with a link to `https://apps.apple.com/app/id6826691353` (no country
  code, so each visitor lands in their own storefront), keeping "Free, with ads."; if that link carries
  a picture of what to look for in the store, it is the app's icon, option 3 (the game's
  `marketing/app-icon-1024.png`, resized by the script like the logo), with alt text calling it the
  app's icon, never the site's logo (see "The site's logo is not the app's icon");
- add `apps.apple.com` to `LINK_HOSTS` in `scripts/lint-site.py`, the one place the lint allows a new
  host;
- run the lint, `scripts/shoot.sh`, push, and `scripts/check-live.sh`.

A checklist in a README is not a mechanism: a sibling site said "Coming soon" for three days after its
game went on sale. So `scripts/check-live.sh` asks Apple's public lookup whether the app is on sale and
**fails while the page disagrees**, in either direction. Run it on launch day, and after every push.

## Left for a human, deliberately

- **AdMob's "Add store" link**, once the listing is live (decision 220 in the game repository). The
  GDPR and US state consent messages already exist and name the privacy URL above, which is live.
- **Any quote from a player.** Absent on purpose: nobody outside has played it.
