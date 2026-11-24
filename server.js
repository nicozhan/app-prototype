/**
 * VendSolution 原型静态服务
 * 用于 Railway / 任意 Node 环境托管：
 *   /            入口选择页（App Demo / Web 后台）
 *   /navigation  可交互 App Demo
 *   /nav         全部页面画廊
 * 无第三方依赖，只做静态文件 + 少量路径回退。
 */
const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const { promisify } = require('node:util');

const ROOT = __dirname;
const PORT = Number(process.env.PORT) || 3000;
const HOST = process.env.HOST || '0.0.0.0';

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.htm': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.mjs': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.map': 'application/json; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.webp': 'image/webp',
  '.gif': 'image/gif',
  '.ico': 'image/x-icon',
  '.woff': 'font/woff',
  '.woff2': 'font/woff2',
  '.ttf': 'font/ttf',
  '.mp4': 'video/mp4',
  '.webm': 'video/webm',
  '.txt': 'text/plain; charset=utf-8',
  '.md': 'text/markdown; charset=utf-8'
};

/* 不对外暴露的目录/文件 */
const BLOCKED = [
  '.git', '.workbuddy', 'jpgk-platform', 'shots', 'new', 'node_modules'
];

const stat = promisify(fs.stat);
const readFile = promisify(fs.readFile);

function safeJoin(root, target) {
  const resolved = path.resolve(root, '.' + path.posix.normalize('/' + target));
  return resolved.startsWith(root + path.sep) || resolved === root ? resolved : null;
}

async function resolveFile(pathname) {
  const clean = decodeURIComponent(pathname.split('?')[0].split('#')[0]);
  if (clean.includes('\0')) return null;

  const segments = clean.split('/').filter(Boolean);
  if (segments.some((s) => BLOCKED.includes(s))) return null;

  const candidates = [];
  const base = safeJoin(ROOT, clean);
  if (!base) return null;

  if (clean.endsWith('/')) {
    candidates.push(path.join(base, 'index.html'));
  } else {
    candidates.push(base);
    if (!path.extname(clean)) {
      candidates.push(base + '.html');
      candidates.push(path.join(base, 'index.html'));
    }
  }

  for (const candidate of candidates) {
    try {
      const info = await stat(candidate);
      if (info.isFile()) return { file: candidate, size: info.size, mtime: info.mtime };
    } catch (_) {
      /* 继续尝试下一个候选 */
    }
  }
  return null;
}

function send(res, status, body, headers = {}) {
  res.writeHead(status, {
    'Content-Type': 'text/html; charset=utf-8',
    'X-Content-Type-Options': 'nosniff',
    ...headers
  });
  res.end(body);
}

const server = http.createServer(async (req, res) => {
  if (req.method !== 'GET' && req.method !== 'HEAD') {
    send(res, 405, 'Method Not Allowed', { Allow: 'GET, HEAD' });
    return;
  }

  const url = new URL(req.url || '/', `http://${req.headers.host || 'localhost'}`);

  if (url.pathname === '/healthz') {
    send(res, 200, 'ok', { 'Content-Type': 'text/plain; charset=utf-8', 'Cache-Control': 'no-store' });
    return;
  }

  let found = null;
  try {
    found = await resolveFile(url.pathname);
  } catch (_) {
    send(res, 400, 'Bad Request');
    return;
  }

  if (!found) {
    send(res, 404, `<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>404 · VendSolution</title>
<style>body{margin:0;min-height:100dvh;display:flex;flex-direction:column;align-items:center;justify-content:center;
background:#F6F7FB;color:#0B102F;font-family:-apple-system,BlinkMacSystemFont,"PingFang SC",system-ui,sans-serif;text-align:center;padding:24px}
b{font-size:56px;font-weight:800;color:#2434C8;letter-spacing:-2px}p{color:#5A6079;font-size:14px;margin:10px 0 22px}
a{display:inline-flex;align-items:center;height:42px;padding:0 18px;border-radius:11px;background:#2434C8;color:#fff;
text-decoration:none;font-size:14px;font-weight:700}</style></head>
<body><b>404</b><p>页面不存在：${url.pathname.replace(/[<>&"]/g, '')}</p><a href="/">返回入口</a></body></html>`,
      { 'Cache-Control': 'no-store' });
    return;
  }

  const ext = path.extname(found.file).toLowerCase();
  const isHtml = ext === '.html' || ext === '.htm';
  const etag = `W/"${found.size.toString(16)}-${Math.round(found.mtime.getTime() / 1000).toString(16)}"`;

  if (req.headers['if-none-match'] === etag) {
    res.writeHead(304, { ETag: etag });
    res.end();
    return;
  }

  const headers = {
    'Content-Type': MIME[ext] || 'application/octet-stream',
    'Content-Length': found.size,
    ETag: etag,
    'Cache-Control': isHtml ? 'no-cache' : 'public, max-age=3600'
  };

  if (req.method === 'HEAD') {
    res.writeHead(200, headers);
    res.end();
    return;
  }

  try {
    const data = await readFile(found.file);
    res.writeHead(200, headers);
    res.end(data);
  } catch (_) {
    send(res, 500, 'Internal Server Error', { 'Cache-Control': 'no-store' });
  }
});

server.listen(PORT, HOST, () => {
  console.log(`VendSolution prototype listening on http://${HOST}:${PORT}`);
});

const shutdown = () => server.close(() => process.exit(0));
process.on('SIGTERM', shutdown);
process.on('SIGINT', shutdown);
