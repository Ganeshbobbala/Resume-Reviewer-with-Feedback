const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const rootDir = path.resolve(__dirname, '..');
const venvPythonWin = path.join(rootDir, 'backend', 'venv', 'Scripts', 'python.exe');
const venvPythonUnix = path.join(rootDir, 'backend', 'venv', 'bin', 'python');

let pythonBin = 'python';
if (process.platform === 'win32' && fs.existsSync(venvPythonWin)) {
  pythonBin = venvPythonWin;
} else if (fs.existsSync(venvPythonUnix)) {
  pythonBin = venvPythonUnix;
}

const args = [
  '-m', 'uvicorn',
  'main:app',
  '--app-dir', path.join(rootDir, 'backend'),
  '--host', '127.0.0.1',
  '--port', '8000',
  '--reload'
];

console.log(`[Backend Runner] Launching FastAPI using ${pythonBin}...`);

const child = spawn(pythonBin, args, {
  cwd: rootDir,
  stdio: 'inherit',
  shell: true
});

child.on('error', (err) => {
  console.error('[Backend Runner Error]:', err.message);
});

child.on('exit', (code) => {
  process.exit(code || 0);
});
