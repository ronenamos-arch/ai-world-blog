import { execSync } from "node:child_process";
import path from "node:path";

export function commitAndPush(repoRoot, files, message) {
  const opts = { cwd: repoRoot, stdio: "pipe", encoding: "utf-8" };

  try {
    for (const f of files) {
      execSync(`git add "${path.relative(repoRoot, f)}"`, opts);
    }

    // Check if there are staged changes
    const status = execSync("git status --porcelain", opts);
    if (!status.trim()) {
      return { committed: false, reason: "no changes" };
    }

    execSync(`git commit -m "${message.replace(/"/g, '\\"')}"`, opts);
    execSync(`git push`, opts);

    const sha = execSync("git rev-parse HEAD", opts).trim();
    return { committed: true, sha };
  } catch (e) {
    throw new Error(`Git operation failed: ${e.message}`);
  }
}
