import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const repoDir = dirname(fileURLToPath(import.meta.url));
const sourceImage = resolve(repoDir, "entry.png");

if (!existsSync(sourceImage)) {
  throw new Error(`Missing required source image at ${sourceImage}`);
}

const targetDir = process.env.MAKEFUN_OUTPUT_DIR?.trim() || "/output";
const targetImage = join(targetDir, "entry.png");

mkdirSync(targetDir, { recursive: true });
copyFileSync(sourceImage, targetImage);
