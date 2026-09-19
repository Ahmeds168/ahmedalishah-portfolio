#!/usr/bin/env bash
#
# Publish a new podcast episode.
#
#   ./scripts/new-episode.sh <episode-number> <slug> <path-to-audio>
#
# e.g.
#   ./scripts/new-episode.sh 7 solidity-storage-layout ~/Downloads/episode.m4a
#
# What it does:
#   1. Uploads the audio to R2 (with --remote, which Wrangler v4 needs)
#   2. Reads the real duration from the file via ffprobe
#   3. Scaffolds src/content/podcast/<slug>.md with correct frontmatter
#   4. Generates the OG image
#
# What it does NOT do: write the transcript, the summary, the timestamps or
# the cross-links. Those still need you.

set -euo pipefail

BUCKET="ahmed-podcasts"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [ "$#" -ne 3 ]; then
  echo "usage: $0 <episode-number> <slug> <path-to-audio>" >&2
  exit 1
fi

NUM="$1"
SLUG="$2"
AUDIO="$3"

[ -f "$AUDIO" ] || { echo "error: no such file: $AUDIO" >&2; exit 1; }

PADDED=$(printf "%03d" "$NUM")
EXT="${AUDIO##*.}"
KEY="podcasts/${PADDED}-${SLUG}/episode.${EXT}"
MD="$ROOT/src/content/podcast/${SLUG}.md"

if [ -f "$MD" ]; then
  echo "error: $MD already exists — pick a different slug" >&2
  exit 1
fi

# --- 1. duration -------------------------------------------------------------
if command -v ffprobe >/dev/null 2>&1; then
  SECS=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$AUDIO" | cut -d. -f1)
  MINS=$(( (SECS + 30) / 60 ))   # nearest minute
else
  echo "warning: ffprobe not found — duration left as a placeholder" >&2
  SECS=0
  MINS=0
fi

# --- 2. upload to R2 ---------------------------------------------------------
# --remote is REQUIRED. Without it Wrangler v4 writes to a local simulator
# in ./.wrangler and reports success, and the file never reaches the bucket.
echo "→ uploading to r2://${BUCKET}/${KEY}"
npx wrangler r2 object put "${BUCKET}/${KEY}" \
  --file="$AUDIO" \
  --remote

# --- 3. scaffold the markdown ------------------------------------------------
TODAY=$(date +%Y-%m-%d)
cat > "$MD" <<EOF
---
title: "TODO — episode title"
shortDescription: "TODO — one sentence, shown in listings."
description: "TODO — a paragraph for SEO and the episode page."
episodeNumber: ${NUM}
date: ${TODAY}
duration: "${MINS} min"
durationSeconds: ${SECS}
featured: false
audioPath: "/${KEY}"
topics: ["TODO"]
inThisEpisode:
  - "TODO"
timestamps:
  - { time: "00:00", label: "Introduction" }
resources: []
relatedArticles: []
relatedEpisodes: []
---

TODO — full transcript. This renders as the page body and is what search
engines index, so it needs to be the real thing, not a summary.
EOF

echo "→ wrote ${MD#$ROOT/}"

# --- 4. OG image -------------------------------------------------------------
python3 "$ROOT/scripts/gen-og.py" "$SLUG" "PODCAST · EPISODE ${NUM}" "TODO — episode title" 2>/dev/null \
  && echo "→ generated public/images/og/${SLUG}.png" \
  || echo "note: OG image not generated — run scripts/gen-og.py once the title is set"

cat <<EOF

Done. Still to do by hand:
  1. Fill in the TODOs in ${MD#$ROOT/} (title, descriptions, topics, transcript)
  2. Re-run scripts/gen-og.py once the title is final
  3. npm run build   # confirms the frontmatter validates
  4. git add -A && git commit && git push

EOF
