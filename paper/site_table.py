"""Print the project page's results table from the paper's Table 2 source.

Reads paper/src/generated/controlled_full_table.tex and keeps the registration
recall (RR) columns and the 3DLoMatch+FPFH time, so the page never retypes a
number by hand. Usage: python paper/site_table.py > table.html
"""
import re
from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "src" / "generated" / "controlled_full_table.tex"
RR_COLUMNS = [1, 4, 7, 10, 13, 16]  # RR of 3DMatch, 3DLoMatch, KITTI x (FPFH, FCGF)
TIME_COLUMN = 19
GROUPS = {
    "Correspondence frontends": "Native output",
    "Using the point clouds": "Methods that also use the point clouds",
    "Each frontend + our common finishing and release": "Each frontend + our finishing and release (F+R)",
}


def cell(tex):
    tex = tex.strip()
    for macro, tag in (("textbf", "b"), ("underline", "u")):
        m = re.fullmatch(r"\\%s\{(.*)\}" % macro, tex)
        if m:
            return f"<{tag}>{cell(m.group(1))}</{tag}>"
    return tex.replace("--", "&ndash;")


def name(tex):
    tex = tex.replace("SC$^2$", "SC<sup>2</sup>").replace("$^\\dagger$", "<sup>&dagger;</sup>")
    return tex.replace("+ F+R", "+ F+R").strip()


def main():
    rows, group = [], None
    for line in SOURCE.read_text().splitlines():
        if line.startswith("\\multicolumn{20}"):
            label = re.search(r"\\emph\{([^}(]*)", line).group(1).strip()
            group = next(v for k, v in GROUPS.items() if label.startswith(k))
            rows.append(f'<tr class="group"><td colspan="8">{group}</td></tr>')
        elif group and line.rstrip().endswith("\\\\") and "&" in line:
            parts = [p.strip() for p in line.rstrip()[:-2].split("&")]
            cells = [cell(parts[i]) for i in RR_COLUMNS] + [cell(parts[TIME_COLUMN])]
            highlight = ' class="ours"' if parts[0].startswith("NGRR-LS + F+R") else ""
            rows.append(f"<tr{highlight}><td>{name(parts[0])}</td>" + "".join(f"<td>{c}</td>" for c in cells) + "</tr>")
    print("\n".join(rows))


if __name__ == "__main__":
    main()
