// main.ts — u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee
// (Node 22, stdlib only).
// COPY-ONLY: it copies the committed entry.png into the output directory.
// It never runs draw.py: the grader runs this file read-only as user 65534,
// so any write beside the repo (or any attempt to regenerate the image)
// would fail. draw.py is a local build tool only.
import { copyFileSync, mkdirSync, readFileSync } from "node:fs";
import { createHash } from "node:crypto";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const src = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

mkdirSync(outDir, { recursive: true });
const bytes = readFileSync(src);
if (bytes.length < 8 || bytes[0] !== 0x89 || bytes[1] !== 0x50 ||
    bytes[2] !== 0x4e || bytes[3] !== 0x47) {
  throw new Error("entry.png is not a PNG file");
}
if (bytes.length > 1024 * 1024) {
  throw new Error(`entry.png is ${bytes.length} bytes, over the 1 MiB limit`);
}
// Gate: the sealed scorer requires exactly 1024x1024. PNG IHDR starts at
// byte 16 (width, height as big-endian uint32).
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width !== 1024 || height !== 1024) {
  throw new Error(`entry.png is ${width}x${height}, must be 1024x1024`);
}
copyFileSync(src, join(outDir, "entry.png"));
const hash = createHash("sha256").update(bytes).digest("hex");
console.log(`entry.png ${bytes.length} bytes ${width}x${height} sha256 ${hash}`);
