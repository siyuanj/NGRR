#!/usr/bin/env bash
# Build the arXiv PDF and the arXiv upload archive from paper/src.
# Needs pdflatex and bibtex (TeX Live 2023 was used). No experiments are run.
set -euo pipefail
cd "$(dirname "$0")/src"
rm -f main.aux main.bbl main.blg main.log main.out main.brf main.pdf
run() { pdflatex -interaction=nonstopmode -halt-on-error main.tex > /dev/null || { tail -40 main.log; exit 1; }; }
run
bibtex main > /dev/null
run
# Back-references and cross-references settle after at most a few more passes.
for _ in 1 2 3; do
    run
    grep -q 'Rerun to get' main.log || break
done
if grep -nE 'undefined|multiply defined|Rerun to get|same identifier' main.log; then
    echo "build.sh: unresolved or duplicate references, see main.log" >&2
    exit 1
fi
cp main.pdf ../ngrr_arxiv.pdf
# arXiv does not run BibTeX, so the archive carries main.bbl next to the sources.
tar -czf ../ngrr_arxiv_source.tar.gz --exclude='main.aux' --exclude='main.blg' \
    --exclude='main.log' --exclude='main.out' --exclude='main.brf' --exclude='main.pdf' .
echo "built ../ngrr_arxiv.pdf ($(pdfinfo main.pdf 2>/dev/null | awk '/^Pages/ {print $2}') pages) and ../ngrr_arxiv_source.tar.gz"
