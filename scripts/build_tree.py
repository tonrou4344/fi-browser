import json

with open(
    "data/fi_latest.json",
    encoding="utf-8"
) as f:

    rows = json.load(f)

root = []

stack = []

for row in rows:

    node = {
        **row,
        "children": []
    }

    level = row["level"]

    while (
        len(stack) > level
    ):
        stack.pop()

    if level == 0:

        root.append(node)

    else:

        stack[-1]["children"]\
            .append(node)

    stack.append(node)

with open(
    "data/tree.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        root,
        f,
        ensure_ascii=False,
        indent=2
    )
