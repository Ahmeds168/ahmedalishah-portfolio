#!/usr/bin/env bash
#
# Transcribe a podcast episode with Groq's Whisper.
#
#   export GROQ_API_KEY=your_key
#   ./scripts/transcribe.sh ~/Downloads/episode.m4a
#
# Writes <name>.txt next to the audio file.
#
# Compresses first: speech at ~1000 kbps (NotebookLM's default) is wasteful,
# and Groq's free tier caps uploads at 25 MB. 96 kbps mono is transparent for
# voice and cuts a 45-minute episode from ~87 MB to ~8 MB — which also means
# listeners aren't downloading 87 MB on mobile data.

set -euo pipefail

[ $# -eq 1 ] || { echo "usage: $0 <audio-file>" >&2; exit 1; }
[ -n "${GROQ_API_KEY:-}" ] || { echo "error: GROQ_API_KEY not set" >&2; exit 1; }

SRC="$1"
[ -f "$SRC" ] || { echo "error: no such file: $SRC" >&2; exit 1; }

BASE="${SRC%.*}"
SMALL="${BASE}-compressed.m4a"
OUT="${BASE}.txt"

echo "→ compressing (96 kbps mono)"
ffmpeg -loglevel error -y -i "$SRC" -c:a aac -b:a 96k -ac 1 "$SMALL"

SIZE_MB=$(( $(stat -f%z "$SMALL" 2>/dev/null || stat -c%s "$SMALL") / 1024 / 1024 ))
echo "  $(basename "$SMALL") is ${SIZE_MB} MB"
if [ "$SIZE_MB" -gt 24 ]; then
  echo "  warning: over the 25 MB free-tier limit — lower the bitrate or split the file" >&2
fi

echo "→ transcribing via Groq whisper-large-v3-turbo"
curl -s https://api.groq.com/openai/v1/audio/transcriptions \
  -H "Authorization: Bearer ${GROQ_API_KEY}" \
  -F "file=@${SMALL}" \
  -F "model=whisper-large-v3-turbo" \
  -F "response_format=text" \
  -o "$OUT"

echo "→ wrote $(basename "$OUT") ($(wc -w < "$OUT" | tr -d ' ') words)"
cat <<EOF

Next: the raw transcript needs editing before it goes on the site — Whisper
gives you one unbroken block with no headings or paragraphs. Paste it into the
chat and I'll structure it into the episode page.

Also worth using ${SMALL} as the file you upload to R2.

EOF
