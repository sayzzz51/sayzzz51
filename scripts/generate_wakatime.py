
import os
import json
import base64
import html
import urllib.request
from pathlib import Path

API_KEY = os.environ["WAKATIME_API_KEY"]
API_URL = "https://wakatime.com/api/v1/users/current/stats/last_7_days"

encoded_key = base64.b64encode(API_KEY.encode()).decode()

request = urllib.request.Request(
    API_URL,
    headers={"Authorization": f"Basic {encoded_key}"}
)

with urllib.request.urlopen(request, timeout=30) as response:
    stats = json.loads(response.read().decode())["data"]

languages = sorted(
    stats.get("languages", []),
    key=lambda item: item.get("total_seconds", 0),
    reverse=True
)[:6]

total_time = stats.get("human_readable_total", "0 secs")
width = 620
bar_width = 350

colors = ["#7aa2f7", "#bb9af7", "#7dcfff",
          "#9ece6a", "#e0af68", "#f7768e"]

parts = []
parts.append(f'''<svg xmlns="http://www.w3.org/2000/svg"
 width="680" height="300" viewBox="0 0 680 300">
<rect width="680" height="300" rx="18" fill="#1a1b27"/>
<rect x="1" y="1" width="678" height="298" rx="17"
 fill="none" stroke="#414868"/>
<text x="28" y="39" fill="#c0caf5"
 font-family="Arial,sans-serif" font-size="19" font-weight="bold">
  CODING ACTIVITY
</text>
<text x="28" y="67" fill="#7aa2f7"
 font-family="Arial,sans-serif" font-size="13">
  LAST 7 DAYS
</text>
<text x="652" y="43" text-anchor="end" fill="#9ece6a"
 font-family="Arial,sans-serif" font-size="15">
  {html.escape(total_time)}
</text>
<line x1="28" y1="84" x2="652" y2="84" stroke="#414868"/>
''')

y = 116

for index, language in enumerate(languages):
    name = html.escape(language.get("name", "Other"))
    seconds = max(0, language.get("total_seconds", 0))
    percent = max(0, min(100, language.get("percent", 0)))
    bar = bar_width * percent / 100
    color = colors[index % len(colors)]

    parts.append(f'''
<text x="28" y="{y}" fill="#c0caf5"
 font-family="Arial,sans-serif" font-size="13">{name}</text>
<rect x="190" y="{y - 12}" width="{bar_width}" height="12"
 rx="6" fill="#292e42"/>
<rect x="190" y="{y - 12}" width="{bar:.2f}" height="12"
 rx="6" fill="{color}"/>
<text x="650" y="{y}" text-anchor="end" fill="#a9b1d6"
 font-family="Arial,sans-serif" font-size="12">{percent:.1f}%</text>
''')
    y += 30

if not languages:
    parts.append('''<text x="28" y="130" fill="#a9b1d6"
 font-family="Arial,sans-serif" font-size="14">
  No coding activity recorded yet.
</text>''')

parts.append('''<text x="28" y="282" fill="#565f89"
 font-family="Arial,sans-serif" font-size="11">
  Powered by WakaTime
</text>
</svg>''')

output = Path("assets/wakatime.svg")
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text("".join(parts), encoding="utf-8")

print(f"Generated {output}")
