#!/usr/bin/env bash
# Checks the LIVE site, once DNS, GitHub Pages and HTTPS are set up (README.md, "Setting it up").
#
#     scripts/check-live.sh
#
# Network, read only: curl against https://halfcourtduo.com and one App Store lookup. Changes nothing.
# Run it after every push, after any change to _config.yml, and on the day the game goes on sale.
# Every line it prints is PASS or FAIL; it exits non-zero on any FAIL.
#
# What it holds, and why:
#   - the four pages serve 200 at the trailing slash URLs the app and the listing use, and the bare
#     paths redirect to them (the privacy URL is compiled into the app; a 404 there is a 2.1 rejection);
#   - the served privacy page is byte for byte this repository's (a push that did not deploy, or a
#     deploy of the wrong branch, looks fine from a browser);
#   - an unknown path serves the styled 404 with a 404 status;
#   - app-ads.txt is 200, text/plain, at the apex with no redirect, and carries the seller line;
#   - plain HTTP and www both land on the HTTPS apex;
#   - README.md, scripts/ and _config.yml are NOT served (on another property the lint's own word list
#     was published as a page; _config.yml's exclude list is what prevents it here);
#   - THE "COMING" LINE AGREES WITH THE APP STORE. A sibling site went on saying "Coming soon" for
#     three days after its game went on sale, because the change was a checklist item in a README and
#     a checklist item is not a mechanism. This asks Apple's public lookup whether the app is on sale
#     and fails when the home page disagrees, in either direction.
set -uo pipefail
SITE="$(cd "$(dirname "$0")/.." && pwd)"
HOST="https://halfcourtduo.com"
APPLE_ID="6826691353"          # App Store Connect's Apple ID for Half Court Duo (docs/STATUS.md)
fails=0
pass() { printf 'PASS %s\n' "$1"; }
fail() { printf 'FAIL %s\n' "$1"; fails=$((fails + 1)); }

status() { curl -sS -o /dev/null -w '%{http_code}' --max-time 20 "$1" 2>/dev/null; }
header() { curl -sSI --max-time 20 "$1" 2>/dev/null | tr -d '\r' | awk -v h="$(tr A-Z a-z <<< "$2")" \
    'BEGIN{FS=": "} tolower($1)==h {print $2}' | tail -1; }

for path in / /privacy/ /support/ /terms/ /app-ads.txt /robots.txt /sitemap.xml /style.css \
            /assets/og-1.jpg /assets/favicon-32.png; do
    code=$(status "$HOST$path")
    [ "$code" = 200 ] && pass "$path is 200" || fail "$path is $code, expected 200"
done

for path in /privacy /support /terms; do
    code=$(status "$HOST$path"); loc=$(header "$HOST$path" location)
    if [ "$code" = 301 ] && { [ "$loc" = "$HOST$path/" ] || [ "$loc" = "$path/" ]; }; then pass "$path redirects to $path/"
    else fail "$path is $code to '${loc}', expected 301 to $HOST$path/"; fi
done

if curl -sS --max-time 20 "$HOST/privacy/" 2>/dev/null | cmp -s - "$SITE/privacy/index.html"; then
    pass "the served privacy page is this repository's, byte for byte"
else
    fail "the served privacy page differs from privacy/index.html (not deployed, or the wrong branch)"
fi

code=$(status "$HOST/no-such-page-$$")
body=$(curl -sS --max-time 20 "$HOST/no-such-page-$$" 2>/dev/null)
if [ "$code" = 404 ] && grep -q "Off the rim" <<< "$body"; then pass "an unknown path serves the styled 404"
else fail "an unknown path is $code$(grep -q 'Off the rim' <<< "$body" || echo ', not the styled 404')"; fi

type=$(header "$HOST/app-ads.txt" content-type)
case "$type" in text/plain*) pass "app-ads.txt is $type" ;; *) fail "app-ads.txt is '$type', expected text/plain" ;; esac
if curl -sS --max-time 20 "$HOST/app-ads.txt" 2>/dev/null \
        | grep -qx 'google.com, pub-5706069574815967, DIRECT, f08c47fec0942fa0'; then
    pass "app-ads.txt carries the Google seller line"
else
    fail "app-ads.txt does not carry the Google seller line"
fi

loc=$(header "http://halfcourtduo.com/" location)
[ "$loc" = "$HOST/" ] && pass "http:// redirects to the HTTPS apex" || fail "http:// goes to '$loc'"
loc=$(header "https://www.halfcourtduo.com/" location)
[ "$loc" = "$HOST/" ] && pass "www redirects to the apex" || fail "www goes to '$loc'"

for path in /README.md /scripts/lint-site.py /scripts/check-live.sh /_config.yml /.gitignore; do
    code=$(status "$HOST$path")
    [ "$code" = 404 ] && pass "$path is not published" || fail "$path is $code: it is PUBLIC (see _config.yml)"
done

# The App Store's own answer. An empty result means not on sale in the US storefront (yet).
count=$(curl -sS --max-time 20 "https://itunes.apple.com/lookup?id=$APPLE_ID" 2>/dev/null \
    | python3 -c 'import json,sys; print(json.load(sys.stdin).get("resultCount", 0))' 2>/dev/null)
says_coming=$(grep -c "Coming to the App Store" "$SITE/index.html")
links_store=$(grep -c "apps.apple.com/app/id$APPLE_ID" "$SITE/index.html")
if [ -z "$count" ]; then
    fail "could not ask the App Store whether Half Court Duo is on sale"
elif [ "$count" -gt 0 ] && [ "$says_coming" -gt 0 ]; then
    fail "Half Court Duo is ON SALE and index.html still says 'Coming to the App Store'. README.md, 'Launch day'."
elif [ "$count" -gt 0 ] && [ "$links_store" -eq 0 ]; then
    fail "Half Court Duo is on sale and index.html has no link to it. README.md, 'Launch day'."
elif [ "$count" -eq 0 ] && [ "$links_store" -gt 0 ]; then
    fail "index.html links to the App Store page of an app that is not on sale"
else
    pass "the home page agrees with the App Store (on sale: $([ "$count" -gt 0 ] && echo yes || echo no))"
fi

echo
[ "$fails" -eq 0 ] && echo "check-live: clean" || echo "check-live: $fails failure(s)"
[ "$fails" -eq 0 ]
