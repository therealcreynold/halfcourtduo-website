#!/usr/bin/env bash
# Renders the Open Graph share card, assets/og-3.jpg, from scripts/og-card.html.
#
#     scripts/make-og.sh                 writes assets/og-3.jpg
#     scripts/make-og.sh assets/og-4.jpg a new name, for when the card's words or pictures change
#
# WHY THERE IS A SCRIPT AND NOT JUST AN IMAGE. The card carries words, and a picture's words are
# invisible to grep, to a diff and to scripts/lint-site.py. Here they are text in og-card.html.
#
# WRITE TO A NEW FILENAME WHENEVER THE WORDING OR THE LOGO CHANGES. Messaging apps and social sites
# cache a card by its URL and serve the old bytes for days, so overwriting the card would leave the
# stale one in circulation exactly where it does the damage. Bump the name, point the four pages'
# og:image and twitter:image at it (scripts/lint-site.py checks they all name a file that exists),
# and keep the old file for a release cycle so links already in the wild do not break. og-3.jpg
# carries the site's logo, option 4 (README.md, "The pictures"), and the name Hinge Hoops. Two
# exceptions, both deleted the day they were replaced and both held gone by scripts/check-live.sh:
# og-1.jpg, the first card, which showed an icon option the owner did not choose and had been public
# for about an hour; and og-2.jpg, which carried the game's first name and the device's, the words
# App Review rejected under guideline 5.2.5, and whose links in the wild all name the old domain.
#
# The renderer is headless Brave on a local file: nothing is fetched. Run scripts/make-images.sh first
# if the logo or the hero screenshot changed, since the card draws both.
set -euo pipefail
SITE="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$SITE/${1:-assets/og-3.jpg}"
BRAVE="/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
[ -x "$BRAVE" ] || { echo "make-og: headless Brave not found at $BRAVE"; exit 1; }

WORK="$(mktemp -d -t hcd-og)"
trap 'rm -rf "$WORK"' EXIT
"$BRAVE" --headless --disable-gpu --hide-scrollbars --no-first-run --disable-background-networking \
    --disable-component-update --disable-sync --force-device-scale-factor=1 \
    --window-size=1200,630 --screenshot="$WORK/card.png" "file://$SITE/scripts/og-card.html" >/dev/null 2>&1
[ -s "$WORK/card.png" ] || { echo "make-og: Brave wrote nothing"; exit 1; }
sips -s format jpeg -s formatOptions 84 "$WORK/card.png" --out "$OUT" >/dev/null

# A card whose pictures failed to load is a sign and a pill on navy, which looks enough like a design
# to be committed by accident. The screenshot alone is most of the bytes; refuse a card without it.
bytes=$(stat -f%z "$OUT")
[ "$bytes" -gt 60000 ] || { echo "make-og: $OUT is only ${bytes} bytes; the pictures did not render."; exit 1; }
printf 'wrote %s (%s bytes) ' "${OUT#"$SITE/"}" "$bytes"
sips -g pixelWidth -g pixelHeight "$OUT" | tail -2 | tr -d '\n'; echo
