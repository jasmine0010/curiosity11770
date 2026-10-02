// Use an installed Python 3, including Codex's bundled runtime on this computer.
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const {spawnSync} = require('node:child_process');
const bundled = path.join(os.homedir(), '.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe');
const candidates = [process.env.CURIOSITY_PYTHON, fs.existsSync(bundled) && bundled, 'python3', 'python', ...(process.platform === 'win32' ? ['py'] : [])].filter(Boolean);
for (const python of candidates) {
  const check = spawnSync(python, ['-c','import sys; assert sys.version_info.major == 3'], {stdio:'ignore',windowsHide:true});
  if (check.status !== 0) continue;
  const run = spawnSync(python, [path.join(__dirname,'build_site.py')], {stdio:'inherit',windowsHide:true});
  process.exit(run.status ?? 1);
}
console.error('Python 3 was not found. Install Python 3 or set CURIOSITY_PYTHON to its executable path.');
process.exit(1);
