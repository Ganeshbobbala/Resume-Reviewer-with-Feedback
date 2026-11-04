const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const rootDir = path.resolve(__dirname, '..');
const backendDir = path.join(rootDir, 'backend');
const venvPythonWin = path.join(backendDir, 'venv', 'Scripts', 'python.exe');
const venvPythonUnix = path.join(backendDir, 'venv', 'bin', 'python');

let pythonBin = 'python';
if (process.platform === 'win32' && fs.existsSync(venvPythonWin)) {
  pythonBin = venvPythonWin;
} else if (fs.existsSync(venvPythonUnix)) {
  pythonBin = venvPythonUnix;
}

const args = [
  '-m', 'uvicorn',
  'main:app',
  '--host', '127.0.0.1',
  '--port', '8000',
  '--reload'
];

console.log(`[Backend Runner] Launching FastAPI from ${backendDir} using ${pythonBin}...`);

const child = spawn(pythonBin, args, {
  cwd: backendDir,
  stdio: 'inherit',
  shell: false
});

child.on('error', (err) => {
  console.error('[Backend Runner Error]:', err.message);
});

child.on('exit', (code) => {
  process.exit(code || 0);
});
