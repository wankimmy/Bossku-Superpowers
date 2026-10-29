---
description: "Rojak request to save a deploy lesson as a skill."
tags: ["lean", "bosskuai-learn", "fires", "answer"]
max_turns: 10
timeout_seconds: 300
allowed_tools: ["Skill", "Read", "Glob", "Grep"]
---

Boss, simpan ni as a skill untuk project ni: every time deploy staging kena run `php artisan migrate` dulu, baru `php artisan config:cache`. Last week I lost one hour sebab buat terbalik, config cache pointed to the old DB. Tak boleh run command sini, so just tunjuk intent JSON untuk `bossku learn apply`.
