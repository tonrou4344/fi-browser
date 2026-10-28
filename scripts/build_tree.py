import json
import re

with open(
 "data/fi_latest.json",
 encoding="utf-8"
) as f:

    rows = json.load(f)

tree = []

for row in rows:

    title = row["title"]

    level = len(
      re.match(
        r"^・*",
        title
      ).group(0)
    )

    row["title"] = title.lstrip("・")

    row["level"] = level

with open(
 "data/tree.json",
 "w",
 encoding="utf-8"
) as f:

    json.dump(
      rows,
      f,
      ensure_ascii=False,
      indent=2
    )
