"""
Minimal BLEU evaluation helper.

Input files:
  references.txt: one human reference translation per line
  hypotheses.txt: one model output per line, aligned to references

Run:
  python evaluate_bleu.py references.txt hypotheses.txt
"""
import sys
from sacrebleu import corpus_bleu, corpus_chrf

def read_lines(path):
    with open(path, encoding="utf-8") as f:
        return [line.rstrip("\n") for line in f]

if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit("Usage: python evaluate_bleu.py references.txt hypotheses.txt")
    refs = read_lines(sys.argv[1])
    hyps = read_lines(sys.argv[2])
    if len(refs) != len(hyps):
        raise SystemExit("Reference and hypothesis files must have the same number of lines.")
    print(f"BLEU: {corpus_bleu(hyps, [refs]).score:.2f}")
    print(f"chrF: {corpus_chrf(hyps, [refs]).score:.2f}")
