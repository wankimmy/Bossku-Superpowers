---
description: "Casual 'what does this repo even do': an API, a queue and a worker."
tags: ["lean", "bosskuai-project-understanding", "fires", "answer"]
max_turns: 10
timeout_seconds: 300
allowed_tools: ["Skill", "Read", "Glob", "Grep"]
---

new to this repo, what does it even do and how do the pieces fit? files below

package.json:
```json
{
  "name": "pantau",
  "scripts": { "start": "node src/server.js", "worker": "node src/worker.js", "test": "vitest run" },
  "dependencies": { "express": "^4.19.0", "bullmq": "^5.7.0", "ioredis": "^5.4.0", "pg": "^8.11.0" }
}
```

src/server.js:
```js
const express = require('express');
const { Queue } = require('bullmq');
const app = express();
const checks = new Queue('uptime-checks', { connection: { host: process.env.REDIS_HOST } });
app.use(express.json());
app.post('/monitors', async (req, res) => {
  await checks.add('check', { url: req.body.url }, { repeat: { every: 60000 } });
  res.status(201).json({ ok: true });
});
app.listen(process.env.PORT || 3000);
```

src/worker.js:
```js
const { Worker } = require('bullmq');
const { Pool } = require('pg');
const db = new Pool();
new Worker('uptime-checks', async (job) => {
  const started = Date.now();
  const res = await fetch(job.data.url);
  await db.query('INSERT INTO results(url, status, ms) VALUES ($1, $2, $3)', [job.data.url, res.status, Date.now() - started]);
}, { connection: { host: process.env.REDIS_HOST } });
```
