---
description: "Modernise callbacks to async/await without silently breaking existing callers."
tags: ["lean", "bosskuai-code-revamp", "fires", "answer"]
max_turns: 10
timeout_seconds: 300
allowed_tools: ["Skill", "Read", "Glob", "Grep"]
---

we're moving this node file from callbacks to async/await. can you modernise it safely? keep the exported function names and what they return the same.

```js
const fs = require('fs');

function readConfig(path, cb) {
  fs.readFile(path, 'utf8', (err, text) => {
    if (err) return cb(err);
    let config;
    try {
      config = JSON.parse(text);
    } catch (e) {
      return cb(new Error('Invalid config: ' + e.message));
    }
    cb(null, config);
  });
}

function loadPort(path, cb) {
  readConfig(path, (err, config) => {
    if (err) return cb(err);
    cb(null, config.port || 3000);
  });
}

module.exports = { readConfig, loadPort };
```
