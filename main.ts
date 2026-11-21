// news-image-20261121 entrypoint (Node 22, standard library only).
//
// The front page was drawn ahead of time by generate.py (Python + Pillow) and
// ships beside this file as entry.png.b64 (base64 text, so the repository
// stays text-only). This program's only job is to place that exact image at
// /output/entry.png, deterministically: same input bytes, same output bytes,
// every run. It performs no network access and reads no clock, so two runs
// are byte-identical.
//
// Run locally:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
writeFileSync(join(outDir, "entry.png"), Buffer.from(readFileSync(join(here, "entry.png.b64"), "utf8"), "base64"));
