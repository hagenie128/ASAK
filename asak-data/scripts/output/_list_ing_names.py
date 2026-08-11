import json
from pathlib import Path

rows = json.loads(Path(r"c:\ASAK-workspace\ASAK\asak-data\seed-v3\ing.json").read_text(encoding="utf-8"))
out = Path(r"c:\ASAK-workspace\ASAK\asak-data\scripts\output\ing_names.txt")
out.write_text("\n".join(f"{r['id']}\t{r['name']}" for r in rows), encoding="utf-8")
print(len(rows), "written to", out)
