import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const htmlFiles = fs.readdirSync(root).filter((f) => f.endsWith(".html"));
const hrefRe = /href\s*=\s*"([^"]+)"/gi;
let failed = 0;

for (const file of htmlFiles) {
  const src = fs.readFileSync(path.join(root, file), "utf8");
  let m;
  while ((m = hrefRe.exec(src))) {
    const href = m[1];
    if (
      href.startsWith("http") ||
      href.startsWith("mailto:") ||
      href.startsWith("tel:") ||
      href.startsWith("#") ||
      href.startsWith("data:")
    ) {
      continue;
    }
    const clean = href.split("#")[0].split("?")[0];
    if (!clean) continue;
    const target = path.join(root, clean);
    if (!fs.existsSync(target)) {
      console.error(`MISSING from ${file}: ${href}`);
      failed++;
    }
  }
}

if (failed) {
  console.error(`Failed: ${failed}`);
  process.exit(1);
}
console.log(`OK: checked ${htmlFiles.length} HTML files`);
