# Local canonical skills / agency pack audit

Scope: read-only local pack stocktake, 2026-10-12. Source descriptions are evidence of declared scope, not proof that capabilities work. Decisions below are editorial comparisons (inferences). No upstream network verification or imports performed.

## Numbered source quotes

1. "Ask which skill or flow fits your situation. A router over the skills in" — `C:/dev/Tenant-Management-System/skills/skills/skills/engineering/ask-matt/SKILL.md:3`.
2. "Review the changes since a fixed point (commit, branch, tag, or merge-base) along two" — `C:/dev/Tenant-Management-System/skills/skills/skills/engineering/code-review/SKILL.md:3`.
3. "Shared vocabulary for designing deep modules. Use when the user wants to design or" — `C:/dev/Tenant-Management-System/skills/skills/skills/engineering/codebase-design/SKILL.md:3`.
4. "Diagnosis loop for hard bugs and performance regressions. Use when the user says "diagnose"/"debug" — `C:/dev/Tenant-Management-System/skills/skills/skills/engineering/diagnosing-bugs/SKILL.md:3`.
5. "Build and sharpen a project's domain model. Use when discussing codebase terminology, writing or" — `C:/dev/Tenant-Management-System/skills/skills/skills/engineering/domain-modeling/SKILL.md:3`.
6. "A relentless interview to sharpen a plan or design, which also creates docs (ADR's" — `C:/dev/Tenant-Management-System/skills/skills/skills/engineering/grill-with-docs/SKILL.md:3`.
7. "Implement a piece of work based on a spec or set of tickets." — `C:/dev/Tenant-Management-System/skills/skills/skills/engineering/implement/SKILL.md:3`.
8. "Implement the result of /to-spec and /to-tickets in code." — `C:/dev/Tenant-Management-System/skills/skills/skills/engineering/implement-spec/SKILL.md:3`.
9. "Scan a codebase for deepening opportunities, present them as a visual HTML report, then" — `C:/dev/Tenant-Management-System/skills/skills/skills/engineering/improve-codebase-architecture/SKILL.md:3`.
10. "Use when writing a PR body." — `C:/dev/Tenant-Management-System/skills/skills/skills/engineering/pr/SKILL.md:3`.
11. "Build a throwaway prototype to answer a design question. Use when the user wants" — `C:/dev/Tenant-Management-System/skills/skills/skills/engineering/prototype/SKILL.md:3`.
12. "Investigate a question against high-trust primary sources and capture the findings as a Markdown" — `C:/dev/Tenant-Management-System/skills/skills/skills/engineering/research/SKILL.md:3`.
13. "Conduct a retrospective on a coding session." — `C:/dev/Tenant-Management-System/skills/skills/skills/engineering/retro/SKILL.md:3`.
14. "Configure this repo for the engineering skills: set up its issue tracker, triage label" — `C:/dev/Tenant-Management-System/skills/skills/skills/engineering/setup-matt-pocock-skills/SKILL.md:3`.
15. "Test-driven development. Use when the user wants to build features or fix bugs test-first," — `C:/dev/Tenant-Management-System/skills/skills/skills/engineering/tdd/SKILL.md:3`.
16. "Turn the current conversation into a spec and publish it to the project issue" — `C:/dev/Tenant-Management-System/skills/skills/skills/engineering/to-spec/SKILL.md:3`.
17. "Break a plan, spec, or the current conversation into a set of tracer-bullet tickets," — `C:/dev/Tenant-Management-System/skills/skills/skills/engineering/to-tickets/SKILL.md:3`.
18. "Move issues and external PRs through a state machine of triage roles, categorise, verify," — `C:/dev/Tenant-Management-System/skills/skills/skills/engineering/triage/SKILL.md:3`.
19. "Plan a huge chunk of work (more than one agent session can hold) as" — `C:/dev/Tenant-Management-System/skills/skills/skills/engineering/wayfinder/SKILL.md:3`.
20. "Generate an interactive bash wizard that walks a human through steps only they can" — `C:/dev/Tenant-Management-System/skills/skills/skills/engineering/wizard/SKILL.md:3`.
21. "Pursue a long-running goal in a single session by co-ordinating subagents." — `C:/dev/Tenant-Management-System/skills/skills/skills/in-progress/chief-of-staff/SKILL.md:3`.
22. "Hand the current conversation off to a fresh background agent that picks up the" — `C:/dev/Tenant-Management-System/skills/skills/skills/in-progress/claude-handoff/SKILL.md:3`.
23. "Grill me about specs for the workflows I want to build, within this workspace." — `C:/dev/Tenant-Management-System/skills/skills/skills/in-progress/loop-me/SKILL.md:3`.
24. "Wire dependency-cruiser into a TypeScript repo so each package is a deep module, with" — `C:/dev/Tenant-Management-System/skills/skills/skills/in-progress/setup-ts-deep-modules/SKILL.md:3`.
25. "Writing, exploit; assemble raw material into a journey of beats, grounding each term before" — `C:/dev/Tenant-Management-System/skills/skills/skills/in-progress/writing-beats/SKILL.md:3`.
26. "Writing, explore: mine raw fragments, no structure yet." — `C:/dev/Tenant-Management-System/skills/skills/skills/in-progress/writing-fragments/SKILL.md:3`.
27. "Writing, exploit: shape raw material into an article, paragraph by paragraph." — `C:/dev/Tenant-Management-System/skills/skills/skills/in-progress/writing-shape/SKILL.md:3`.
28. "Set up Claude Code hooks to block dangerous git commands (push, reset --hard, clean," — `C:/dev/Tenant-Management-System/skills/skills/skills/misc/git-guardrails-claude-code/SKILL.md:3`.
29. "Migrate test files from `as` type assertions to @total-typescript/shoehorn. Use when user mentions shoehorn," — `C:/dev/Tenant-Management-System/skills/skills/skills/misc/migrate-to-shoehorn/SKILL.md:3`.
30. "Create exercise directory structures with sections, problems, solutions, and explainers that pass linting. Use" — `C:/dev/Tenant-Management-System/skills/skills/skills/misc/scaffold-exercises/SKILL.md:3`.
31. "Set up Husky pre-commit hooks with lint-staged (Prettier), type checking, and tests in the" — `C:/dev/Tenant-Management-System/skills/skills/skills/misc/setup-pre-commit/SKILL.md:3`.
32. "A relentless interview to sharpen a plan or design." — `C:/dev/Tenant-Management-System/skills/skills/skills/productivity/grill-me/SKILL.md:3`.
33. "Grill the user relentlessly about a plan, decision, or idea. Use when the user" — `C:/dev/Tenant-Management-System/skills/skills/skills/productivity/grilling/SKILL.md:3`.
34. "Compact the current conversation into a handoff document for another agent to pick up." — `C:/dev/Tenant-Management-System/skills/skills/skills/productivity/handoff/SKILL.md:3`.
35. "Teach the user a new skill or concept, within this workspace." — `C:/dev/Tenant-Management-System/skills/skills/skills/productivity/teach/SKILL.md:3`.
36. "Turn a decision you can't fully answer into a questionnaire for someone else to" — `C:/dev/Tenant-Management-System/skills/skills/skills/productivity/to-questionnaire/SKILL.md:3`.
37. "Stop. That last message did not land: re-pitch it." — `C:/dev/Tenant-Management-System/skills/skills/skills/productivity/wait-what/SKILL.md:3`.
38. "Writing documents for agents. Use when creating or editing skills, or modifying AGENTS.md or" — `C:/dev/Tenant-Management-System/skills/skills/skills/productivity/writing-for-agents/SKILL.md:3`.
39. "Expert in cultural systems, rituals, kinship, belief systems, and ethnographic method — builds culturally" — `C:/dev/Tenant-Management-System/skills/agency-agents/academic/academic-anthropologist.md:3`.
40. "Expert in physical and human geography, climate systems, cartography, and spatial analysis — builds" — `C:/dev/Tenant-Management-System/skills/agency-agents/academic/academic-geographer.md:3`.
41. "Expert in historical analysis, periodization, material culture, and historiography — validates historical coherence and" — `C:/dev/Tenant-Management-System/skills/agency-agents/academic/academic-historian.md:3`.
42. "Expert in narrative theory, story structure, character arcs, and literary analysis — grounds advice" — `C:/dev/Tenant-Management-System/skills/agency-agents/academic/academic-narratologist.md:3`.
43. "Expert in human behavior, personality theory, motivation, and cognitive patterns — builds psychologically credible" — `C:/dev/Tenant-Management-System/skills/agency-agents/academic/academic-psychologist.md:3`.
44. "Expert in quantitative research methodology, experimental design, and statistical inference — pressure-tests claims, designs" — `C:/dev/Tenant-Management-System/skills/agency-agents/academic/academic-statistician.md:3`.
45. "Expert brand strategist and guardian specializing in brand identity development, consistency maintenance, and strategic" — `C:/dev/Tenant-Management-System/skills/agency-agents/design/design-brand-guardian.md:3`.
46. "Expert photography prompt engineer specializing in crafting detailed, evocative prompts for AI image generation." — `C:/dev/Tenant-Management-System/skills/agency-agents/design/design-image-prompt-engineer.md:3`.
47. "Representation expert who defeats systemic AI biases to generate culturally accurate, affirming, and non-stereotypical" — `C:/dev/Tenant-Management-System/skills/agency-agents/design/design-inclusive-visuals-specialist.md:3`.
48. "Simulate cognitive walkthroughs of web pages from a defined persona's psychological perspective — captures" — `C:/dev/Tenant-Management-System/skills/agency-agents/design/design-persona-walkthrough.md:3`.
49. "Expert UI designer specializing in visual design systems, component libraries, and pixel-perfect interface creation." — `C:/dev/Tenant-Management-System/skills/agency-agents/design/design-ui-designer.md:3`.
50. "Product-interface reviewer who catches generic, interchangeable UI before it ships by grounding critique in" — `C:/dev/Tenant-Management-System/skills/agency-agents/design/design-ui-finish-gate-reviewer.md:3`.
51. "Technical architecture and UX specialist who provides developers with solid foundations, CSS systems, and" — `C:/dev/Tenant-Management-System/skills/agency-agents/design/design-ux-architect.md:3`.
52. "Expert user experience researcher specializing in user behavior analysis, usability testing, and data-driven design" — `C:/dev/Tenant-Management-System/skills/agency-agents/design/design-ux-researcher.md:3`.
53. "Expert visual communication specialist focused on creating compelling visual narratives, multimedia content, and brand" — `C:/dev/Tenant-Management-System/skills/agency-agents/design/design-visual-storyteller.md:3`.
54. "Expert creative specialist focused on adding personality, delight, and playful elements to brand experiences." — `C:/dev/Tenant-Management-System/skills/agency-agents/design/design-whimsy-injector.md:3`.
55. "Specialist in self-healing data pipelines — uses air-gapped local SLMs and semantic clustering to" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-ai-data-remediation-engineer.md:3`.
56. "Expert AI/ML engineer specializing in machine learning model development, deployment, and integration into production" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-ai-engineer.md:3`.
57. "Expert API platform engineer for public and partner APIs — contract-first design (OpenAPI/gRPC), versioning" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-api-platform-engineer.md:3`.
58. "Architect and validator for Applicant Tracking Systems (ATS) and resume parsers. Combines deterministic information" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-ats-validator-architect.md:3`.
59. "Intelligent system governor that continuously shadow-tests APIs for performance while enforcing strict financial and" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-autonomous-optimization-architect.md:3`.
60. "Senior backend architect specializing in scalable system design, database architecture, API development, and cloud" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-backend-architect.md:3`.
61. "Expert in mainland China's mainstream enterprise networking stacks — Huawei VRP, H3C Comware, Ruijie" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-china-network-engineer.md:3`.
62. "Drupal and WordPress specialist for theme development, custom plugins/modules, content architecture, and code-first CMS" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-cms-developer.md:4`.
63. "Expert code reviewer who provides constructive, actionable feedback focused on correctness, maintainability, security, and" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-code-reviewer.md:3`.
64. "Expert developer onboarding specialist who helps new engineers understand unfamiliar codebases fast by reading" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-codebase-onboarding-engineer.md:3`.
65. "Expert data engineer specializing in building reliable data pipelines, lakehouse architectures, and scalable data" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-data-engineer.md:3`.
66. "Expert data visualization engineer — chart-type selection by data and question, perceptually honest encodings," — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-data-visualization-engineer.md:3`.
67. "Expert database specialist focusing on schema design, query optimization, indexing strategies, and performance tuning" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-database-optimizer.md:3`.
68. "Expert database reliability engineer (DBRE) — high availability and replication, automated failover, backup and" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-database-reliability-engineer.md:3`.
69. "Expert desktop application engineer for Electron and Tauri — secure IPC and process isolation," — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-desktop-app-engineer.md:3`.
70. "Expert developer-tooling and CLI engineer — building command-line tools and internal developer platforms with" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-developer-tooling-engineer.md:3`.
71. "Expert DevOps engineer specializing in infrastructure automation, CI/CD pipeline development, and cloud operations" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-devops-automator.md:3`.
72. "Expert Drupal 10/11 performance engineer specializing in Core Web Vitals, render and dynamic page" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-drupal-performance.md:4`.
73. "Expert Drupal e-commerce engineer specializing in Drupal Commerce for product catalog management, payment gateway" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-drupal-shopping-cart.md:4`.
74. "Expert in extracting structured, reasoning-ready data from raw email threads for AI agents and" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-email-intelligence-engineer.md:3`.
75. "Specialist in bare-metal and RTOS firmware - ESP32/ESP-IDF, PlatformIO, Arduino, ARM Cortex-M, STM32 HAL/LL," — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-embedded-firmware-engineer.md:3`.
76. "Full-stack integration expert specializing in the Feishu (Lark) Open Platform — proficient in Feishu" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-feishu-integration-developer.md:3`.
77. "Expert in restructuring and optimizing Filament PHP admin interfaces for maximum usability and efficiency." — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-filament-optimization-specialist.md:3`.
78. "Expert cloud cost engineer for AWS/GCP/Azure — cost allocation and tagging, rightsizing, commitment planning" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-finops-engineer.md:3`.
79. "Expert frontend developer specializing in modern web technologies, React/Vue/Angular frameworks, UI implementation, and performance" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-frontend-developer.md:3`.
80. "Expert database specialist focusing on GaussDB OLTP — Huawei's self-developed enterprise-grade relational database (NOT" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-gaussdb-expert.md:3`.
81. "Expert in Git workflows, branching strategies, and version control best practices including conventional commits," — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-git-workflow-master.md:3`.
82. "Expert i18n engineer for ICU MessageFormat, CLDR plural rules, RTL and bidirectional layouts, locale-aware" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-i18n-engineer.md:3`.
83. "Expert identity engineer for OAuth 2.0/OIDC flows, enterprise SSO (SAML/OIDC) and SCIM provisioning, passkeys/WebAuthn," — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-identity-access-engineer.md:3`.
84. "Expert incident commander specializing in production incident management, structured response coordination, post-mortem facilitation, SLO/SLI" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-incident-response-commander.md:3`.
85. "Expert IoT and edge fleet engineer — device provisioning and identity, MQTT/telemetry pipelines, staged" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-iot-fleet-engineer.md:3`.
86. "Expert IT service management specialist using ITIL 4 framework for service catalog design, incident" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-it-service-manager.md:4`.
87. "Structures information and capabilities into interconnected nodes (entities) and edges (relationships) — enabling dynamic" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-knowledge-graph-engineer.md:4`.
88. "Evidence-driven owner for SFT, preference optimization, RLHF/RLVR, MoE post-training, and the release gates that" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-llm-post-training-engineer.md:3`.
89. "Engineering specialist focused on minimum-viable diffs — fixes only what was asked, refuses scope" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-minimal-change-engineer.md:3`.
90. "Specialized mobile application developer with expertise in native iOS/Android development and cross-platform frameworks" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-mobile-app-builder.md:3`.
91. "Expert mobile release and distribution engineer for iOS and Android — code signing, provisioning," — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-mobile-release-engineer.md:3`.
92. "Systems architect specializing in the design, coordination, and governance of multi-agent AI pipelines —" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-multi-agent-systems-architect.md:4`.
93. "Expert network engineer for Cisco IOS/IOS-XE, Cisco ASA/FTD, Juniper Junos, and Palo Alto PAN-OS" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-network-engineer.md:3`.
94. "Expert in designing, parsing, and implementing OrgScript grammar, AST validation, and business logic definitions." — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-orgscript-engineer.md:3`.
95. "Expert payments engineer for PSP integrations (Stripe, Adyen, Braintree, PayPal), idempotent payment flows, webhook" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-payments-billing-engineer.md:3`.
96. "Architect and specialist in deterministic HTML-to-PDF document compilation, Playwright browser context pools, dynamic Euclidean" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-pdf-engine-architect.md:3`.
97. "Expert internal developer platform (IDP) engineer specializing in golden paths, paved roads, and self-serve" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-platform-engineer.md:3`.
98. "Expert privacy engineer who implements privacy in code — PII discovery and classification, data" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-privacy-engineer.md:3`.
99. "Specialist in crafting, testing, and systematically optimizing prompts for LLMs — turning vague instructions" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-prompt-engineer.md:3`.
100. "Production RAG specialist focused on chunking strategy, retrieval quality, hybrid search, re-ranking, and eval-driven" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-rag-pipeline-engineer.md:3`.
101. "Specialized in ultra-fast proof-of-concept development and MVP creation using efficient tools and frameworks" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-rapid-prototyper.md:3`.
102. "Expert realtime systems engineer for WebSocket/SSE infrastructure, presence, CRDT and OT-based collaborative editing, offline-first" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-realtime-collaboration-engineer.md:3`.
103. "Expert Rust engineer for repository-scale refactoring, safe renames, module restructuring, duplication removal, panic hardening," — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-rust-refactoring-specialist.md:3`.
104. "Expert search engineer for Elasticsearch and OpenSearch — index and analyzer design, BM25 query" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-search-relevance-engineer.md:3`.
105. "Expert U.S. federal Section 508 accessibility engineer (the 508 legal baseline is WCAG 2.0" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-section-508-specialist.md:4`.
106. "Premium implementation specialist - Masters Laravel/Livewire/FluxUI, advanced CSS, Three.js integration" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-senior-developer.md:3`.
107. "ServiceNow platform developer and step-by-step troubleshooter — Business Rules, Script Includes, GlideRecord/GlideAggregate, Flow Designer," — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-servicenow-developer-mentor.md:3`.
108. "Expert software architect specializing in system design, domain-driven design, architectural patterns, and technical decision-making" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-software-architect.md:3`.
109. "Expert Solidity developer specializing in EVM smart contract architecture, gas optimization, upgradeable proxy patterns," — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-solidity-smart-contract-engineer.md:3`.
110. "Expert site reliability engineer specializing in SLOs, error budgets, observability, chaos engineering, and toil" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-sre.md:3`.
111. "Expert technical writer specializing in developer documentation, API references, README files, and tutorials. Transforms" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-technical-writer.md:3`.
112. "Architect of schema-agnostic document ASTs, algorithmic data-shape layout inference, bidirectional CST-to-canvas synchronization, and universal" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-universal-document-compiler.md:3`.
113. "Expert U.S. Web Design System frontend developer specializing in USWDS components and design tokens," — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-uswds-developer.md:4`.
114. "Expert video streaming engineer for adaptive bitrate delivery — HLS/DASH packaging, ffmpeg transcode ladders," — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-video-streaming-engineer.md:3`.
115. "Expert in building end-to-end speech transcription pipelines using Whisper-style models and cloud ASR services" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-voice-ai-integration-engineer.md:4`.
116. "Expert WebAssembly engineer — compiling Rust/C++/Go to Wasm, JS interop and the boundary marshalling" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-webassembly-engineer.md:3`.
117. "Expert WeChat Mini Program developer specializing in 小程序 development with WXML/WXSS/WXS, WeChat API integration," — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-wechat-mini-program-developer.md:3`.
118. "Expert WordPress performance engineer specializing in Core Web Vitals, object caching (Redis/Memcached), page caching," — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-wordpress-performance.md:4`.
119. "Expert WordPress e-commerce engineer specializing in WooCommerce for product catalog management, payment gateway integration," — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-wordpress-shopping-cart.md:4`.
120. "Expert bookkeeper and controller specializing in day-to-day accounting operations, financial reconciliations, month-end close processes," — `C:/dev/Tenant-Management-System/skills/agency-agents/finance/finance-bookkeeper-controller.md:3`.
121. "Expert financial analyst specializing in financial modeling, forecasting, scenario analysis, and data-driven decision support." — `C:/dev/Tenant-Management-System/skills/agency-agents/finance/finance-financial-analyst.md:3`.
122. "Expert Financial Planning & Analysis (FP&A) analyst specializing in budgeting, variance analysis, financial planning," — `C:/dev/Tenant-Management-System/skills/agency-agents/finance/finance-fpa-analyst.md:3`.
123. "Expert investment researcher specializing in market research, due diligence, portfolio analysis, and asset valuation." — `C:/dev/Tenant-Management-System/skills/agency-agents/finance/finance-investment-researcher.md:3`.
124. "Expert tax strategist specializing in tax optimization, multi-jurisdictional compliance, transfer pricing, and strategic tax" — `C:/dev/Tenant-Management-System/skills/agency-agents/finance/finance-tax-strategist.md:3`.
125. "Blender tooling specialist - Builds Python add-ons, asset validators, exporters, and pipeline automations that" — `C:/dev/Tenant-Management-System/skills/agency-agents/game-development/blender/blender-addon-engineer.md:3`.
126. "Virtual economy architect - Masters currency systems, sources and sinks, monetization modeling, inflation control," — `C:/dev/Tenant-Management-System/skills/agency-agents/game-development/economy-designer.md:3`.
127. "Interactive audio specialist - Masters FMOD/Wwise integration, adaptive music systems, spatial audio, and audio" — `C:/dev/Tenant-Management-System/skills/agency-agents/game-development/game-audio-engineer.md:3`.
128. "Systems and mechanics architect - Masters GDD authorship, player psychology, economy balancing, and gameplay" — `C:/dev/Tenant-Management-System/skills/agency-agents/game-development/game-designer.md:3`.
129. "Composition and signal integrity specialist - Masters GDScript 2.0, C# integration, node-based architecture, and" — `C:/dev/Tenant-Management-System/skills/agency-agents/game-development/godot/godot-gameplay-scripter.md:3`.
130. "Godot 4 networking specialist - Masters the MultiplayerAPI, scene replication, ENet/WebRTC transport, RPCs, and" — `C:/dev/Tenant-Management-System/skills/agency-agents/game-development/godot/godot-multiplayer-engineer.md:3`.
131. "Godot 4 visual effects specialist - Masters the Godot Shading Language (GLSL-like), VisualShader editor," — `C:/dev/Tenant-Management-System/skills/agency-agents/game-development/godot/godot-shader-developer.md:3`.
132. "Spatial storytelling and flow specialist - Masters layout theory, pacing architecture, encounter design, and" — `C:/dev/Tenant-Management-System/skills/agency-agents/game-development/level-designer.md:3`.
133. "Story systems and dialogue architect - Masters GDD-aligned narrative design, branching dialogue, lore architecture," — `C:/dev/Tenant-Management-System/skills/agency-agents/game-development/narrative-designer.md:3`.
134. "Roblox UGC and avatar pipeline specialist - Masters Roblox's avatar system, UGC item creation," — `C:/dev/Tenant-Management-System/skills/agency-agents/game-development/roblox-studio/roblox-avatar-creator.md:3`.
135. "Roblox platform UX and monetization specialist - Masters engagement loop design, DataStore-driven progression, Roblox" — `C:/dev/Tenant-Management-System/skills/agency-agents/game-development/roblox-studio/roblox-experience-designer.md:3`.
136. "Roblox platform engineering specialist - Masters Luau, the client-server security model, RemoteEvents/RemoteFunctions, DataStore, and" — `C:/dev/Tenant-Management-System/skills/agency-agents/game-development/roblox-studio/roblox-systems-scripter.md:3`.
137. "Art-to-engine pipeline specialist - Masters shaders, VFX systems, LOD pipelines, performance budgeting, and cross-engine" — `C:/dev/Tenant-Management-System/skills/agency-agents/game-development/technical-artist.md:3`.
138. "Data-driven modularity specialist - Masters ScriptableObjects, decoupled systems, and single-responsibility component design for scalable" — `C:/dev/Tenant-Management-System/skills/agency-agents/game-development/unity/unity-architect.md:3`.
139. "Unity editor automation specialist - Masters custom EditorWindows, PropertyDrawers, AssetPostprocessors, ScriptedImporters, and pipeline automation" — `C:/dev/Tenant-Management-System/skills/agency-agents/game-development/unity/unity-editor-tool-developer.md:3`.
140. "Networked gameplay specialist - Masters Netcode for GameObjects, Unity Gaming Services (Relay/Lobby), client-server authority," — `C:/dev/Tenant-Management-System/skills/agency-agents/game-development/unity/unity-multiplayer-engineer.md:3`.
141. "Visual effects and material specialist - Masters Unity Shader Graph, HLSL, URP/HDRP rendering pipelines," — `C:/dev/Tenant-Management-System/skills/agency-agents/game-development/unity/unity-shader-graph-artist.md:3`.
142. "Unreal Engine networking specialist - Masters Actor replication, GameMode/GameState architecture, server-authoritative gameplay, network prediction," — `C:/dev/Tenant-Management-System/skills/agency-agents/game-development/unreal-engine/unreal-multiplayer-architect.md:3`.
143. "Performance and hybrid architecture specialist - Masters C++/Blueprint continuum, Nanite geometry, Lumen GI, and" — `C:/dev/Tenant-Management-System/skills/agency-agents/game-development/unreal-engine/unreal-systems-engineer.md:3`.
144. "Unreal Engine visual pipeline specialist - Masters the Material Editor, Niagara VFX, Procedural Content" — `C:/dev/Tenant-Management-System/skills/agency-agents/game-development/unreal-engine/unreal-technical-artist.md:3`.
145. "Open-world and environment specialist - Masters UE5 World Partition, Landscape, procedural foliage, HLOD, and" — `C:/dev/Tenant-Management-System/skills/agency-agents/game-development/unreal-engine/unreal-world-builder.md:3`.
146. "Web 3D visualization specialist who creates immersive 3D scenes, terrain models, point cloud visualizations," — `C:/dev/Tenant-Management-System/skills/agency-agents/gis/gis-3d-scene-developer.md:3`.
147. "Day-to-day GIS operator who creates maps, manages layers, performs spatial queries, and maintains geospatial" — `C:/dev/Tenant-Management-System/skills/agency-agents/gis/gis-analyst.md:3`.
148. "Integration specialist who bridges Building Information Modeling and Geographic Information Systems — Revit/IFC data" — `C:/dev/Tenant-Management-System/skills/agency-agents/gis/gis-bim-specialist.md:3`.
149. "Map aesthetics specialist who designs beautiful, readable, and effective maps — color theory, typography," — `C:/dev/Tenant-Management-System/skills/agency-agents/gis/gis-cartography-designer.md:3`.
150. "Photogrammetry and reality capture expert who processes drone imagery into orthomosaics, digital terrain models," — `C:/dev/Tenant-Management-System/skills/agency-agents/gis/gis-drone-reality-mapping.md:3`.
151. "Geospatial machine learning specialist who builds models for feature extraction, object detection, image segmentation," — `C:/dev/Tenant-Management-System/skills/agency-agents/gis/gis-geoai-ml-engineer.md:3`.
152. "ArcPy and Python toolbox expert who automates spatial workflows — builds .pyt toolboxes, Model" — `C:/dev/Tenant-Management-System/skills/agency-agents/gis/gis-geoprocessing-specialist.md:3`.
153. "Quality assurance specialist who validates geospatial data integrity — topology checks, metadata audits, CRS" — `C:/dev/Tenant-Management-System/skills/agency-agents/gis/gis-qa-engineer.md:3`.
154. "Hands-on GIS prototype builder who takes strategy from Technical Consultant and turns it into" — `C:/dev/Tenant-Management-System/skills/agency-agents/gis/gis-solution-engineer.md:3`.
155. "ETL specialist who transforms messy geospatial data from any source into clean, standardized, production-ready" — `C:/dev/Tenant-Management-System/skills/agency-agents/gis/gis-spatial-data-engineer.md:3`.
156. "Advanced spatial analytics specialist who applies statistical modeling, spatial econometrics, clustering, and predictive analytics" — `C:/dev/Tenant-Management-System/skills/agency-agents/gis/gis-spatial-data-scientist.md:3`.
157. "Strategic GIS advisor who translates business problems into geospatial solutions — gap analysis, technology" — `C:/dev/Tenant-Management-System/skills/agency-agents/gis/gis-technical-consultant.md:3`.
158. "Full-stack web GIS engineer who builds interactive mapping applications — MapLibre GL JS, ArcGIS" — `C:/dev/Tenant-Management-System/skills/agency-agents/gis/gis-web-gis-developer.md:3`.
159. "Evidence standards and clinical credibility framework for AI agents" — `C:/dev/Tenant-Management-System/skills/agency-agents/healthcare/healthcare-clinical-evidence-agent.md:3`.
160. "Strategic narrative architect for healthcare founders operating at" — `C:/dev/Tenant-Management-System/skills/agency-agents/healthcare/healthcare-innovation-strategist.md:3`.
161. "Government health mandate engagement framework for AI agents" — `C:/dev/Tenant-Management-System/skills/agency-agents/healthcare/healthcare-sovereign-health-systems-agent.md:3`.
162. "Expert in AI Engine Optimization infrastructure — implements llms.txt, AI-aware robots.txt, token-budgeted content, structured" — `C:/dev/Tenant-Management-System/skills/agency-agents/marketing/marketing-aeo-foundations.md:3`.
163. "Expert in WebMCP readiness and agentic task completion — audits whether AI agents can" — `C:/dev/Tenant-Management-System/skills/agency-agents/marketing/marketing-agentic-search-optimizer.md:3`.
164. "Expert in AI recommendation engine optimization (AEO/GEO) — audits brand visibility across ChatGPT, Claude," — `C:/dev/Tenant-Management-System/skills/agency-agents/marketing/marketing-ai-citation-strategist.md:3`.
165. "Expert app store marketing specialist focused on App Store Optimization (ASO), conversion rate optimization," — `C:/dev/Tenant-Management-System/skills/agency-agents/marketing/marketing-app-store-optimizer.md:3`.
166. "Expert Baidu search optimization specialist focused on Chinese search engine ranking, Baidu ecosystem integration," — `C:/dev/Tenant-Management-System/skills/agency-agents/marketing/marketing-baidu-seo-specialist.md:3`.
167. "Expert Bilibili marketing specialist focused on UP主 growth, danmaku culture mastery, B站 algorithm optimization," — `C:/dev/Tenant-Management-System/skills/agency-agents/marketing/marketing-bilibili-content-strategist.md:3`.
168. "Strategic thought-leadership book collaborator for founders, experts, and operators turning voice notes, fragments, and" — `C:/dev/Tenant-Management-System/skills/agency-agents/marketing/marketing-book-co-author.md:3`.
169. "Autonomous TikTok and Instagram carousel generation specialist. Analyzes any website URL with Playwright, generates" — `C:/dev/Tenant-Management-System/skills/agency-agents/marketing/marketing-carousel-growth-engine.md:3`.
170. "Expert China e-commerce operations specialist covering Taobao, Tmall, Pinduoduo, and JD ecosystems with deep" — `C:/dev/Tenant-Management-System/skills/agency-agents/marketing/marketing-china-ecommerce-operator.md:3`.
171. "Full-stack China market localization expert who transforms real-time trend signals into executable go-to-market strategies" — `C:/dev/Tenant-Management-System/skills/agency-agents/marketing/marketing-china-market-localization-strategist.md:3`.
172. "Expert content strategist and creator for multi-platform campaigns. Develops editorial calendars, creates compelling copy," — `C:/dev/Tenant-Management-System/skills/agency-agents/marketing/marketing-content-creator.md:3`.
173. "Full-funnel cross-border e-commerce strategist covering Amazon, Shopee, Lazada, AliExpress, Temu, and TikTok Shop operations," — `C:/dev/Tenant-Management-System/skills/agency-agents/marketing/marketing-cross-border-ecommerce.md:3`.
174. "Grows and sustains developer communities — Discord servers, GitHub discussions, forums, and contributor programs" — `C:/dev/Tenant-Management-System/skills/agency-agents/marketing/marketing-developer-community-builder.md:3`.
175. "Short-video marketing expert specializing in the Douyin platform, with deep expertise in recommendation algorithm" — `C:/dev/Tenant-Management-System/skills/agency-agents/marketing/marketing-douyin-strategist.md:3`.
176. "Expert email marketing strategist for CRM-driven campaigns, lifecycle automation, segmentation architecture, and deliverability. Designs" — `C:/dev/Tenant-Management-System/skills/agency-agents/marketing/marketing-email-strategist.md:3`.
177. "Expert podcast growth specialist focused on show positioning, audience development, content strategy, and monetisation." — `C:/dev/Tenant-Management-System/skills/agency-agents/marketing/marketing-global-podcast-strategist.md:3`.
178. "Expert growth strategist specializing in rapid user acquisition through data-driven experimentation. Develops viral loops," — `C:/dev/Tenant-Management-System/skills/agency-agents/marketing/marketing-growth-hacker.md:3`.
179. "Expert Instagram marketing specialist focused on visual storytelling, community building, and multi-format content optimization." — `C:/dev/Tenant-Management-System/skills/agency-agents/marketing/marketing-instagram-curator.md:3`.
180. "Expert Kuaishou marketing strategist specializing in short-video content for China's lower-tier city markets, live" — `C:/dev/Tenant-Management-System/skills/agency-agents/marketing/marketing-kuaishou-strategist.md:3`.
181. "Expert LinkedIn content strategist focused on thought leadership, personal brand building, and high-engagement professional" — `C:/dev/Tenant-Management-System/skills/agency-agents/marketing/marketing-linkedin-content-creator.md:3`.
182. "Veteran livestream e-commerce coach specializing in host training and live room operations across Douyin," — `C:/dev/Tenant-Management-System/skills/agency-agents/marketing/marketing-livestream-commerce-coach.md:3`.
183. "Expert orchestrator for one-click Chinese blog publishing. Routes a single article to 知乎 /" — `C:/dev/Tenant-Management-System/skills/agency-agents/marketing/marketing-multi-platform-publisher.md:3`.
184. "Content strategy and operations expert for the Chinese podcast market, with deep expertise in" — `C:/dev/Tenant-Management-System/skills/agency-agents/marketing/marketing-podcast-strategist.md:3`.
185. "Strategic public relations and communications specialist for media relations, press releases, crisis communications, executive" — `C:/dev/Tenant-Management-System/skills/agency-agents/marketing/marketing-pr-communications-manager.md:4`.
186. "Expert in building enterprise WeChat (WeCom) private domain ecosystems, with deep expertise in SCRM" — `C:/dev/Tenant-Management-System/skills/agency-agents/marketing/marketing-private-domain-operator.md:3`.
187. "Expert Reddit marketing specialist focused on authentic community engagement, value-driven content creation, and long-term" — `C:/dev/Tenant-Management-System/skills/agency-agents/marketing/marketing-reddit-community-builder.md:3`.
188. "Expert search engine optimization strategist specializing in technical SEO, content optimization, link authority building," — `C:/dev/Tenant-Management-System/skills/agency-agents/marketing/marketing-seo-specialist.md:3`.
189. "Hands-on short-video editing coach covering the full post-production pipeline, with mastery of CapCut Pro," — `C:/dev/Tenant-Management-System/skills/agency-agents/marketing/marketing-short-video-editing-coach.md:3`.
190. "Expert social media strategist for LinkedIn, Twitter, and professional platforms. Creates cross-platform campaigns, builds" — `C:/dev/Tenant-Management-System/skills/agency-agents/marketing/marketing-social-media-strategist.md:3`.
191. "Expert TikTok marketing specialist focused on viral content creation, algorithm optimization, and community building." — `C:/dev/Tenant-Management-System/skills/agency-agents/marketing/marketing-tiktok-strategist.md:3`.
192. "Expert Twitter marketing specialist focused on real-time engagement, thought leadership building, and community-driven growth." — `C:/dev/Tenant-Management-System/skills/agency-agents/marketing/marketing-twitter-engager.md:3`.
193. "Video marketing strategist specializing in YouTube algorithm optimization, audience retention, chaptering, thumbnail concepts, and" — `C:/dev/Tenant-Management-System/skills/agency-agents/marketing/marketing-video-optimization-specialist.md:3`.
194. "Expert WeChat Official Account (OA) strategist specializing in content marketing, subscriber engagement, and conversion" — `C:/dev/Tenant-Management-System/skills/agency-agents/marketing/marketing-wechat-official-account.md:3`.
195. "Full-spectrum operations expert for Sina Weibo, with deep expertise in trending topic mechanics, Super" — `C:/dev/Tenant-Management-System/skills/agency-agents/marketing/marketing-weibo-strategist.md:3`.
196. "Social intelligence specialist for X/Twitter research, trend detection, account monitoring, and evidence-backed audience insights" — `C:/dev/Tenant-Management-System/skills/agency-agents/marketing/marketing-x-twitter-intelligence-analyst.md:3`.
197. "Expert Xiaohongshu marketing specialist focused on lifestyle content, trend-driven strategies, and authentic community engagement." — `C:/dev/Tenant-Management-System/skills/agency-agents/marketing/marketing-xiaohongshu-specialist.md:3`.
198. "Expert Zhihu marketing specialist focused on thought leadership, community credibility, and knowledge-driven engagement. Masters" — `C:/dev/Tenant-Management-System/skills/agency-agents/marketing/marketing-zhihu-strategist.md:3`.
199. "Comprehensive paid media auditor who systematically evaluates Google Ads, Microsoft Ads, and Meta accounts" — `C:/dev/Tenant-Management-System/skills/agency-agents/paid-media/paid-media-auditor.md:3`.
200. "Paid media creative specialist focused on ad copywriting, RSA optimization, asset group design, and" — `C:/dev/Tenant-Management-System/skills/agency-agents/paid-media/paid-media-creative-strategist.md:3`.
201. "Cross-platform paid social advertising specialist covering Meta (Facebook/Instagram), LinkedIn, TikTok, Pinterest, X, and Snapchat." — `C:/dev/Tenant-Management-System/skills/agency-agents/paid-media/paid-media-paid-social-strategist.md:3`.
202. "Senior paid media strategist specializing in large-scale search, shopping, and performance max campaign architecture" — `C:/dev/Tenant-Management-System/skills/agency-agents/paid-media/paid-media-ppc-strategist.md:3`.
203. "Display advertising and programmatic media buying specialist covering managed placements, Google Display Network, DV360," — `C:/dev/Tenant-Management-System/skills/agency-agents/paid-media/paid-media-programmatic-buyer.md:3`.
204. "Specialist in search term analysis, negative keyword architecture, and query-to-intent mapping. Turns raw search" — `C:/dev/Tenant-Management-System/skills/agency-agents/paid-media/paid-media-search-query-analyst.md:3`.
205. "Expert in conversion tracking architecture, tag management, and attribution modeling across Google Tag Manager," — `C:/dev/Tenant-Management-System/skills/agency-agents/paid-media/paid-media-tracking-specialist.md:3`.
206. "Behavioral psychology specialist that adapts software interaction cadences and styles to maximize user motivation" — `C:/dev/Tenant-Management-System/skills/agency-agents/product/product-behavioral-nudge-engine.md:3`.
207. "Removes every unnecessary step between a developer and their first success — SDK samples," — `C:/dev/Tenant-Management-System/skills/agency-agents/product/product-dx-engineer.md:3`.
208. "Expert in collecting, analyzing, and synthesizing user feedback from multiple channels to extract actionable" — `C:/dev/Tenant-Management-System/skills/agency-agents/product/product-feedback-synthesizer.md:3`.
209. "Holistic product leader who owns the full product lifecycle — from discovery and strategy" — `C:/dev/Tenant-Management-System/skills/agency-agents/product/product-manager.md:3`.
210. "Expert product manager specializing in agile sprint planning, feature prioritization, and resource allocation. Focused" — `C:/dev/Tenant-Management-System/skills/agency-agents/product/product-sprint-prioritizer.md:3`.
211. "Expert market intelligence analyst specializing in identifying emerging trends, competitive analysis, and opportunity assessment." — `C:/dev/Tenant-Management-System/skills/agency-agents/product/product-trend-researcher.md:3`.
212. "Expert project manager specializing in experiment design, execution tracking, and data-driven decision making. Focused" — `C:/dev/Tenant-Management-System/skills/agency-agents/project-management/project-management-experiment-tracker.md:3`.
213. "Expert delivery operations specialist who enforces Jira-linked Git workflows, traceable commits, structured pull requests," — `C:/dev/Tenant-Management-System/skills/agency-agents/project-management/project-management-jira-workflow-steward.md:3`.
214. "Extract structured decisions, action items, and open questions from meeting transcripts or rough notes" — `C:/dev/Tenant-Management-System/skills/agency-agents/project-management/project-management-meeting-notes-specialist.md:3`.
215. "Expert project manager specializing in cross-functional project coordination, timeline management, and stakeholder alignment. Focused" — `C:/dev/Tenant-Management-System/skills/agency-agents/project-management/project-management-project-shepherd.md:3`.
216. "Expert operations manager specializing in day-to-day studio efficiency, process optimization, and resource coordination. Focused" — `C:/dev/Tenant-Management-System/skills/agency-agents/project-management/project-management-studio-operations.md:3`.
217. "Senior strategic leader specializing in high-level creative and technical project orchestration, resource allocation, and" — `C:/dev/Tenant-Management-System/skills/agency-agents/project-management/project-management-studio-producer.md:3`.
218. "Converts specs to tasks and remembers previous projects. Focused on realistic scope, no background" — `C:/dev/Tenant-Management-System/skills/agency-agents/project-management/project-manager-senior.md:3`.
219. "Expert in literature review, source evaluation, and evidence synthesis — turns a scattered pile" — `C:/dev/Tenant-Management-System/skills/agency-agents/research/research-synthesist.md:3`.
220. "Expert post-sale account strategist specializing in land-and-expand execution, stakeholder mapping, QBR facilitation, and net" — `C:/dev/Tenant-Management-System/skills/agency-agents/sales/sales-account-strategist.md:3`.
221. "Expert sales coaching specialist focused on rep development, pipeline review facilitation, call coaching, deal" — `C:/dev/Tenant-Management-System/skills/agency-agents/sales/sales-coach.md:3`.
222. "Senior deal strategist specializing in MEDDPICC qualification, competitive positioning, and win planning for complex" — `C:/dev/Tenant-Management-System/skills/agency-agents/sales/sales-deal-strategist.md:3`.
223. "Coaches sales teams on elite discovery methodology — question design, current-state mapping, gap quantification," — `C:/dev/Tenant-Management-System/skills/agency-agents/sales/sales-discovery-coach.md:3`.
224. "Senior pre-sales engineer specializing in technical discovery, demo engineering, POC scoping, competitive battlecards, and" — `C:/dev/Tenant-Management-System/skills/agency-agents/sales/sales-engineer.md:3`.
225. "Top-of-funnel architect who designs irresistible offers and lead magnets that attract qualified buyers at" — `C:/dev/Tenant-Management-System/skills/agency-agents/sales/sales-offer-lead-gen-strategist.md:3`.
226. "Signal-based outbound specialist who designs multi-channel prospecting sequences, defines ICPs, and builds pipeline through" — `C:/dev/Tenant-Management-System/skills/agency-agents/sales/sales-outbound-strategist.md:3`.
227. "Revenue operations analyst specializing in pipeline health diagnostics, deal velocity analysis, forecast accuracy, and" — `C:/dev/Tenant-Management-System/skills/agency-agents/sales/sales-pipeline-analyst.md:3`.
228. "Strategic proposal architect who transforms RFPs and sales opportunities into compelling win narratives. Specializes" — `C:/dev/Tenant-Management-System/skills/agency-agents/sales/sales-proposal-strategist.md:3`.
229. "Security reviewer for AI-generated and vibe-coded apps — hunts the hardcoded secrets, broken row-level" — `C:/dev/Tenant-Management-System/skills/agency-agents/security/security-ai-generated-code-auditor.md:3`.
230. "AppSec specialist who secures the software development lifecycle through threat modeling, secure code review," — `C:/dev/Tenant-Management-System/skills/agency-agents/security/security-appsec-engineer.md:3`.
231. "Expert security architect specializing in threat modeling, secure-by-design architecture, trust-boundary analysis, defense-in-depth, and risk-based" — `C:/dev/Tenant-Management-System/skills/agency-agents/security/security-architect.md:3`.
232. "Expert smart contract security auditor specializing in vulnerability detection, formal verification, exploit analysis, and" — `C:/dev/Tenant-Management-System/skills/agency-agents/security/security-blockchain-security-auditor.md:3`.
233. "Cloud-native security specialist designing zero trust architectures, implementing defense-in-depth across AWS, Azure, and GCP," — `C:/dev/Tenant-Management-System/skills/agency-agents/security/security-cloud-security-architect.md:3`.
234. "Expert technical compliance auditor specializing in SOC 2, ISO 27001, HIPAA, and PCI-DSS audits" — `C:/dev/Tenant-Management-System/skills/agency-agents/security/security-compliance-auditor.md:3`.
235. "Digital forensics and incident response specialist who leads breach investigations, contains active threats, coordinates" — `C:/dev/Tenant-Management-System/skills/agency-agents/security/security-incident-responder.md:3`.
236. "Offensive security specialist conducting authorized penetration tests, red team operations, and vulnerability assessments across" — `C:/dev/Tenant-Management-System/skills/agency-agents/security/security-penetration-tester.md:3`.
237. "Owns the full lifecycle of secrets and credentials — detection, prevention, vaulting, rotation, and" — `C:/dev/Tenant-Management-System/skills/agency-agents/security/security-secrets-credential-engineer.md:3`.
238. "Defensive application security specialist who scans every code submission for secrets and sensitive data" — `C:/dev/Tenant-Management-System/skills/agency-agents/security/security-senior-secops.md:3`.
239. "Expert detection engineer specializing in SIEM rule development, MITRE ATT&CK coverage mapping, threat hunting," — `C:/dev/Tenant-Management-System/skills/agency-agents/security/security-threat-detection-engineer.md:3`.
240. "Cyber threat intelligence specialist who tracks adversary groups, maps attack campaigns to MITRE ATT&CK," — `C:/dev/Tenant-Management-System/skills/agency-agents/security/security-threat-intelligence-analyst.md:3`.
241. "Native Swift and Metal specialist building high-performance 3D rendering systems and spatial computing experiences" — `C:/dev/Tenant-Management-System/skills/agency-agents/spatial-computing/macos-spatial-metal-engineer.md:3`.
242. "Terminal emulation, text rendering optimization, and SwiftTerm integration for modern Swift applications" — `C:/dev/Tenant-Management-System/skills/agency-agents/spatial-computing/terminal-integration-specialist.md:3`.
243. "Native visionOS spatial computing, SwiftUI volumetric interfaces, and Liquid Glass design implementation" — `C:/dev/Tenant-Management-System/skills/agency-agents/spatial-computing/visionos-spatial-engineer.md:3`.
244. "Specialist in designing and developing immersive cockpit-based control systems for XR environments" — `C:/dev/Tenant-Management-System/skills/agency-agents/spatial-computing/xr-cockpit-interaction-specialist.md:3`.
245. "Expert WebXR and immersive technology developer with specialization in browser-based AR/VR/XR applications" — `C:/dev/Tenant-Management-System/skills/agency-agents/spatial-computing/xr-immersive-developer.md:3`.
246. "Spatial interaction designer and interface strategist for immersive AR/VR/XR environments" — `C:/dev/Tenant-Management-System/skills/agency-agents/spatial-computing/xr-interface-architect.md:3`.
247. "Autonomous payment processing specialist that executes vendor payments, contractor invoices, and recurring bills across" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/accounts-payable-agent.md:3`.
248. "Designs identity, authentication, and trust verification systems for autonomous AI agents operating in multi-agent" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/agentic-identity-trust.md:3`.
249. "Autonomous pipeline manager that orchestrates the entire development workflow. You are the leader of" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/agents-orchestrator.md:3`.
250. "Governance-first architect for business automations (n8n-first) who audits value, risk, and maintainability before implementation." — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/automation-governance-architect.md:3`.
251. "Senior management consulting specialist for competitive analysis, market entry strategy, business model design, growth" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/business-strategist.md:4`.
252. "Expert change management specialist using ADKAR, Kotter, and Prosci frameworks to guide organizations through" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/change-management-consultant.md:4`.
253. "Strategic finance executive who governs capital allocation, treasury operations, financial planning, M&A finance, investor" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/chief-financial-officer.md:4`.
254. "Expert in enterprise training system design and curriculum development — proficient in training needs" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/corporate-training-designer.md:3`.
255. "Friendly, professional customer service specialist for any industry — handling inquiries, complaints, account support," — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/customer-service.md:4`.
256. "Strategic customer success specialist for onboarding, health scoring, QBR facilitation, churn prevention, expansion identification," — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/customer-success-manager.md:4`.
257. "AI agent that consolidates extracted sales data into live reporting dashboards with territory, rep," — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/data-consolidation-agent.md:3`.
258. "Corporate data privacy specialist and DPO who builds GDPR, CCPA, and global privacy compliance" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/data-privacy-officer.md:4`.
259. "Corporate sustainability strategist and ESG reporting specialist who builds environmental, social, and governance programs," — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/esg-sustainability-officer.md:4`.
260. "Presales expert for China's government digital transformation market (ToG), proficient in policy interpretation, solution" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/government-digital-presales-consultant.md:3`.
261. "Expert grant writing specialist for nonprofits, research institutions, and social enterprises — covering prospect" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/grant-writer.md:4`.
262. "Compassionate, HIPAA-aligned care coordination and decision-support agent for family caregivers managing an aging parent's" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/healthcare-aging-parent-care-companion.md:4`.
263. "Empathetic healthcare customer service specialist for patient support, billing inquiries, appointment management, insurance questions," — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/healthcare-customer-service.md:4`.
264. "Expert in healthcare marketing compliance in China, proficient in the Advertising Law, Medical Advertisement" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/healthcare-marketing-compliance.md:3`.
265. "Comprehensive hospitality guest services specialist for hotels, resorts, restaurants, and event venues — covering" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/hospitality-guest-services.md:4`.
266. "Comprehensive HR onboarding specialist for employee orientation, documentation management, compliance tracking, benefits enrollment, culture" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/hr-onboarding.md:4`.
267. "Operates a shared identity graph that multiple AI agents resolve against. Ensures every agent" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/identity-graph-operator.md:3`.
268. "Real-time Spanish ↔ English translation specialist with cultural context, regional dialect awareness, travel phrase" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/language-translator.md:4`.
269. "Comprehensive legal billing and time tracking specialist for accurate time capture, invoice generation, billing" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/legal-billing-time-tracking.md:4`.
270. "Comprehensive legal client intake specialist for qualifying prospects, collecting case information, scheduling consultations, managing" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/legal-client-intake.md:4`.
271. "Comprehensive legal document review specialist for contracts, litigation documents, and real estate agreements —" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/legal-document-review.md:4`.
272. "Comprehensive loan officer assistant for mortgage and lending professionals — covering borrower intake, pre-qualification," — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/loan-officer-assistant.md:4`.
273. "Language Server Protocol specialist building unified code intelligence systems through LSP client orchestration and" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/lsp-index-engineer.md:3`.
274. "Mergers and acquisitions integration specialist who designs and executes post-merger integration programs — covering" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/ma-integration-manager.md:4`.
275. "Expert medical billing and coding specialist for ICD-10-CM/PCS, CPT, and HCPCS coding, claim submission," — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/medical-billing-coding-specialist.md:4`.
276. "Business operations specialist who applies Lean, Six Sigma, and systems thinking to process mapping," — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/operations-manager.md:4`.
277. "Applied organizational psychologist who diagnoses team dynamics, psychological safety, burnout risk, and culture health" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/organizational-psychologist.md:4`.
278. "Cross-domain personal development mentor for goal clarity, habit design, strategic decisions, and accountability without" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/personal-growth-mentor.md:3`.
279. "Comprehensive real estate agent assistant for buyer representation, seller representation, listing management, offer negotiation," — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/real-estate-buyer-seller.md:4`.
280. "Expert recruitment operations and talent acquisition specialist — skilled in China's major hiring platforms," — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/recruitment-specialist.md:3`.
281. "AI agent that automates distribution of consolidated sales reports to representatives based on territorial" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/report-distribution-agent.md:3`.
282. "Candidate-side resume optimization specialist who analyzes job descriptions, maps real experience to role requirements," — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/resume-tailor.md:3`.
283. "Comprehensive retail customer returns specialist for processing returns, exchanges, and refunds across in-store, online," — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/retail-customer-returns.md:4`.
284. "AI agent specialized in monitoring Excel files and extracting key sales metrics (MTD, YTD," — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/sales-data-extraction-agent.md:3`.
285. "Consultative B2B sales outreach specialist for cold prospecting, lead follow-up, objection handling, proposal writing," — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/sales-outreach.md:4`.
286. "Master coordinator for founders and executives — filters noise, owns processes, enforces consistency, routes" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/specialized-chief-of-staff.md:3`.
287. "Expert civil and structural engineer with global standards coverage — Eurocode, DIN, ACI, AISC," — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/specialized-civil-engineer.md:3`.
288. "Multi-session, multi-tool drift detection specialist who audits codebases touched by several AI coding tools" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/specialized-codebase-archaeologist.md:3`.
289. "CQ specialist that detects invisible exclusion, researches global context, and ensures software resonates authentically" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/specialized-cultural-intelligence-strategist.md:3`.
290. "Expert developer advocate specializing in building developer communities, creating compelling technical content, optimizing developer" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/specialized-developer-advocate.md:3`.
291. "Expert document creation specialist who generates professional PDF, PPTX, DOCX, and XLSX files using" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/specialized-document-generator.md:3`.
292. "Expert FedRAMP and NIST Risk Management Framework compliance engineer specializing in both FedRAMP authorization" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/specialized-fedramp-rmf-compliance.md:4`.
293. "Instrumental focus music specialist and neuroacoustic prompt engineer — crafts high-yield prompts, soundscape architectures," — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/specialized-focus-music-architect.md:3`.
294. "Navigate the French ESN/SI freelance ecosystem — margin models, platform mechanics (Malt, collective.work), portage" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/specialized-french-consulting-market.md:3`.
295. "Korean business culture for foreign professionals — 품의 decision process, nunchi reading, KakaoTalk business" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/specialized-korean-business-navigator.md:3`.
296. "Master planning architect, technical educator, and ruthless plan critic who specializes in deep architectural" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/specialized-master-plan-architect.md:3`.
297. "Expert Model Context Protocol developer who designs, builds, and tests MCP servers that extend" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/specialized-mcp-builder.md:3`.
298. "Independent model QA expert who audits ML and statistical models end-to-end - from documentation" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/specialized-model-qa.md:3`.
299. "Specialized pricing analyst who develops optimal pricing models through market research, competitor analysis, cost" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/specialized-pricing-analyst.md:3`.
300. "Solution architecture for Salesforce platform — multi-cloud design, integration patterns, governor limits, deployment strategy," — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/specialized-salesforce-architect.md:3`.
301. "Conducts live strategy duels using game theory and the 36 Chinese stratagems" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/specialized-strategy-duel-agent.md:4`.
302. "Workflow design specialist who maps complete workflow trees for every system, user journey, and" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/specialized-workflow-architect.md:3`.
303. "Full-spectrum study abroad planning expert covering the US, UK, Canada, Australia, Europe, Hong Kong," — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/study-abroad-advisor.md:3`.
304. "Expert supply chain management and procurement strategy specialist — skilled in supplier development, strategic" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/supply-chain-strategist.md:3`.
305. "Knowledge-base steward in the spirit of Niklas Luhmann's Zettelkasten. Default perspective: Luhmann; switches to" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/zk-steward.md:3`.
306. "Expert data analyst transforming raw data into actionable business insights. Creates dashboards, performs statistical" — `C:/dev/Tenant-Management-System/skills/agency-agents/support/support-analytics-reporter.md:3`.
307. "Consultant-grade AI specialist trained to think and communicate like a senior strategy consultant. Transforms" — `C:/dev/Tenant-Management-System/skills/agency-agents/support/support-executive-summary-generator.md:3`.
308. "Expert financial analyst and controller specializing in financial planning, budget management, and business performance" — `C:/dev/Tenant-Management-System/skills/agency-agents/support/support-finance-tracker.md:3`.
309. "Expert infrastructure specialist focused on system reliability, performance optimization, and technical operations management. Maintains" — `C:/dev/Tenant-Management-System/skills/agency-agents/support/support-infrastructure-maintainer.md:3`.
310. "Expert legal and compliance specialist ensuring business operations, data handling, and content creation comply" — `C:/dev/Tenant-Management-System/skills/agency-agents/support/support-legal-compliance-checker.md:3`.
311. "Expert customer support specialist delivering exceptional customer service, issue resolution, and user experience optimization." — `C:/dev/Tenant-Management-System/skills/agency-agents/support/support-support-responder.md:3`.
312. "Expert accessibility specialist who audits interfaces against WCAG standards, tests with assistive technologies, and" — `C:/dev/Tenant-Management-System/skills/agency-agents/testing/testing-accessibility-auditor.md:3`.
313. "Expert API testing specialist focused on comprehensive API validation, performance testing, and quality assurance" — `C:/dev/Tenant-Management-System/skills/agency-agents/testing/testing-api-tester.md:3`.
314. "Screenshot-obsessed, fantasy-allergic QA specialist - Reports reproducible issues with evidence and marks untested scope" — `C:/dev/Tenant-Management-System/skills/agency-agents/testing/testing-evidence-collector.md:3`.
315. "Expert performance testing and optimization specialist focused on measuring, analyzing, and improving system performance" — `C:/dev/Tenant-Management-System/skills/agency-agents/testing/testing-performance-benchmarker.md:3`.
316. "Stops fantasy approvals, evidence-based certification - Default to "NEEDS WORK", requires overwhelming proof for" — `C:/dev/Tenant-Management-System/skills/agency-agents/testing/testing-reality-checker.md:3`.
317. "Expert end-to-end test automation engineer for Playwright and Cypress — resilient selectors, flake elimination," — `C:/dev/Tenant-Management-System/skills/agency-agents/testing/testing-test-automation-engineer.md:3`.
318. "Expert test analysis specialist focused on comprehensive test result evaluation, quality metrics analysis, and" — `C:/dev/Tenant-Management-System/skills/agency-agents/testing/testing-test-results-analyzer.md:3`.
319. "Expert technology assessment specialist focused on evaluating, testing, and recommending tools, software, and platforms" — `C:/dev/Tenant-Management-System/skills/agency-agents/testing/testing-tool-evaluator.md:3`.
320. "Expert process improvement specialist focused on analyzing, optimizing, and automating workflows across all business" — `C:/dev/Tenant-Management-System/skills/agency-agents/testing/testing-workflow-optimizer.md:3`.
321. "When the user wants to plan, design, or implement an A/B test or experiment," — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/ab-testing/SKILL.md:3`.
322. "Design, implement, and audit inclusive digital products using WCAG 2.2 Level AA. Use when" — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/accessibility/SKILL.md:3`.
323. "When the user wants to generate, iterate, or scale ad creative — headlines, descriptions," — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/ad-creative/SKILL.md:3`.
324. "When the user wants help with paid advertising campaigns on Google Ads, Meta (Facebook/Instagram)," — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/ads/SKILL.md:3`.
325. "When the user wants to optimize content for AI search engines, get cited by" — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/ai-seo/SKILL.md:3`.
326. "When the user wants to set up, improve, or audit analytics tracking and measurement." — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/analytics/SKILL.md:3`.
327. "UI and visual skill for antislop. Use when building or editing any interface: color," — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/antislop-ui/SKILL.md:3`.
328. "When the user wants to audit or optimize an App Store or Google Play" — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/aso/SKILL.md:3`.
329. "Use when auditing an agent or LLM app for wrapper regression, memory pollution, tool" — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/bosskuai-agent-architecture-audit/SKILL.md:3`.
330. "Use when working out what to measure: instrumentation strategy, event design, funnels, experimentation, north-star" — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/bosskuai-analytics-metrics/SKILL.md:3`.
331. "Use when designing an API contract across REST, GraphQL, and event-driven interfaces: resource modeling," — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/bosskuai-api-design/SKILL.md:3`.
332. "Use when coupled modules should be consolidated or a codebase made more testable and" — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/bosskuai-architecture-deepening/SKILL.md:3`.
333. "Use when designing agent loop structure, from sequential pipelines to RFC-driven DAGs: exit conditions," — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/bosskuai-autonomous-loops/SKILL.md:3`.
334. "Use when reviewing workflow rules for hidden business logic flaws: state transitions, approval and" — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/bosskuai-business-logic-review/SKILL.md:3`.
335. "Use when designing, speeding up, or fixing CI/CD pipelines, including GitHub Actions, GitLab CI," — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/bosskuai-ci-cd-pipelines/SKILL.md:3`.
336. "Use when explaining runtime behavior by tracing execution paths, call chains, module boundaries and" — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/bosskuai-codebase-analysis/SKILL.md:3`.
337. "Use when tasks, reviews, incidents, or repeated observations produced a lesson: decide the smallest" — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/bosskuai-continuous-learning/SKILL.md:3`.
338. "Use when controlling cloud/server/API/model cost: token budgets, queue sizing, storage costs, vendor spend, and" — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/bosskuai-cost-optimization/SKILL.md:3`.
339. "Use when acting as a CTO on technology strategy, roadmaps, architecture bets, build-vs-buy, engineering" — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/bosskuai-cto-strategy/SKILL.md:3`.
340. "Use when you need support SOPs, ticket triage and SLAs, human-led onboarding to first" — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/bosskuai-customer-success-support/SKILL.md:3`.
341. "Use when doing a cybersecurity review or hardening: privacy, abuse-case analysis, auth and authorization" — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/bosskuai-cybersecurity-risk/SKILL.md:3`.
342. "Use when SQL or NoSQL database design affects correctness or scale (MariaDB, MySQL, PostgreSQL," — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/bosskuai-database-engineering/SKILL.md:3`.
343. "Use when a task needs in-depth investigation: multi-source research, due diligence, technology evaluation, and" — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/bosskuai-deep-research/SKILL.md:3`.
344. "Use when creating, auditing, or applying a design system, including DESIGN.md generation, design token" — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/bosskuai-design-systems/SKILL.md:3`.
345. "Use when doing infrastructure as code (Terraform/OpenTofu, Pulumi), environment promotion, release strategies (canary, blue-green," — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/bosskuai-devops-iac/SKILL.md:3`.
346. "Use when diagnosing hard bugs or perf regressions: reproduce, minimise, hypothesise, instrument, fix, regression-test." — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/bosskuai-diagnose-loop/SKILL.md:3`.
347. "Use when implementing a software change through planning, tests, review, and observed product verification." — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/bosskuai-engineering-delivery/SKILL.md:3`.
348. "Use when you need agent eval design, routing tests, retrieval tests, LLM quality cases," — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/bosskuai-eval-driven-agent-improvement/SKILL.md:3`.
349. "Use when modeling forward-looking startup finance: revenue and ARR/MRR projections, runway and burn, unit" — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/bosskuai-financial-modeling/SKILL.md:3`.
350. "Use when GitHub is the delivery surface: issues, pull requests, Actions, releases, Dependabot, repository" — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/bosskuai-github-workflow/SKILL.md:3`.
351. "Use when a plan needs stress-testing against the existing domain model; updates CONTEXT.md and" — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/bosskuai-grill-with-docs/SKILL.md:3`.
352. "Use when the user asks to hand off, wrap up for another agent or" — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/bosskuai-handoff/SKILL.md:3`.
353. "Use when the task names Hindsight or asks to integrate its MCP/CLI, scope its" — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/bosskuai-hindsight-memory/SKILL.md:3`.
354. "Use when a product must work across languages, locales, and regions: content, locale handling," — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/bosskuai-i18n-l10n/SKILL.md:3`.
355. "Use when an incident is active: triage, severity classification, escalation coordination, on-call communication, timeline" — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/bosskuai-incident-response/SKILL.md:3`.
356. "Use when designing integration tests: contract testing (CDC/Pact), test double strategy, fixture management, and" — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/bosskuai-integration-testing/SKILL.md:3`.
357. "Use when building, refactoring, or auditing Laravel code: Eloquent, validation, policies, jobs, events, migrations," — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/bosskuai-laravel-development/SKILL.md:3`.
358. "Use when checking product-facing legal and compliance readiness, such as privacy posture, consent, retention," — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/bosskuai-legal-compliance/SKILL.md:3`.
359. "Use when doing a Malaysia PDPA-aware privacy review: data minimization, consent, retention, user rights," — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/bosskuai-malaysia-pdpa-privacy/SKILL.md:3`.
360. "Use when you need market analysis, competitor comparison, trend research, demand validation, positioning, pricing" — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/bosskuai-market-analysis/SKILL.md:3`.
361. "Use when you need a one-pass go-to-market or growth strategy: audience, positioning line, stage-fit" — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/bosskuai-marketing-growth/SKILL.md:3`.
362. "Use when releasing a mobile app to Apple App Store or Google Play, including" — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/bosskuai-mobile-app-release/SKILL.md:3`.
363. "Use when adding logs, metrics, tracing, alerts, SLOs, health checks, dashboards, incident detection, or" — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/bosskuai-observability-sre/SKILL.md:3`.
364. "Use when doing business operations work: vendor management, process documentation, change management, capacity planning," — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/bosskuai-operations/SKILL.md:3`.
365. "Use when investigating why something is slow or growing: CPU/memory profiling, bottleneck diagnosis, query" — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/bosskuai-performance-profiling/SKILL.md:3`.
366. "Use when the task touches BosskuAI memory, automatic remembering, bossku remember, Obsidian storage, cross-tool" — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/bosskuai-permanent-memory-orchestration/SKILL.md:3`.
367. "Use when you need roadmap planning, execution slicing, milestone sequencing, launch planning, prioritization, delivery" — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/bosskuai-planning-execution/SKILL.md:3`.
368. "Use when a task spans several languages, frameworks, or runtimes, or ecosystem context changes" — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/bosskuai-polyglot-engineering/SKILL.md:3`.
369. "Use when deciding what to build and why: product strategy, feature shaping, PRD review," — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/bosskuai-product-strategy/SKILL.md:3`.
370. "Use when verifying real user journeys, signup/checkout flows, CLI smoke checks, or a launch" — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/bosskuai-product-verification/SKILL.md:3`.
371. "Use when learning what a repo is, who it serves, what defines its behavior" — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/bosskuai-project-understanding/SKILL.md:3`.
372. "Use when the user asks to optimize, improve, or draft a prompt for BosskuAI;" — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/bosskuai-prompt-optimizer/SKILL.md:3`.
373. "Use when setting automated testing strategy: Playwright/Cypress, feature tests, integration tests, regression suites, fixtures," — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/bosskuai-qa-automation-strategy/SKILL.md:3`.
374. "Use when you need rapid prototypes, proof-of-concepts, demos, hackathon-style builds, MVP scaffolds, unfamiliar API" — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/bosskuai-rapid-prototype/SKILL.md:3`.
375. "Use when building or auditing React and TypeScript frontends, including components, hooks, state management," — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/bosskuai-react-development/SKILL.md:3`.
376. "Use when doing PR or pre-merge review, adversarial review, or challenging an implementation, a" — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/bosskuai-rigorous-code-review/SKILL.md:3`.
377. "Use when handling SaaS subscription lifecycle, invoices, failed payments, dunning, tax/receipt flows, plan changes," — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/bosskuai-saas-billing-ops/SKILL.md:3`.
378. "Use when turning interest into revenue: sales positioning, ICP definition, pipeline strategy, founder-led sales," — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/bosskuai-sales-strategy/SKILL.md:3`.
379. "Use when creating, improving, evaluating, or benchmarking BosskuAI skills and their triggers, sidecars, or" — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/bosskuai-skill-creator/SKILL.md:3`.
380. "Use when no listed skill fits (marketing, SEO, ads, legal, finance, design, mobile, DevOps)" — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/bosskuai-skill-finder/SKILL.md:3`.
381. "Use when deciding software architecture, module boundaries, system design, integration design, layering decisions, structural" — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/bosskuai-software-architecture/SKILL.md:3`.
382. "Use when the user asks for TDD, test-first, or red-green-refactor work on a feature" — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/bosskuai-tdd-loop/SKILL.md:3`.
383. "Use when checking multi-tenant data isolation: organization scoping, cross-tenant leaks, authorization boundaries, row-level access," — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/bosskuai-tenant-isolation-security/SKILL.md:3`.
384. "Use when one design question needs a throwaway prototype: a runnable terminal app for" — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/bosskuai-throwaway-prototype/SKILL.md:3`.
385. "Use when the user explicitly asks for terse output, lower token use, caveman mode," — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/bosskuai-token-saver/SKILL.md:3`.
386. "Use when the user asks to set up, check or install an optional tool" — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/bosskuai-tools/SKILL.md:3`.
387. "Use when reviewing or critiquing UI/UX, or turning designs or screenshots into implementation-ready code" — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/bosskuai-ui-ux-design-to-code/SKILL.md:3`.
388. "You MUST use this before any creative work - creating features, building components, adding" — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/brainstorming/SKILL.md:3`.
389. "Premium brand-kit image generation skill for creating high-end brand-guidelines boards, logo systems, identity decks," — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/brandkit/SKILL.md:3`.
390. "Write B2B cold emails and follow-up sequences that get replies. Use when the user" — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/cold-email/SKILL.md:3`.
391. "Build and leverage online communities to drive product growth and brand loyalty. Use when" — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/community-marketing/SKILL.md:3`.
392. "When the user wants to plan a content strategy, decide what content to create," — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/content-strategy/SKILL.md:3`.
393. "When the user wants to optimize, improve, or increase conversions on any marketing page" — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/cro/SKILL.md:3`.
394. "When the user wants to conduct, analyze, or synthesize customer research. Use when the" — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/customer-research/SKILL.md:3`.
395. "Destructive Command Guard (dcg) — agent hook that blocks dangerous shell/git before execution. Use" — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/dcg/SKILL.md:3`.
396. "Playwright E2E testing patterns, Page Object Model, configuration, CI/CD integration, artifact management, and flaky" — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/e2e-testing/SKILL.md:3`.
397. "When the user wants to create or optimize an email sequence, drip campaign, automated" — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/emails/SKILL.md:3`.
398. "Use for any question about a codebase, its architecture, file relationships, or project content" — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/graphify/SKILL.md:3`.
399. "When the user wants to create, generate, edit, or optimize images for marketing —" — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/image/SKILL.md:3`.
400. ">" — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/loop-triage/SKILL.md:3`.
401. "When the user wants to apply psychological principles, mental models, or behavioral science to" — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/marketing-psychology/SKILL.md:3`.
402. "Build MCP servers with Node/TypeScript SDK — tools, resources, prompts, Zod validation, stdio vs" — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/mcp-server-patterns/SKILL.md:3`.
403. ">" — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/minimal-fix/SKILL.md:3`.
404. "When the user wants to design, construct, or improve an offer — the thing" — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/offers/SKILL.md:3`.
405. "When the user wants help with pricing decisions, packaging, or monetization strategy. Also use" — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/pricing/SKILL.md:3`.
406. "When the user wants help with public relations, earned media, press coverage, journalist outreach," — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/public-relations/SKILL.md:3`.
407. "When the user wants help with revenue operations, lead lifecycle management, or marketing-to-sales handoff" — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/revops/SKILL.md:3`.
408. "When the user wants to audit, review, or diagnose SEO issues on their site." — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/seo-audit/SKILL.md:3`.
409. "When the user wants help creating, scheduling, or optimizing social media content for LinkedIn," — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/social/SKILL.md:3`.
410. "When the user wants to create, generate, or produce video content using AI tools" — `C:/Users/mspc0/OneDrive/Documents/Bossku-AI/skills/video/SKILL.md:3`.
411. "MIT License" and "Copyright (c) 2026 Matt Pocock" — `C:/dev/Tenant-Management-System/skills/skills/LICENSE:1`, `:3`.
412. "MIT License" and "Copyright (c) 2025 AgentLand Contributors" — `C:/dev/Tenant-Management-System/skills/agency-agents/LICENSE:1`, `:3`.

413. "Lead each section with the recommended answer so the user can accept it in a word." — `C:/dev/Tenant-Management-System/skills/skills/skills/engineering/setup-matt-pocock-skills/SKILL.md:36`.
414. "- For setup: `.env`, `.env.example`, `.env.*`, `README`, `docker-compose*`, framework config, and `.github/workflows/*` (every `secrets.*` / `vars.*`" — `C:/dev/Tenant-Management-System/skills/skills/skills/engineering/wizard/SKILL.md:20`.
415. "Create a committed `<packages-root>/example/` as a copy-me template:" — `C:/dev/Tenant-Management-System/skills/skills/skills/in-progress/setup-ts-deep-modules/SKILL.md:69`.
416. "2. **Create directories** - `mkdir -p` for each path" — `C:/dev/Tenant-Management-System/skills/skills/skills/misc/scaffold-exercises/SKILL.md:47`.
417. "- `./lessons/*.html`: A directory of lessons. A **lesson** is a single, self-contained HTML output that teaches" — `C:/dev/Tenant-Management-System/skills/skills/skills/productivity/teach/SKILL.md:18`.
418. "1. **Who is it going to?** Ask, in one exchange, the recipient's role, expertise, and relationship" — `C:/dev/Tenant-Management-System/skills/skills/skills/productivity/to-questionnaire/SKILL.md:12`.
419. "- Build kinship systems, social organization, and power structures that make anthropological sense" — `C:/dev/Tenant-Management-System/skills/agency-agents/academic/academic-anthropologist.md:22`.
420. "- Check that climate, terrain, and biomes are physically consistent with each other" — `C:/dev/Tenant-Management-System/skills/agency-agents/academic/academic-geographer.md:22`.
421. "- Identify anachronisms — not just obvious ones (potatoes in pre-Columbian Europe) but subtle ones (attitudes," — `C:/dev/Tenant-Management-System/skills/agency-agents/academic/academic-historian.md:22`.
422. "- Identify the **controlling idea** (McKee) or **premise** (Egri) — what the story is actually about" — `C:/dev/Tenant-Management-System/skills/agency-agents/academic/academic-narratologist.md:22`.
423. "- Analyze character behavior through established personality frameworks (Big Five, attachment theory)" — `C:/dev/Tenant-Management-System/skills/agency-agents/academic/academic-psychologist.md:22`.
424. "- Create brand character through micro-interactions, copy, and visual elements" — `C:/dev/Tenant-Management-System/skills/agency-agents/design/design-whimsy-injector.md:23`.
425. "- Extract 3-5 representative samples per cluster for AI analysis" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-ai-data-remediation-engineer.md:33`.
426. "- Build machine learning models for practical business applications" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-ai-engineer.md:22`.
427. "1. **Enforce Structural Linearization & Geometry Safety**: Audit document bounding boxes to eliminate multi-column reading-order traps," — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-ats-validator-architect.md:29`.
428. "Design, configure, and troubleshoot production networks built on the Chinese domestic stack, with the same rigor" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-china-network-engineer.md:31`.
429. "1. **Never fight the CMS.** Use hooks, filters, and the plugin/module system. Don't monkey-patch core." — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-cms-developer.md:38`.
430. "- Design and build ETL/ELT pipelines that are idempotent, observable, and self-healing" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-data-engineer.md:22`.
431. "- Build the release pipeline: code signing on Windows, signing + notarization on macOS, reproducible builds," — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-desktop-app-engineer.md:22`.
432. "Make Drupal sites load fast and stay fast — passing Core Web Vitals on real mobile" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-drupal-performance.md:29`.
433. "Build and maintain Drupal Commerce storefronts that are correct, reliable, and scalable — where pricing is" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-drupal-shopping-cart.md:29`.
434. "* Build robust pipelines that ingest raw email (MIME, Gmail API, Microsoft Graph) and produce structured," — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-email-intelligence-engineer.md:24`.
435. "- Write correct, deterministic firmware that respects hardware constraints (RAM, flash, timing)" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-embedded-firmware-engineer.md:18`.
436. "- Use official Feishu SDKs (`oapi-sdk-nodejs` / `oapi-sdk-python`) instead of manually constructing HTTP requests" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-feishu-integration-developer.md:81`.
437. "Build GaussDB architectures that perform well under load, leverage distributed parallelism, achieve financial-grade availability, and never" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-gaussdb-expert.md:101`.
438. "- Build telemetry pipelines over MQTT (or equivalent) that tolerate intermittent connectivity, buffer at the edge," — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-iot-fleet-engineer.md:21`.
439. "Ensure IT services are reliable, measurable, and aligned with business needs — by implementing structured service" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-it-service-manager.md:28`.
440. "- Identify the target, non-goals, supervision signal, and missing evidence." — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-llm-post-training-engineer.md:24`.
441. "- Design and write production-ready router, switch, and firewall configurations for Cisco, Juniper, and Palo Alto" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-network-engineer.md:18`.
442. "- Maintain and enhance the OrgScript parser, linter, formatter, and CLI tooling." — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-orgscript-engineer.md:22`.
443. "Never generate PDF HTML by concatenating raw template strings in a parallel backend codebase. Always snapshot" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-pdf-engine-architect.md:44`.
444. "- Make the opinionated path the easiest path. Customization is opt-in and costs more" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-platform-engineer.md:24`.
445. "- Design chunking pipelines that preserve semantic coherence — choosing between fixed-size, semantic, and structural (header-based)" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-rag-pipeline-engineer.md:30`.
446. "- Build realtime transport that treats disconnection as the normal case: heartbeats, resumable sessions, exponential backoff" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-realtime-collaboration-engineer.md:20`.
447. "- Report every credible, evidence-backed opportunity rather than stopping at an arbitrary top-N list" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-rust-refactoring-specialist.md:31`.
448. "- Design indices, mappings, and analyzer chains that make documents findable the way users actually type" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-search-relevance-engineer.md:20`.
449. "Make web applications and documents genuinely usable by people with disabilities and demonstrably conformant to the" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-section-508-specialist.md:31`.
450. "- Choose the right automation surface: **Flow Designer** for orchestrated, low-code flows; **Business Rules** for record-event" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-servicenow-developer-mentor.md:23`.
451. "- Write Solidity contracts following checks-effects-interactions and pull-over-push patterns by default" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-solidity-smart-contract-engineer.md:23`.
452. "Never discard, truncate, or reject an unknown YAML key. If an incoming document contains `clinical_trials`, `server_benchmarks`," — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-universal-document-compiler.md:42`.
453. "Build trustworthy, accessible, consistent federal interfaces with the U.S. Web Design System — themed through its" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-uswds-developer.md:31`.
454. "- Build transcode ladders that match content and audience: per-title or per-scene bitrate/resolution rungs via ffmpeg," — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-video-streaming-engineer.md:20`.
455. "* Design and build complete pipelines from audio upload to structured, usable output" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-voice-ai-integration-engineer.md:24`.
456. "- Build server-side Wasm: WASI modules on Wasmtime/Wasmer for plugin systems, edge compute, and sandboxed untrusted" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-webassembly-engineer.md:23`.
457. "- Implement responsive layouts using WXML/WXSS that feel native to WeChat" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-wechat-mini-program-developer.md:23`.
458. "Turn slow WordPress sites into fast, Core-Web-Vitals-passing ones — on real mobile devices — through measurement," — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-wordpress-performance.md:31`.
459. "Build and maintain WooCommerce storefronts that convert and reconcile — fast, frictionless checkouts that turn visitors" — `C:/dev/Tenant-Management-System/skills/agency-agents/engineering/engineering-wordpress-shopping-cart.md:29`.
460. "- Automate the recurring, focus the brain on the exceptional. Manual journal entries should be the" — `C:/dev/Tenant-Management-System/skills/agency-agents/finance/finance-bookkeeper-controller.md:24`.
461. "Produce institutional-quality investment research that surfaces actionable insights, quantifies risks and opportunities, and supports data-driven portfolio" — `C:/dev/Tenant-Management-System/skills/agency-agents/finance/finance-investment-researcher.md:29`.
462. "2. **Document every position.** Every tax election, every intercompany pricing decision, every uncertain position must have" — `C:/dev/Tenant-Management-System/skills/agency-agents/finance/finance-tax-strategist.md:34`.
463. "- Build Blender add-ons that automate asset prep, validation, and export" — `C:/dev/Tenant-Management-System/skills/agency-agents/game-development/blender/blender-addon-engineer.md:22`.
464. "- Map every currency and resource with explicit sources, sinks, and conversion paths" — `C:/dev/Tenant-Management-System/skills/agency-agents/game-development/economy-designer.md:22`.
465. "- Design FMOD/Wwise project structures that scale with content without becoming unmaintainable" — `C:/dev/Tenant-Management-System/skills/agency-agents/game-development/game-audio-engineer.md:22`.
466. "- Design core gameplay loops with clear moment-to-moment, session, and long-term hooks" — `C:/dev/Tenant-Management-System/skills/agency-agents/game-development/game-designer.md:23`.
467. "- Enforce the "everything is a node" philosophy through correct scene and node composition" — `C:/dev/Tenant-Management-System/skills/agency-agents/game-development/godot/godot-gameplay-scripter.md:22`.
468. "- Implement server-authoritative gameplay using `set_multiplayer_authority()` correctly" — `C:/dev/Tenant-Management-System/skills/agency-agents/game-development/godot/godot-multiplayer-engineer.md:22`.
469. "- Write 2D CanvasItem shaders for sprite effects, UI polish, and 2D post-processing" — `C:/dev/Tenant-Management-System/skills/agency-agents/game-development/godot/godot-shader-developer.md:22`.
470. "- Create layouts that teach mechanics without text through environmental affordances" — `C:/dev/Tenant-Management-System/skills/agency-agents/game-development/level-designer.md:22`.
471. "- Write dialogue and story content that sounds like characters, not writers" — `C:/dev/Tenant-Management-System/skills/agency-agents/game-development/narrative-designer.md:22`.
472. "- Create avatar accessories that attach correctly across R15 body types and avatar scales" — `C:/dev/Tenant-Management-System/skills/agency-agents/game-development/roblox-studio/roblox-avatar-creator.md:22`.
473. "- Design core engagement loops tuned for Roblox's audience (predominantly ages 9–17)" — `C:/dev/Tenant-Management-System/skills/agency-agents/game-development/roblox-studio/roblox-experience-designer.md:22`.
474. "- Implement server-authoritative game logic where clients receive visual confirmation, not truth" — `C:/dev/Tenant-Management-System/skills/agency-agents/game-development/roblox-studio/roblox-systems-scripter.md:22`.
475. "- Write and optimize shaders for target platforms (PC, console, mobile)" — `C:/dev/Tenant-Management-System/skills/agency-agents/game-development/technical-artist.md:22`.
476. "- Enforce single-responsibility across all MonoBehaviours and components" — `C:/dev/Tenant-Management-System/skills/agency-agents/game-development/unity/unity-architect.md:23`.
477. "- Build `EditorWindow` tools that give teams insight into project state without leaving Unity" — `C:/dev/Tenant-Management-System/skills/agency-agents/game-development/unity/unity-editor-tool-developer.md:22`.
478. "- Implement server-authoritative gameplay logic using Netcode for GameObjects" — `C:/dev/Tenant-Management-System/skills/agency-agents/game-development/unity/unity-multiplayer-engineer.md:22`.
479. "- Build custom render passes using URP's Renderer Feature system for full-screen effects" — `C:/dev/Tenant-Management-System/skills/agency-agents/game-development/unity/unity-shader-graph-artist.md:24`.
480. "- Implement UE5's authority model correctly: server simulates, clients predict and reconcile" — `C:/dev/Tenant-Management-System/skills/agency-agents/game-development/unreal-engine/unreal-multiplayer-architect.md:22`.
481. "- Implement the Gameplay Ability System (GAS) for abilities, attributes, and tags in a network-ready manner" — `C:/dev/Tenant-Management-System/skills/agency-agents/game-development/unreal-engine/unreal-systems-engineer.md:22`.
482. "- Build Niagara VFX systems with precise GPU/CPU budget control" — `C:/dev/Tenant-Management-System/skills/agency-agents/game-development/unreal-engine/unreal-technical-artist.md:23`.
483. "- Configure World Partition grids and streaming sources for smooth, hitch-free loading" — `C:/dev/Tenant-Management-System/skills/agency-agents/game-development/unreal-engine/unreal-world-builder.md:22`.
484. "- Build web scenes with terrain, buildings, trees, and infrastructure" — `C:/dev/Tenant-Management-System/skills/agency-agents/gis/gis-3d-scene-developer.md:22`.
485. "- Create clear, publication-ready maps for reports, presentations, and web" — `C:/dev/Tenant-Management-System/skills/agency-agents/gis/gis-analyst.md:22`.
486. "- Preserve BIM semantics: room names, materials, fire ratings, ownership" — `C:/dev/Tenant-Management-System/skills/agency-agents/gis/gis-bim-specialist.md:23`.
487. "- Choose appropriate color schemes: sequential (magnitude), diverging (deviation), qualitative (categories)" — `C:/dev/Tenant-Management-System/skills/agency-agents/gis/gis-cartography-designer.md:22`.
488. "- Design optimal flight plans for mapping: overlap, altitude, speed, camera settings" — `C:/dev/Tenant-Management-System/skills/agency-agents/gis/gis-drone-reality-mapping.md:22`.
489. "- **Never trust a single accuracy number**: Check per-class metrics, confusion matrix, spatial distribution of errors" — `C:/dev/Tenant-Management-System/skills/agency-agents/gis/gis-geoai-ml-engineer.md:43`.
490. "- Design professional geoprocessing tools with validation, error handling, and documentation" — `C:/dev/Tenant-Management-System/skills/agency-agents/gis/gis-geoprocessing-specialist.md:22`.
491. "- Geometry checks: self-intersections, null geometry, duplicate features, sliver polygons" — `C:/dev/Tenant-Management-System/skills/agency-agents/gis/gis-qa-engineer.md:22`.
492. "- Choose the right tool for the job: Pro for spatial analysis, AGOL for sharing, Python" — `C:/dev/Tenant-Management-System/skills/agency-agents/gis/gis-solution-engineer.md:23`.
493. "- Read data from any format: Shapefile, GeoPackage, GeoJSON, KML, KMZ, GPX, DXF, DWG, CSV, Parquet," — `C:/dev/Tenant-Management-System/skills/agency-agents/gis/gis-spatial-data-engineer.md:22`.
494. "- Identify statistically significant clusters of events (hot/cold spot analysis)" — `C:/dev/Tenant-Management-System/skills/agency-agents/gis/gis-spatial-data-scientist.md:22`.
495. "- Identify where location intelligence creates measurable value: cost reduction, revenue growth, risk mitigation" — `C:/dev/Tenant-Management-System/skills/agency-agents/gis/gis-technical-consultant.md:23`.
496. "- Choose the right mapping library for the use case: MapLibre GL JS, ArcGIS JS API," — `C:/dev/Tenant-Management-System/skills/agency-agents/gis/gis-web-gis-developer.md:22`.
497. "build and maintain the clinical credibility layer that differentiates serious" — `C:/dev/Tenant-Management-System/skills/agency-agents/healthcare/healthcare-clinical-evidence-agent.md:25`.
498. "Maintain narrative coherence across all external outputs. Ensure every" — `C:/dev/Tenant-Management-System/skills/agency-agents/healthcare/healthcare-innovation-strategist.md:50`.
499. "2. Always identify the specific UHC mandate or national health policy your" — `C:/dev/Tenant-Management-System/skills/agency-agents/healthcare/healthcare-sovereign-health-systems-agent.md:60`.
500. "- Optimize for Baidu's ranking factors, which differ fundamentally from Google's approach" — `C:/dev/Tenant-Management-System/skills/agency-agents/marketing/marketing-baidu-seo-specialist.md:20`.
501. "- Develop content strategies tailored to Bilibili's recommendation algorithm and tiered exposure system" — `C:/dev/Tenant-Management-System/skills/agency-agents/marketing/marketing-bilibili-content-strategist.md:20`.
502. "**Trace Claims to Sources**: Every substantial claim should be grounded in source notes, explicit assumptions, or" — `C:/dev/Tenant-Management-System/skills/agency-agents/marketing/marketing-book-co-author.md:31`.
503. "- Manage store operations across Taobao (淘宝), Tmall (天猫), Pinduoduo (拼多多), JD (京东), and Douyin Shop" — `C:/dev/Tenant-Management-System/skills/agency-agents/marketing/marketing-china-ecommerce-operator.md:20`.
504. "- Monitor China's hotlist ecosystem: Douyin (抖音热榜), Bilibili (B站热门), Weibo (微博热搜), Zhihu (知乎热榜), Baidu (百度热搜), Toutiao" — `C:/dev/Tenant-Management-System/skills/agency-agents/marketing/marketing-china-market-localization-strategist.md:23`.
505. "- **Review management**: Negative review response strategy (buyer outreach / Vine reviews / product improvement), review" — `C:/dev/Tenant-Management-System/skills/agency-agents/marketing/marketing-cross-border-ecommerce.md:95`.
506. "- Design high-completion-rate video structures: golden 3-second hook + information density + ending cliffhanger" — `C:/dev/Tenant-Management-System/skills/agency-agents/marketing/marketing-douyin-strategist.md:21`.
507. "Build and grow podcasts that become category authorities through:" — `C:/dev/Tenant-Management-System/skills/agency-agents/marketing/marketing-global-podcast-strategist.md:21`.
508. "- Develop strategies tailored to Kuaishou's 老铁经济 (brotherhood economy) built on trust and loyalty" — `C:/dev/Tenant-Management-System/skills/agency-agents/marketing/marketing-kuaishou-strategist.md:20`.
509. "- Evaluate hosts on process metrics, not just outcomes: script execution rate, interaction frequency, pacing control" — `C:/dev/Tenant-Management-System/skills/agency-agents/marketing/marketing-livestream-commerce-coach.md:81`.
510. "- **NEVER** trigger publish-to-production. Wechatsync defaults to drafts; rely on this default and stop there." — `C:/dev/Tenant-Management-System/skills/agency-agents/marketing/marketing-multi-platform-publisher.md:41`.
511. "- Do not manufacture controversy or spread unverified information for the sake of topicality" — `C:/dev/Tenant-Management-System/skills/agency-agents/marketing/marketing-podcast-strategist.md:133`.
512. "- Never add users to groups or mass-message without their consent" — `C:/dev/Tenant-Management-System/skills/agency-agents/marketing/marketing-private-domain-operator.md:71`.
513. "- Maintain consistent publishing schedule (2-3 posts per week for most businesses)" — `C:/dev/Tenant-Management-System/skills/agency-agents/marketing/marketing-wechat-official-account.md:27`.
514. "- Build real-time monitoring for brand keywords, competitor keywords, and industry-sensitive terms" — `C:/dev/Tenant-Management-System/skills/agency-agents/marketing/marketing-weibo-strategist.md:76`.
515. "- Create visually cohesive content with consistent aesthetic across all posts" — `C:/dev/Tenant-Management-System/skills/agency-agents/marketing/marketing-xiaohongshu-specialist.md:27`.
516. "- **Lead Generation Excellence**: Converting engaged readers into qualified leads through strategic positioning and CTAs" — `C:/dev/Tenant-Management-System/skills/agency-agents/marketing/marketing-zhihu-strategist.md:22`.
517. "- Implement instanced Metal rendering for 10k-100k nodes at 90fps" — `C:/dev/Tenant-Management-System/skills/agency-agents/spatial-computing/macos-spatial-metal-engineer.md:22`.
518. "- **Terminal Modes**: Raw mode, cooked mode, and application-specific terminal behavior" — `C:/dev/Tenant-Management-System/skills/agency-agents/spatial-computing/terminal-integration-specialist.md:18`.
519. "- **Design System**: Liquid Glass materials, spatial typography, and depth-aware UI components" — `C:/dev/Tenant-Management-System/skills/agency-agents/spatial-computing/visionos-spatial-engineer.md:36`.
520. "- Design hand-interactive yokes, levers, and throttles using 3D meshes and input constraints" — `C:/dev/Tenant-Management-System/skills/agency-agents/spatial-computing/xr-cockpit-interaction-specialist.md:22`.
521. "- Implement immersive interactions using raycasting, hit testing, and real-time physics" — `C:/dev/Tenant-Management-System/skills/agency-agents/spatial-computing/xr-immersive-developer.md:23`.
522. "- Create HUDs, floating menus, panels, and interaction zones" — `C:/dev/Tenant-Management-System/skills/agency-agents/spatial-computing/xr-interface-architect.md:22`.
523. "- Execute vendor and contractor payments with human-defined approval thresholds" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/accounts-payable-agent.md:22`.
524. "4. **Never announce a change before the plan is ready.** Announcing a change without a clear" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/change-management-consultant.md:47`.
525. "- Leads with the decision and the trade-off: "Here's the recommendation, the number, and what we" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/chief-financial-officer.md:20`.
526. "- Respect learners' existing experience — use facilitation, not lecturing; use discussion, not preaching" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/corporate-training-designer.md:123`.
527. "- **Report against recognized frameworks.** Align disclosures to GRI, SASB, TCFD, CSRD, or CDP as applicable" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/esg-sustainability-officer.md:30`.
528. "- Track national and local government digitalization policies to identify project opportunities:" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/government-digital-presales-consultant.md:24`.
529. "1. **Never misrepresent the organization or its work.** Funders verify claims, conduct site visits, and talk" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/grant-writer.md:44`.
530. "- Never replacing, overriding, or second-guessing the judgment of the care recipient's actual care team" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/healthcare-aging-parent-care-companion.md:45`.
531. "1. **Never provide clinical advice.** You are not a clinician. Never diagnose, recommend treatments, interpret test" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/healthcare-customer-service.md:42`.
532. "- Establish an internal three-tier review mechanism: Legal initial review -> Compliance secondary review -> Final" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/healthcare-marketing-compliance.md:39`.
533. "- **Check-In**: arrival experience, room assignment, amenity orientation" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/hospitality-guest-services.md:33`.
534. "2. **Never share one employee's information with another.** All personal, compensation, and benefits information is strictly" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/hr-onboarding.md:43`.
535. "Provide accurate, natural, culturally-aware translations that convey the intended meaning — not just the literal words" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/language-translator.md:26`.
536. "2. **Never bill for non-billable time.** Administrative time, firm overhead, time spent on billing itself, and" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/legal-billing-time-tracking.md:44`.
537. "1. **Never provide legal advice.** You are an intake specialist, not an attorney. Never tell a" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/legal-client-intake.md:43`.
538. "1. **Never provide legal advice.** You are a document review tool, not a lawyer. Always frame" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/legal-document-review.md:41`.
539. "Support loan officers in delivering fast, compliant, and borrower-friendly lending experiences — from initial inquiry through" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/loan-officer-assistant.md:28`.
540. "- Orchestrate multiple LSP clients (TypeScript, PHP, Go, Rust, Python) concurrently" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/lsp-index-engineer.md:22`.
541. "- **Track synergies against a baseline, honestly.** Report a synergy bridge with realized vs. planned and" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/ma-integration-manager.md:29`.
542. "4. **Never bill for services not rendered.** Billing for services that were not performed — regardless" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/medical-billing-coding-specialist.md:46`.
543. "- **Diagnose conditions, not characters.** Frame problems in terms of systems, incentives, and psychological needs —" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/organizational-psychologist.md:28`.
544. "- **Diagnose the real goal**: Separate what the user says they want from the outcome they" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/personal-growth-mentor.md:20`.
545. "1. **Always represent your client's best interests — exclusively.** A buyer's agent works for the buyer." — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/real-estate-buyer-seller.md:43`.
546. "- Build **job profiles** based on business needs and team status — clarify core responsibilities, must-have" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/recruitment-specialist.md:35`.
547. "- Extract the job description's must-have qualifications, nice-to-have signals, tools, seniority expectations, responsibilities, and hidden evaluation" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/resume-tailor.md:24`.
548. "Process returns, exchanges, and refunds efficiently, fairly, and in accordance with policy — while maximizing customer" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/retail-customer-returns.md:28`.
549. "- Design primary structural systems: steel frames, reinforced concrete, post-tensioned, timber, masonry, and composite" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/specialized-civil-engineer.md:25`.
550. "1. **Never describe a control you cannot prove — implementation and evidence move together.** A 3PAO" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/specialized-fedramp-rmf-compliance.md:53`.
551. "- Map the user's immediate workload to the optimal neuroacoustic profile:" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/specialized-focus-music-architect.md:27`.
552. "- Track which ESN tiers and platforms yield the best outcomes for the user's profile" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/specialized-french-consulting-market.md:18`.
553. "- Flag when advice conflicts with the user's cultural instincts — explain why Korean context differs" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/specialized-korean-business-navigator.md:19`.
554. "- Track recurring architectural decisions across sessions (e.g., "client always chooses Process Builder over Flow —" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/specialized-salesforce-architect.md:18`.
555. "- Run turn-based strategy duels between user and simulated opponents" — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/specialized-strategy-duel-agent.md:18`.
556. "- Recommend the most suitable countries and regions based on the student's academic background, career goals," — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/study-abroad-advisor.md:23`.
557. "- Establish supplier development and qualification review processes — end-to-end control from credential review, on-site audits," — `C:/dev/Tenant-Management-System/skills/agency-agents/specialized/supply-chain-strategist.md:24`.

## Expanded findings and priorities

User direction supersedes demand-based deferral: **add every useful unique skill, including niche domains**. This local snapshot contains38 canonical skills and282 division personas. Complete disposition: add=145, enhance=57, keep=4, overlap=114. Additions group into142 distinct proposed skill IDs; grouped providers share one workflow. All classifications are editorial inferences from the numbered source evidence, not execution certification.

Local provenance: skills package.json:8 /README.md:72 identify mattpocock/skills; agency README.md:5 identifies msitarzewski/agency-agents. Local MIT licenses name Matt Pocock2026 and AgentLand Contributors2025 (LICENSE:1-3) and require copyright/permission retention (LICENSE:11-12). Remote freshness and exact upstream lineage remain unverified. Source pr/CREDITS.md:3 attributes reproduced summary guidance to Dex Horthy/show-me; preserve that file and verify upstream license before copying that passage.

Priority **P1**: planning ticket schema (to-tickets:31-40); CLI contract checks (developer-tooling:20-36); search relevance (search-relevance:20-36); production RAG, desktop IPC/update, reconnect-safe collaboration and reliable data pipelines. **P2**: all useful niche candidates in the manifest, grouped by independent workflow and installed on demand. Existing role agents remain orchestrator/planner/designer/executor/auditor/final-reviewer.

Portable adaptation for every new candidate: write a narrow Use-when description; gather real source/environment; perform the source-backed methods in an explicit sequence; emit a concrete artifact; check it with observable evidence; list required tools and actual blocked scope. Remove fictional experience/memory, hard-coded performance success targets, unverifiable causal assertions and automatic external sends/payments. Capability sources become first-party skills, not extra generic personas. Facts about current libraries/platforms/law require primary-source verification when invoked; local persona prose does not certify those facts.

Keep vs overlap vs enhance: keep preserves adapted Bossku capability; overlap uses an existing owner without adding a duplicate; enhance lifts distinctive checklist/template into that owner; add is a new scoped portable workflow; defer means no actual method found. Body-method quotes are listed before analysis. All320 source files have a complete matrix entry; new additions have source method locations.

## Supporting resources and import boundaries

Canonical skill support: codebase-design DEEPENING.md/DESIGN-IT-TWICE.md; domain-modeling ADR-FORMAT.md/GLOSSARY-FORMAT.md; architecture HTML-REPORT.md; triage AGENT-BRIEF.md/OUT-OF-SCOPE.md; setup tracker github/gitlab/local adapters; TDD mocking.md/tests.md; teach four *-FORMAT.md resources; wizard template.sh; TS boundaries dependency-cruiser.config.cjs; writing-for-agents SKILL-MECHANICS.md. Carry the relevant resource and maintain local links, not agents/openai.yaml or generated host mirrors. Treat scripts as examples until shell/platform compatibility is checked.

Source in-progress/README.md:3 explicitly calls these beta and excludes them from the plugin. Useful methods can be adapted, but do not silently vendor them as stable upstream skills; record local snapshot provenance. The generated agency integrations are packaging mirrors, not independent capability sources.

## Complete canonical skill decisions

| Source under canonical skills/ | Quote | Decision | Owner |
|---|---:|---|---|
| engineering/ask-matt/SKILL.md | 1 | overlap | bosskuai-skill-finder |
| engineering/code-review/SKILL.md | 2 | enhance | bosskuai-rigorous-code-review |
| engineering/codebase-design/SKILL.md | 3 | overlap | bosskuai-software-architecture |
| engineering/diagnosing-bugs/SKILL.md | 4 | overlap | bosskuai-diagnose-loop |
| engineering/domain-modeling/SKILL.md | 5 | enhance | bosskuai-software-architecture |
| engineering/grill-with-docs/SKILL.md | 6 | keep | bosskuai-grill-with-docs |
| engineering/implement/SKILL.md | 7 | overlap | bosskuai-engineering-delivery |
| engineering/implement-spec/SKILL.md | 8 | overlap | bosskuai-engineering-delivery |
| engineering/improve-codebase-architecture/SKILL.md | 9 | keep | bosskuai-architecture-deepening |
| engineering/pr/SKILL.md | 10 | enhance | bosskuai-github-workflow |
| engineering/prototype/SKILL.md | 11 | keep | bosskuai-throwaway-prototype |
| engineering/research/SKILL.md | 12 | overlap | bosskuai-deep-research |
| engineering/retro/SKILL.md | 13 | overlap | bosskuai-continuous-learning |
| engineering/setup-matt-pocock-skills/SKILL.md | 14 | add | bosskuai-issue-tracker-setup |
| engineering/tdd/SKILL.md | 15 | overlap | bosskuai-tdd-loop |
| engineering/to-spec/SKILL.md | 16 | enhance | bosskuai-planning-execution |
| engineering/to-tickets/SKILL.md | 17 | enhance | bosskuai-planning-execution |
| engineering/triage/SKILL.md | 18 | overlap | loop-triage |
| engineering/wayfinder/SKILL.md | 19 | enhance | bosskuai-planning-execution |
| engineering/wizard/SKILL.md | 20 | add | bosskuai-human-setup-wizard |
| in-progress/chief-of-staff/SKILL.md | 21 | overlap | agents/orchestrator.md |
| in-progress/claude-handoff/SKILL.md | 22 | enhance | bosskuai-handoff |
| in-progress/loop-me/SKILL.md | 23 | enhance | bosskuai-planning-execution |
| in-progress/setup-ts-deep-modules/SKILL.md | 24 | add | bosskuai-typescript-module-boundaries |
| in-progress/writing-beats/SKILL.md | 25 | enhance | copywriting |
| in-progress/writing-fragments/SKILL.md | 26 | enhance | copywriting |
| in-progress/writing-shape/SKILL.md | 27 | enhance | copywriting |
| misc/git-guardrails-claude-code/SKILL.md | 28 | overlap | dcg |
| misc/migrate-to-shoehorn/SKILL.md | 29 | enhance | bosskuai-polyglot-engineering |
| misc/scaffold-exercises/SKILL.md | 30 | add | bosskuai-course-exercises |
| misc/setup-pre-commit/SKILL.md | 31 | enhance | bosskuai-ci-cd-pipelines |
| productivity/grill-me/SKILL.md | 32 | overlap | brainstorming |
| productivity/grilling/SKILL.md | 33 | overlap | bosskuai-grill-with-docs |
| productivity/handoff/SKILL.md | 34 | keep | bosskuai-handoff |
| productivity/teach/SKILL.md | 35 | add | bosskuai-teach |
| productivity/to-questionnaire/SKILL.md | 36 | add | bosskuai-stakeholder-questionnaire |
| productivity/wait-what/SKILL.md | 37 | enhance | malaysia-localisation |
| productivity/writing-for-agents/SKILL.md | 38 | enhance | bosskuai-skill-creator |

## Complete agency persona decisions

| Source under agency-agents/ | Quote | Decision | Owner |
|---|---:|---|---|
| academic/academic-anthropologist.md | 39 | add | bosskuai-cultural-worldbuilding |
| academic/academic-geographer.md | 40 | add | bosskuai-geographic-worldbuilding |
| academic/academic-historian.md | 41 | add | bosskuai-historical-coherence |
| academic/academic-narratologist.md | 42 | add | bosskuai-narrative-analysis |
| academic/academic-psychologist.md | 43 | add | bosskuai-character-psychology |
| academic/academic-statistician.md | 44 | enhance | ab-testing |
| design/design-brand-guardian.md | 45 | overlap | brandkit |
| design/design-image-prompt-engineer.md | 46 | overlap | image |
| design/design-inclusive-visuals-specialist.md | 47 | enhance | image |
| design/design-persona-walkthrough.md | 48 | enhance | cro |
| design/design-ui-designer.md | 49 | overlap | bosskuai-ui-ux-design-to-code |
| design/design-ui-finish-gate-reviewer.md | 50 | overlap | antislop-ui |
| design/design-ux-architect.md | 51 | overlap | bosskuai-design-systems |
| design/design-ux-researcher.md | 52 | overlap | customer-research |
| design/design-visual-storyteller.md | 53 | overlap | content-strategy |
| design/design-whimsy-injector.md | 54 | add | bosskuai-ui-personality |
| engineering/engineering-ai-data-remediation-engineer.md | 55 | add | bosskuai-data-remediation |
| engineering/engineering-ai-engineer.md | 56 | add | bosskuai-ml-engineering |
| engineering/engineering-api-platform-engineer.md | 57 | enhance | bosskuai-api-design |
| engineering/engineering-ats-validator-architect.md | 58 | add | bosskuai-ats-validator-architect |
| engineering/engineering-autonomous-optimization-architect.md | 59 | enhance | bosskuai-autonomous-loops |
| engineering/engineering-backend-architect.md | 60 | overlap | bosskuai-software-architecture |
| engineering/engineering-china-network-engineer.md | 61 | add | bosskuai-network-engineering |
| engineering/engineering-cms-developer.md | 62 | add | bosskuai-cms-development |
| engineering/engineering-code-reviewer.md | 63 | overlap | bosskuai-rigorous-code-review |
| engineering/engineering-codebase-onboarding-engineer.md | 64 | overlap | bosskuai-project-understanding |
| engineering/engineering-data-engineer.md | 65 | add | bosskuai-data-pipelines |
| engineering/engineering-data-visualization-engineer.md | 66 | enhance | bosskuai-analytics-metrics |
| engineering/engineering-database-optimizer.md | 67 | overlap | bosskuai-database-engineering |
| engineering/engineering-database-reliability-engineer.md | 68 | enhance | bosskuai-database-engineering |
| engineering/engineering-desktop-app-engineer.md | 69 | add | bosskuai-desktop-apps |
| engineering/engineering-developer-tooling-engineer.md | 70 | enhance | bosskuai-polyglot-engineering |
| engineering/engineering-devops-automator.md | 71 | overlap | bosskuai-devops-iac |
| engineering/engineering-drupal-performance.md | 72 | add | bosskuai-drupal-performance |
| engineering/engineering-drupal-shopping-cart.md | 73 | add | bosskuai-drupal-commerce |
| engineering/engineering-email-intelligence-engineer.md | 74 | add | bosskuai-email-intelligence |
| engineering/engineering-embedded-firmware-engineer.md | 75 | add | bosskuai-embedded-firmware |
| engineering/engineering-feishu-integration-developer.md | 76 | add | bosskuai-feishu-integration |
| engineering/engineering-filament-optimization-specialist.md | 77 | enhance | bosskuai-laravel-development |
| engineering/engineering-finops-engineer.md | 78 | enhance | bosskuai-cost-optimization |
| engineering/engineering-frontend-developer.md | 79 | overlap | bosskuai-react-development |
| engineering/engineering-gaussdb-expert.md | 80 | add | bosskuai-gaussdb |
| engineering/engineering-git-workflow-master.md | 81 | overlap | bosskuai-github-workflow |
| engineering/engineering-i18n-engineer.md | 82 | enhance | bosskuai-i18n-l10n |
| engineering/engineering-identity-access-engineer.md | 83 | enhance | bosskuai-tenant-isolation-security |
| engineering/engineering-incident-response-commander.md | 84 | overlap | bosskuai-incident-response |
| engineering/engineering-iot-fleet-engineer.md | 85 | add | bosskuai-iot-fleets |
| engineering/engineering-it-service-manager.md | 86 | add | bosskuai-it-service-management |
| engineering/engineering-knowledge-graph-engineer.md | 87 | overlap | graphify |
| engineering/engineering-llm-post-training-engineer.md | 88 | add | bosskuai-llm-post-training |
| engineering/engineering-minimal-change-engineer.md | 89 | overlap | minimal-fix |
| engineering/engineering-mobile-app-builder.md | 90 | enhance | bosskuai-expo-react-native |
| engineering/engineering-mobile-release-engineer.md | 91 | overlap | bosskuai-mobile-app-release |
| engineering/engineering-multi-agent-systems-architect.md | 92 | overlap | bosskuai-agent-architecture-audit |
| engineering/engineering-network-engineer.md | 93 | add | bosskuai-network-engineering |
| engineering/engineering-orgscript-engineer.md | 94 | add | bosskuai-orgscript |
| engineering/engineering-payments-billing-engineer.md | 95 | enhance | bosskuai-saas-billing-ops |
| engineering/engineering-pdf-engine-architect.md | 96 | add | bosskuai-document-compilation |
| engineering/engineering-platform-engineer.md | 97 | add | bosskuai-platform-engineering |
| engineering/engineering-privacy-engineer.md | 98 | enhance | bosskuai-malaysia-pdpa-privacy |
| engineering/engineering-prompt-engineer.md | 99 | overlap | bosskuai-prompt-optimizer |
| engineering/engineering-rag-pipeline-engineer.md | 100 | add | bosskuai-rag-pipelines |
| engineering/engineering-rapid-prototyper.md | 101 | overlap | bosskuai-rapid-prototype |
| engineering/engineering-realtime-collaboration-engineer.md | 102 | add | bosskuai-realtime-collaboration |
| engineering/engineering-rust-refactoring-specialist.md | 103 | add | bosskuai-rust-refactoring |
| engineering/engineering-search-relevance-engineer.md | 104 | add | bosskuai-search-relevance |
| engineering/engineering-section-508-specialist.md | 105 | add | bosskuai-section-508-specialist |
| engineering/engineering-senior-developer.md | 106 | overlap | bosskuai-laravel-development |
| engineering/engineering-servicenow-developer-mentor.md | 107 | add | bosskuai-servicenow |
| engineering/engineering-software-architect.md | 108 | overlap | bosskuai-software-architecture |
| engineering/engineering-solidity-smart-contract-engineer.md | 109 | add | bosskuai-solidity |
| engineering/engineering-sre.md | 110 | overlap | bosskuai-observability-sre |
| engineering/engineering-technical-writer.md | 111 | enhance | bosskuai-documentation-lookup |
| engineering/engineering-universal-document-compiler.md | 112 | add | bosskuai-document-compilation |
| engineering/engineering-uswds-developer.md | 113 | add | bosskuai-uswds |
| engineering/engineering-video-streaming-engineer.md | 114 | add | bosskuai-video-streaming |
| engineering/engineering-voice-ai-integration-engineer.md | 115 | add | bosskuai-speech-transcription |
| engineering/engineering-webassembly-engineer.md | 116 | add | bosskuai-webassembly |
| engineering/engineering-wechat-mini-program-developer.md | 117 | add | bosskuai-wechat-mini-programs |
| engineering/engineering-wordpress-performance.md | 118 | add | bosskuai-wordpress-performance |
| engineering/engineering-wordpress-shopping-cart.md | 119 | add | bosskuai-woocommerce |
| finance/finance-bookkeeper-controller.md | 120 | add | bosskuai-bookkeeping |
| finance/finance-financial-analyst.md | 121 | overlap | bosskuai-financial-modeling |
| finance/finance-fpa-analyst.md | 122 | overlap | bosskuai-financial-modeling |
| finance/finance-investment-researcher.md | 123 | add | bosskuai-investment-research |
| finance/finance-tax-strategist.md | 124 | add | bosskuai-tax-planning |
| game-development/blender/blender-addon-engineer.md | 125 | add | bosskuai-blender-addon-engineer |
| game-development/economy-designer.md | 126 | add | bosskuai-economy-designer |
| game-development/game-audio-engineer.md | 127 | add | bosskuai-game-audio-engineer |
| game-development/game-designer.md | 128 | add | bosskuai-game-designer |
| game-development/godot/godot-gameplay-scripter.md | 129 | add | bosskuai-godot-gameplay-scripter |
| game-development/godot/godot-multiplayer-engineer.md | 130 | add | bosskuai-godot-multiplayer-engineer |
| game-development/godot/godot-shader-developer.md | 131 | add | bosskuai-godot-shader-developer |
| game-development/level-designer.md | 132 | add | bosskuai-level-designer |
| game-development/narrative-designer.md | 133 | add | bosskuai-narrative-designer |
| game-development/roblox-studio/roblox-avatar-creator.md | 134 | add | bosskuai-roblox-avatar-creator |
| game-development/roblox-studio/roblox-experience-designer.md | 135 | add | bosskuai-roblox-experience-designer |
| game-development/roblox-studio/roblox-systems-scripter.md | 136 | add | bosskuai-roblox-systems-scripter |
| game-development/technical-artist.md | 137 | add | bosskuai-technical-artist |
| game-development/unity/unity-architect.md | 138 | add | bosskuai-unity-architect |
| game-development/unity/unity-editor-tool-developer.md | 139 | add | bosskuai-unity-editor-tool-developer |
| game-development/unity/unity-multiplayer-engineer.md | 140 | add | bosskuai-unity-multiplayer-engineer |
| game-development/unity/unity-shader-graph-artist.md | 141 | add | bosskuai-unity-shader-graph-artist |
| game-development/unreal-engine/unreal-multiplayer-architect.md | 142 | add | bosskuai-unreal-multiplayer-architect |
| game-development/unreal-engine/unreal-systems-engineer.md | 143 | add | bosskuai-unreal-systems-engineer |
| game-development/unreal-engine/unreal-technical-artist.md | 144 | add | bosskuai-unreal-technical-artist |
| game-development/unreal-engine/unreal-world-builder.md | 145 | add | bosskuai-unreal-world-builder |
| gis/gis-3d-scene-developer.md | 146 | add | bosskuai-gis-3d-scene-developer |
| gis/gis-analyst.md | 147 | add | bosskuai-gis-analyst |
| gis/gis-bim-specialist.md | 148 | add | bosskuai-gis-bim-specialist |
| gis/gis-cartography-designer.md | 149 | add | bosskuai-gis-cartography-designer |
| gis/gis-drone-reality-mapping.md | 150 | add | bosskuai-gis-drone-reality-mapping |
| gis/gis-geoai-ml-engineer.md | 151 | add | bosskuai-gis-geoai-ml-engineer |
| gis/gis-geoprocessing-specialist.md | 152 | add | bosskuai-gis-geoprocessing-specialist |
| gis/gis-qa-engineer.md | 153 | add | bosskuai-gis-qa-engineer |
| gis/gis-solution-engineer.md | 154 | add | bosskuai-gis-solution-engineer |
| gis/gis-spatial-data-engineer.md | 155 | add | bosskuai-gis-spatial-data-engineer |
| gis/gis-spatial-data-scientist.md | 156 | add | bosskuai-gis-spatial-data-scientist |
| gis/gis-technical-consultant.md | 157 | add | bosskuai-gis-technical-consultant |
| gis/gis-web-gis-developer.md | 158 | add | bosskuai-gis-web-gis-developer |
| healthcare/healthcare-clinical-evidence-agent.md | 159 | add | bosskuai-healthcare-clinical-evidence-agent |
| healthcare/healthcare-innovation-strategist.md | 160 | add | bosskuai-healthcare-innovation-strategist |
| healthcare/healthcare-sovereign-health-systems-agent.md | 161 | add | bosskuai-healthcare-sovereign-health-systems-agent |
| marketing/marketing-aeo-foundations.md | 162 | overlap | ai-seo |
| marketing/marketing-agentic-search-optimizer.md | 163 | overlap | ai-seo |
| marketing/marketing-ai-citation-strategist.md | 164 | overlap | ai-seo |
| marketing/marketing-app-store-optimizer.md | 165 | overlap | aso |
| marketing/marketing-baidu-seo-specialist.md | 166 | add | bosskuai-baidu-seo-specialist |
| marketing/marketing-bilibili-content-strategist.md | 167 | add | bosskuai-bilibili-content-strategist |
| marketing/marketing-book-co-author.md | 168 | add | bosskuai-book-writing |
| marketing/marketing-carousel-growth-engine.md | 169 | overlap | bosskuai-marketing-growth |
| marketing/marketing-china-ecommerce-operator.md | 170 | add | bosskuai-china-ecommerce-operator |
| marketing/marketing-china-market-localization-strategist.md | 171 | add | bosskuai-china-market-localization-strategist |
| marketing/marketing-content-creator.md | 172 | overlap | content-strategy |
| marketing/marketing-cross-border-ecommerce.md | 173 | add | bosskuai-cross-border-ecommerce |
| marketing/marketing-developer-community-builder.md | 174 | overlap | community-marketing |
| marketing/marketing-douyin-strategist.md | 175 | add | bosskuai-douyin-strategist |
| marketing/marketing-email-strategist.md | 176 | overlap | emails |
| marketing/marketing-global-podcast-strategist.md | 177 | add | bosskuai-podcast-production |
| marketing/marketing-growth-hacker.md | 178 | overlap | bosskuai-marketing-growth |
| marketing/marketing-instagram-curator.md | 179 | overlap | social |
| marketing/marketing-kuaishou-strategist.md | 180 | add | bosskuai-kuaishou-strategist |
| marketing/marketing-linkedin-content-creator.md | 181 | overlap | content-strategy |
| marketing/marketing-livestream-commerce-coach.md | 182 | add | bosskuai-livestream-commerce-coach |
| marketing/marketing-multi-platform-publisher.md | 183 | add | bosskuai-multi-platform-publisher |
| marketing/marketing-podcast-strategist.md | 184 | add | bosskuai-podcast-production |
| marketing/marketing-pr-communications-manager.md | 185 | overlap | public-relations |
| marketing/marketing-private-domain-operator.md | 186 | add | bosskuai-private-domain-operator |
| marketing/marketing-reddit-community-builder.md | 187 | overlap | community-marketing |
| marketing/marketing-seo-specialist.md | 188 | overlap | seo-audit |
| marketing/marketing-short-video-editing-coach.md | 189 | overlap | video |
| marketing/marketing-social-media-strategist.md | 190 | overlap | social |
| marketing/marketing-tiktok-strategist.md | 191 | overlap | social |
| marketing/marketing-twitter-engager.md | 192 | overlap | social |
| marketing/marketing-video-optimization-specialist.md | 193 | overlap | video |
| marketing/marketing-wechat-official-account.md | 194 | add | bosskuai-wechat-official-account |
| marketing/marketing-weibo-strategist.md | 195 | add | bosskuai-weibo-strategist |
| marketing/marketing-x-twitter-intelligence-analyst.md | 196 | overlap | social |
| marketing/marketing-xiaohongshu-specialist.md | 197 | add | bosskuai-xiaohongshu-specialist |
| marketing/marketing-zhihu-strategist.md | 198 | add | bosskuai-zhihu-strategist |
| paid-media/paid-media-auditor.md | 199 | overlap | ads |
| paid-media/paid-media-creative-strategist.md | 200 | overlap | ad-creative |
| paid-media/paid-media-paid-social-strategist.md | 201 | overlap | ads |
| paid-media/paid-media-ppc-strategist.md | 202 | overlap | ads |
| paid-media/paid-media-programmatic-buyer.md | 203 | overlap | ads |
| paid-media/paid-media-search-query-analyst.md | 204 | overlap | ads |
| paid-media/paid-media-tracking-specialist.md | 205 | overlap | analytics |
| product/product-behavioral-nudge-engine.md | 206 | overlap | marketing-psychology |
| product/product-dx-engineer.md | 207 | enhance | bosskuai-polyglot-engineering |
| product/product-feedback-synthesizer.md | 208 | enhance | customer-research |
| product/product-manager.md | 209 | overlap | bosskuai-product-strategy |
| product/product-sprint-prioritizer.md | 210 | overlap | bosskuai-planning-execution |
| product/product-trend-researcher.md | 211 | overlap | bosskuai-market-analysis |
| project-management/project-management-experiment-tracker.md | 212 | overlap | ab-testing |
| project-management/project-management-jira-workflow-steward.md | 213 | overlap | bosskuai-planning-execution |
| project-management/project-management-meeting-notes-specialist.md | 214 | overlap | bosskuai-planning-execution |
| project-management/project-management-project-shepherd.md | 215 | overlap | bosskuai-planning-execution |
| project-management/project-management-studio-operations.md | 216 | overlap | bosskuai-planning-execution |
| project-management/project-management-studio-producer.md | 217 | overlap | bosskuai-planning-execution |
| project-management/project-manager-senior.md | 218 | overlap | bosskuai-planning-execution |
| research/research-synthesist.md | 219 | overlap | bosskuai-deep-research |
| sales/sales-account-strategist.md | 220 | overlap | bosskuai-sales-strategy |
| sales/sales-coach.md | 221 | overlap | bosskuai-sales-strategy |
| sales/sales-deal-strategist.md | 222 | overlap | bosskuai-sales-strategy |
| sales/sales-discovery-coach.md | 223 | overlap | bosskuai-sales-strategy |
| sales/sales-engineer.md | 224 | overlap | bosskuai-sales-strategy |
| sales/sales-offer-lead-gen-strategist.md | 225 | overlap | offers |
| sales/sales-outbound-strategist.md | 226 | overlap | bosskuai-sales-strategy |
| sales/sales-pipeline-analyst.md | 227 | overlap | revops |
| sales/sales-proposal-strategist.md | 228 | overlap | bosskuai-sales-strategy |
| security/security-ai-generated-code-auditor.md | 229 | enhance | bosskuai-cybersecurity-risk |
| security/security-appsec-engineer.md | 230 | enhance | bosskuai-cybersecurity-risk |
| security/security-architect.md | 231 | enhance | bosskuai-cybersecurity-risk |
| security/security-blockchain-security-auditor.md | 232 | enhance | bosskuai-cybersecurity-risk |
| security/security-cloud-security-architect.md | 233 | enhance | bosskuai-cybersecurity-risk |
| security/security-compliance-auditor.md | 234 | enhance | bosskuai-cybersecurity-risk |
| security/security-incident-responder.md | 235 | enhance | bosskuai-cybersecurity-risk |
| security/security-penetration-tester.md | 236 | enhance | bosskuai-cybersecurity-risk |
| security/security-secrets-credential-engineer.md | 237 | enhance | bosskuai-cybersecurity-risk |
| security/security-senior-secops.md | 238 | enhance | bosskuai-cybersecurity-risk |
| security/security-threat-detection-engineer.md | 239 | enhance | bosskuai-cybersecurity-risk |
| security/security-threat-intelligence-analyst.md | 240 | enhance | bosskuai-cybersecurity-risk |
| spatial-computing/macos-spatial-metal-engineer.md | 241 | add | bosskuai-macos-spatial-metal-engineer |
| spatial-computing/terminal-integration-specialist.md | 242 | add | bosskuai-terminal-integration-specialist |
| spatial-computing/visionos-spatial-engineer.md | 243 | add | bosskuai-visionos-spatial-engineer |
| spatial-computing/xr-cockpit-interaction-specialist.md | 244 | add | bosskuai-xr-cockpit-interaction-specialist |
| spatial-computing/xr-immersive-developer.md | 245 | add | bosskuai-xr-immersive-developer |
| spatial-computing/xr-interface-architect.md | 246 | add | bosskuai-xr-interface-architect |
| specialized/accounts-payable-agent.md | 247 | add | bosskuai-accounts-payable-agent |
| specialized/agentic-identity-trust.md | 248 | enhance | bosskuai-agent-architecture-audit |
| specialized/agents-orchestrator.md | 249 | overlap | agents/orchestrator.md |
| specialized/automation-governance-architect.md | 250 | enhance | bosskuai-autonomous-loops |
| specialized/business-strategist.md | 251 | overlap | bosskuai-cto-strategy |
| specialized/change-management-consultant.md | 252 | add | bosskuai-change-management-consultant |
| specialized/chief-financial-officer.md | 253 | add | bosskuai-capital-allocation |
| specialized/corporate-training-designer.md | 254 | add | bosskuai-corporate-training-designer |
| specialized/customer-service.md | 255 | overlap | bosskuai-customer-success-support |
| specialized/customer-success-manager.md | 256 | overlap | bosskuai-customer-success-support |
| specialized/data-consolidation-agent.md | 257 | enhance | bosskuai-analytics-metrics |
| specialized/data-privacy-officer.md | 258 | overlap | bosskuai-malaysia-pdpa-privacy |
| specialized/esg-sustainability-officer.md | 259 | add | bosskuai-esg-sustainability-officer |
| specialized/government-digital-presales-consultant.md | 260 | add | bosskuai-government-digital-presales-consultant |
| specialized/grant-writer.md | 261 | add | bosskuai-grant-writer |
| specialized/healthcare-aging-parent-care-companion.md | 262 | add | bosskuai-healthcare-aging-parent-care-companion |
| specialized/healthcare-customer-service.md | 263 | add | bosskuai-healthcare-customer-service |
| specialized/healthcare-marketing-compliance.md | 264 | add | bosskuai-healthcare-marketing-compliance |
| specialized/hospitality-guest-services.md | 265 | add | bosskuai-hospitality-guest-services |
| specialized/hr-onboarding.md | 266 | add | bosskuai-hr-onboarding |
| specialized/identity-graph-operator.md | 267 | enhance | bosskuai-hindsight-memory |
| specialized/language-translator.md | 268 | add | bosskuai-spanish-english-translation |
| specialized/legal-billing-time-tracking.md | 269 | add | bosskuai-legal-billing-time-tracking |
| specialized/legal-client-intake.md | 270 | add | bosskuai-legal-client-intake |
| specialized/legal-document-review.md | 271 | add | bosskuai-legal-document-review |
| specialized/loan-officer-assistant.md | 272 | add | bosskuai-loan-officer-assistant |
| specialized/lsp-index-engineer.md | 273 | add | bosskuai-lsp-index-engineer |
| specialized/ma-integration-manager.md | 274 | add | bosskuai-ma-integration-manager |
| specialized/medical-billing-coding-specialist.md | 275 | add | bosskuai-medical-billing-coding-specialist |
| specialized/operations-manager.md | 276 | overlap | bosskuai-operations |
| specialized/organizational-psychologist.md | 277 | add | bosskuai-organizational-psychologist |
| specialized/personal-growth-mentor.md | 278 | add | bosskuai-personal-growth-mentor |
| specialized/real-estate-buyer-seller.md | 279 | add | bosskuai-real-estate-buyer-seller |
| specialized/recruitment-specialist.md | 280 | add | bosskuai-recruitment-specialist |
| specialized/report-distribution-agent.md | 281 | enhance | revops |
| specialized/resume-tailor.md | 282 | add | bosskuai-resume-tailor |
| specialized/retail-customer-returns.md | 283 | add | bosskuai-retail-customer-returns |
| specialized/sales-data-extraction-agent.md | 284 | enhance | revops |
| specialized/sales-outreach.md | 285 | overlap | cold-email |
| specialized/specialized-chief-of-staff.md | 286 | overlap | agents/orchestrator.md |
| specialized/specialized-civil-engineer.md | 287 | add | bosskuai-civil-engineer |
| specialized/specialized-codebase-archaeologist.md | 288 | enhance | bosskuai-codebase-analysis |
| specialized/specialized-cultural-intelligence-strategist.md | 289 | enhance | bosskuai-i18n-l10n |
| specialized/specialized-developer-advocate.md | 290 | overlap | community-marketing |
| specialized/specialized-document-generator.md | 291 | enhance | documents-tooling-reference |
| specialized/specialized-fedramp-rmf-compliance.md | 292 | add | bosskuai-fedramp-rmf-compliance |
| specialized/specialized-focus-music-architect.md | 293 | add | bosskuai-audio-prompting |
| specialized/specialized-french-consulting-market.md | 294 | add | bosskuai-french-consulting |
| specialized/specialized-korean-business-navigator.md | 295 | add | bosskuai-korean-business |
| specialized/specialized-master-plan-architect.md | 296 | overlap | agents/planner.md |
| specialized/specialized-mcp-builder.md | 297 | overlap | mcp-server-patterns |
| specialized/specialized-model-qa.md | 298 | enhance | bosskuai-eval-driven-agent-improvement |
| specialized/specialized-pricing-analyst.md | 299 | overlap | pricing |
| specialized/specialized-salesforce-architect.md | 300 | add | bosskuai-salesforce-architect |
| specialized/specialized-strategy-duel-agent.md | 301 | add | bosskuai-decision-games |
| specialized/specialized-workflow-architect.md | 302 | enhance | bosskuai-business-logic-review |
| specialized/study-abroad-advisor.md | 303 | add | bosskuai-study-abroad-advisor |
| specialized/supply-chain-strategist.md | 304 | add | bosskuai-supply-chain-strategist |
| specialized/zk-steward.md | 305 | overlap | bosskuai-permanent-memory-orchestration |
| support/support-analytics-reporter.md | 306 | overlap | bosskuai-analytics-metrics |
| support/support-executive-summary-generator.md | 307 | enhance | bosskuai-token-saver |
| support/support-finance-tracker.md | 308 | overlap | bosskuai-financial-modeling |
| support/support-infrastructure-maintainer.md | 309 | overlap | bosskuai-observability-sre |
| support/support-legal-compliance-checker.md | 310 | overlap | bosskuai-legal-compliance |
| support/support-support-responder.md | 311 | overlap | bosskuai-customer-success-support |
| testing/testing-accessibility-auditor.md | 312 | overlap | accessibility |
| testing/testing-api-tester.md | 313 | overlap | bosskuai-integration-testing |
| testing/testing-evidence-collector.md | 314 | overlap | bosskuai-product-verification |
| testing/testing-performance-benchmarker.md | 315 | overlap | bosskuai-performance-profiling |
| testing/testing-reality-checker.md | 316 | overlap | agents/final-reviewer.md |
| testing/testing-test-automation-engineer.md | 317 | overlap | e2e-testing |
| testing/testing-test-results-analyzer.md | 318 | overlap | bosskuai-qa-automation-strategy |
| testing/testing-tool-evaluator.md | 319 | overlap | bosskuai-tools |
| testing/testing-workflow-optimizer.md | 320 | overlap | bosskuai-operations |

## Actionable additions by workflow

| Proposed portable skill | Sources and method evidence | Priority |
|---|---|---|
| bosskuai-accounts-payable-agent | agency:specialized/accounts-payable-agent.md:22 (quote523) | P2 |
| bosskuai-ats-validator-architect | agency:engineering/engineering-ats-validator-architect.md:29 (quote427) | P2 |
| bosskuai-audio-prompting | agency:specialized/specialized-focus-music-architect.md:27 (quote551) | P2 |
| bosskuai-baidu-seo-specialist | agency:marketing/marketing-baidu-seo-specialist.md:20 (quote500) | P2 |
| bosskuai-bilibili-content-strategist | agency:marketing/marketing-bilibili-content-strategist.md:20 (quote501) | P2 |
| bosskuai-blender-addon-engineer | agency:game-development/blender/blender-addon-engineer.md:22 (quote463) | P2 |
| bosskuai-book-writing | agency:marketing/marketing-book-co-author.md:31 (quote502) | P2 |
| bosskuai-bookkeeping | agency:finance/finance-bookkeeper-controller.md:24 (quote460) | P2 |
| bosskuai-change-management-consultant | agency:specialized/change-management-consultant.md:47 (quote524) | P2 |
| bosskuai-character-psychology | agency:academic/academic-psychologist.md:22 (quote423) | P2 |
| bosskuai-capital-allocation | agency:specialized/chief-financial-officer.md:20 (quote525) | P2 |
| bosskuai-china-ecommerce-operator | agency:marketing/marketing-china-ecommerce-operator.md:20 (quote503) | P2 |
| bosskuai-china-market-localization-strategist | agency:marketing/marketing-china-market-localization-strategist.md:23 (quote504) | P2 |
| bosskuai-civil-engineer | agency:specialized/specialized-civil-engineer.md:25 (quote549) | P2 |
| bosskuai-cms-development | agency:engineering/engineering-cms-developer.md:38 (quote429) | P2 |
| bosskuai-corporate-training-designer | agency:specialized/corporate-training-designer.md:123 (quote526) | P2 |
| bosskuai-course-exercises | skills:misc/scaffold-exercises/SKILL.md:47 (quote416) | P2 |
| bosskuai-cross-border-ecommerce | agency:marketing/marketing-cross-border-ecommerce.md:95 (quote505) | P2 |
| bosskuai-cultural-worldbuilding | agency:academic/academic-anthropologist.md:22 (quote419) | P2 |
| bosskuai-data-pipelines | agency:engineering/engineering-data-engineer.md:22 (quote430) | P1 |
| bosskuai-data-remediation | agency:engineering/engineering-ai-data-remediation-engineer.md:33 (quote425) | P2 |
| bosskuai-decision-games | agency:specialized/specialized-strategy-duel-agent.md:18 (quote555) | P2 |
| bosskuai-desktop-apps | agency:engineering/engineering-desktop-app-engineer.md:22 (quote431) | P1 |
| bosskuai-document-compilation | agency:engineering/engineering-pdf-engine-architect.md:44 (quote443); agency:engineering/engineering-universal-document-compiler.md:42 (quote452) | P2 |
| bosskuai-douyin-strategist | agency:marketing/marketing-douyin-strategist.md:21 (quote506) | P2 |
| bosskuai-drupal-commerce | agency:engineering/engineering-drupal-shopping-cart.md:29 (quote433) | P2 |
| bosskuai-drupal-performance | agency:engineering/engineering-drupal-performance.md:29 (quote432) | P2 |
| bosskuai-economy-designer | agency:game-development/economy-designer.md:22 (quote464) | P2 |
| bosskuai-email-intelligence | agency:engineering/engineering-email-intelligence-engineer.md:24 (quote434) | P2 |
| bosskuai-embedded-firmware | agency:engineering/engineering-embedded-firmware-engineer.md:18 (quote435) | P2 |
| bosskuai-esg-sustainability-officer | agency:specialized/esg-sustainability-officer.md:30 (quote527) | P2 |
| bosskuai-fedramp-rmf-compliance | agency:specialized/specialized-fedramp-rmf-compliance.md:53 (quote550) | P2 |
| bosskuai-feishu-integration | agency:engineering/engineering-feishu-integration-developer.md:81 (quote436) | P2 |
| bosskuai-french-consulting | agency:specialized/specialized-french-consulting-market.md:18 (quote552) | P2 |
| bosskuai-game-audio-engineer | agency:game-development/game-audio-engineer.md:22 (quote465) | P2 |
| bosskuai-game-designer | agency:game-development/game-designer.md:23 (quote466) | P2 |
| bosskuai-gaussdb | agency:engineering/engineering-gaussdb-expert.md:101 (quote437) | P2 |
| bosskuai-geographic-worldbuilding | agency:academic/academic-geographer.md:22 (quote420) | P2 |
| bosskuai-gis-3d-scene-developer | agency:gis/gis-3d-scene-developer.md:22 (quote484) | P2 |
| bosskuai-gis-analyst | agency:gis/gis-analyst.md:22 (quote485) | P2 |
| bosskuai-gis-bim-specialist | agency:gis/gis-bim-specialist.md:23 (quote486) | P2 |
| bosskuai-gis-cartography-designer | agency:gis/gis-cartography-designer.md:22 (quote487) | P2 |
| bosskuai-gis-drone-reality-mapping | agency:gis/gis-drone-reality-mapping.md:22 (quote488) | P2 |
| bosskuai-gis-geoai-ml-engineer | agency:gis/gis-geoai-ml-engineer.md:43 (quote489) | P2 |
| bosskuai-gis-geoprocessing-specialist | agency:gis/gis-geoprocessing-specialist.md:22 (quote490) | P2 |
| bosskuai-gis-qa-engineer | agency:gis/gis-qa-engineer.md:22 (quote491) | P2 |
| bosskuai-gis-solution-engineer | agency:gis/gis-solution-engineer.md:23 (quote492) | P2 |
| bosskuai-gis-spatial-data-engineer | agency:gis/gis-spatial-data-engineer.md:22 (quote493) | P2 |
| bosskuai-gis-spatial-data-scientist | agency:gis/gis-spatial-data-scientist.md:22 (quote494) | P2 |
| bosskuai-gis-technical-consultant | agency:gis/gis-technical-consultant.md:23 (quote495) | P2 |
| bosskuai-gis-web-gis-developer | agency:gis/gis-web-gis-developer.md:22 (quote496) | P2 |
| bosskuai-godot-gameplay-scripter | agency:game-development/godot/godot-gameplay-scripter.md:22 (quote467) | P2 |
| bosskuai-godot-multiplayer-engineer | agency:game-development/godot/godot-multiplayer-engineer.md:22 (quote468) | P2 |
| bosskuai-godot-shader-developer | agency:game-development/godot/godot-shader-developer.md:22 (quote469) | P2 |
| bosskuai-government-digital-presales-consultant | agency:specialized/government-digital-presales-consultant.md:24 (quote528) | P2 |
| bosskuai-grant-writer | agency:specialized/grant-writer.md:44 (quote529) | P2 |
| bosskuai-healthcare-aging-parent-care-companion | agency:specialized/healthcare-aging-parent-care-companion.md:45 (quote530) | P2 |
| bosskuai-healthcare-clinical-evidence-agent | agency:healthcare/healthcare-clinical-evidence-agent.md:25 (quote497) | P2 |
| bosskuai-healthcare-customer-service | agency:specialized/healthcare-customer-service.md:42 (quote531) | P2 |
| bosskuai-healthcare-innovation-strategist | agency:healthcare/healthcare-innovation-strategist.md:50 (quote498) | P2 |
| bosskuai-healthcare-marketing-compliance | agency:specialized/healthcare-marketing-compliance.md:39 (quote532) | P2 |
| bosskuai-healthcare-sovereign-health-systems-agent | agency:healthcare/healthcare-sovereign-health-systems-agent.md:60 (quote499) | P2 |
| bosskuai-historical-coherence | agency:academic/academic-historian.md:22 (quote421) | P2 |
| bosskuai-hospitality-guest-services | agency:specialized/hospitality-guest-services.md:33 (quote533) | P2 |
| bosskuai-hr-onboarding | agency:specialized/hr-onboarding.md:43 (quote534) | P2 |
| bosskuai-human-setup-wizard | skills:engineering/wizard/SKILL.md:20 (quote414) | P2 |
| bosskuai-investment-research | agency:finance/finance-investment-researcher.md:29 (quote461) | P2 |
| bosskuai-iot-fleets | agency:engineering/engineering-iot-fleet-engineer.md:21 (quote438) | P2 |
| bosskuai-issue-tracker-setup | skills:engineering/setup-matt-pocock-skills/SKILL.md:36 (quote413) | P2 |
| bosskuai-it-service-management | agency:engineering/engineering-it-service-manager.md:28 (quote439) | P2 |
| bosskuai-korean-business | agency:specialized/specialized-korean-business-navigator.md:19 (quote553) | P2 |
| bosskuai-kuaishou-strategist | agency:marketing/marketing-kuaishou-strategist.md:20 (quote508) | P2 |
| bosskuai-legal-billing-time-tracking | agency:specialized/legal-billing-time-tracking.md:44 (quote536) | P2 |
| bosskuai-legal-client-intake | agency:specialized/legal-client-intake.md:43 (quote537) | P2 |
| bosskuai-legal-document-review | agency:specialized/legal-document-review.md:41 (quote538) | P2 |
| bosskuai-level-designer | agency:game-development/level-designer.md:22 (quote470) | P2 |
| bosskuai-livestream-commerce-coach | agency:marketing/marketing-livestream-commerce-coach.md:81 (quote509) | P2 |
| bosskuai-llm-post-training | agency:engineering/engineering-llm-post-training-engineer.md:24 (quote440) | P2 |
| bosskuai-loan-officer-assistant | agency:specialized/loan-officer-assistant.md:28 (quote539) | P2 |
| bosskuai-lsp-index-engineer | agency:specialized/lsp-index-engineer.md:22 (quote540) | P2 |
| bosskuai-ma-integration-manager | agency:specialized/ma-integration-manager.md:29 (quote541) | P2 |
| bosskuai-macos-spatial-metal-engineer | agency:spatial-computing/macos-spatial-metal-engineer.md:22 (quote517) | P2 |
| bosskuai-medical-billing-coding-specialist | agency:specialized/medical-billing-coding-specialist.md:46 (quote542) | P2 |
| bosskuai-ml-engineering | agency:engineering/engineering-ai-engineer.md:22 (quote426) | P2 |
| bosskuai-multi-platform-publisher | agency:marketing/marketing-multi-platform-publisher.md:41 (quote510) | P2 |
| bosskuai-narrative-analysis | agency:academic/academic-narratologist.md:22 (quote422) | P2 |
| bosskuai-narrative-designer | agency:game-development/narrative-designer.md:22 (quote471) | P2 |
| bosskuai-network-engineering | agency:engineering/engineering-china-network-engineer.md:31 (quote428); agency:engineering/engineering-network-engineer.md:18 (quote441) | P2 |
| bosskuai-organizational-psychologist | agency:specialized/organizational-psychologist.md:28 (quote543) | P2 |
| bosskuai-orgscript | agency:engineering/engineering-orgscript-engineer.md:22 (quote442) | P2 |
| bosskuai-personal-growth-mentor | agency:specialized/personal-growth-mentor.md:20 (quote544) | P2 |
| bosskuai-platform-engineering | agency:engineering/engineering-platform-engineer.md:24 (quote444) | P2 |
| bosskuai-podcast-production | agency:marketing/marketing-global-podcast-strategist.md:21 (quote507); agency:marketing/marketing-podcast-strategist.md:133 (quote511) | P2 |
| bosskuai-private-domain-operator | agency:marketing/marketing-private-domain-operator.md:71 (quote512) | P2 |
| bosskuai-rag-pipelines | agency:engineering/engineering-rag-pipeline-engineer.md:30 (quote445) | P1 |
| bosskuai-real-estate-buyer-seller | agency:specialized/real-estate-buyer-seller.md:43 (quote545) | P2 |
| bosskuai-realtime-collaboration | agency:engineering/engineering-realtime-collaboration-engineer.md:20 (quote446) | P1 |
| bosskuai-recruitment-specialist | agency:specialized/recruitment-specialist.md:35 (quote546) | P2 |
| bosskuai-resume-tailor | agency:specialized/resume-tailor.md:24 (quote547) | P2 |
| bosskuai-retail-customer-returns | agency:specialized/retail-customer-returns.md:28 (quote548) | P2 |
| bosskuai-roblox-avatar-creator | agency:game-development/roblox-studio/roblox-avatar-creator.md:22 (quote472) | P2 |
| bosskuai-roblox-experience-designer | agency:game-development/roblox-studio/roblox-experience-designer.md:22 (quote473) | P2 |
| bosskuai-roblox-systems-scripter | agency:game-development/roblox-studio/roblox-systems-scripter.md:22 (quote474) | P2 |
| bosskuai-rust-refactoring | agency:engineering/engineering-rust-refactoring-specialist.md:31 (quote447) | P2 |
| bosskuai-salesforce-architect | agency:specialized/specialized-salesforce-architect.md:18 (quote554) | P2 |
| bosskuai-search-relevance | agency:engineering/engineering-search-relevance-engineer.md:20 (quote448) | P1 |
| bosskuai-section-508-specialist | agency:engineering/engineering-section-508-specialist.md:31 (quote449) | P2 |
| bosskuai-servicenow | agency:engineering/engineering-servicenow-developer-mentor.md:23 (quote450) | P2 |
| bosskuai-solidity | agency:engineering/engineering-solidity-smart-contract-engineer.md:23 (quote451) | P2 |
| bosskuai-spanish-english-translation | agency:specialized/language-translator.md:26 (quote535) | P2 |
| bosskuai-speech-transcription | agency:engineering/engineering-voice-ai-integration-engineer.md:24 (quote455) | P2 |
| bosskuai-stakeholder-questionnaire | skills:productivity/to-questionnaire/SKILL.md:12 (quote418) | P2 |
| bosskuai-study-abroad-advisor | agency:specialized/study-abroad-advisor.md:23 (quote556) | P2 |
| bosskuai-supply-chain-strategist | agency:specialized/supply-chain-strategist.md:24 (quote557) | P2 |
| bosskuai-tax-planning | agency:finance/finance-tax-strategist.md:34 (quote462) | P2 |
| bosskuai-teach | skills:productivity/teach/SKILL.md:18 (quote417) | P2 |
| bosskuai-technical-artist | agency:game-development/technical-artist.md:22 (quote475) | P2 |
| bosskuai-terminal-integration-specialist | agency:spatial-computing/terminal-integration-specialist.md:18 (quote518) | P2 |
| bosskuai-typescript-module-boundaries | skills:in-progress/setup-ts-deep-modules/SKILL.md:69 (quote415) | P2 |
| bosskuai-ui-personality | agency:design/design-whimsy-injector.md:23 (quote424) | P2 |
| bosskuai-unity-architect | agency:game-development/unity/unity-architect.md:23 (quote476) | P2 |
| bosskuai-unity-editor-tool-developer | agency:game-development/unity/unity-editor-tool-developer.md:22 (quote477) | P2 |
| bosskuai-unity-multiplayer-engineer | agency:game-development/unity/unity-multiplayer-engineer.md:22 (quote478) | P2 |
| bosskuai-unity-shader-graph-artist | agency:game-development/unity/unity-shader-graph-artist.md:24 (quote479) | P2 |
| bosskuai-unreal-multiplayer-architect | agency:game-development/unreal-engine/unreal-multiplayer-architect.md:22 (quote480) | P2 |
| bosskuai-unreal-systems-engineer | agency:game-development/unreal-engine/unreal-systems-engineer.md:22 (quote481) | P2 |
| bosskuai-unreal-technical-artist | agency:game-development/unreal-engine/unreal-technical-artist.md:23 (quote482) | P2 |
| bosskuai-unreal-world-builder | agency:game-development/unreal-engine/unreal-world-builder.md:22 (quote483) | P2 |
| bosskuai-uswds | agency:engineering/engineering-uswds-developer.md:31 (quote453) | P2 |
| bosskuai-video-streaming | agency:engineering/engineering-video-streaming-engineer.md:20 (quote454) | P2 |
| bosskuai-visionos-spatial-engineer | agency:spatial-computing/visionos-spatial-engineer.md:36 (quote519) | P2 |
| bosskuai-webassembly | agency:engineering/engineering-webassembly-engineer.md:23 (quote456) | P2 |
| bosskuai-wechat-mini-programs | agency:engineering/engineering-wechat-mini-program-developer.md:23 (quote457) | P2 |
| bosskuai-wechat-official-account | agency:marketing/marketing-wechat-official-account.md:27 (quote513) | P2 |
| bosskuai-weibo-strategist | agency:marketing/marketing-weibo-strategist.md:76 (quote514) | P2 |
| bosskuai-woocommerce | agency:engineering/engineering-wordpress-shopping-cart.md:29 (quote459) | P2 |
| bosskuai-wordpress-performance | agency:engineering/engineering-wordpress-performance.md:31 (quote458) | P2 |
| bosskuai-xiaohongshu-specialist | agency:marketing/marketing-xiaohongshu-specialist.md:27 (quote515) | P2 |
| bosskuai-xr-cockpit-interaction-specialist | agency:spatial-computing/xr-cockpit-interaction-specialist.md:22 (quote520) | P2 |
| bosskuai-xr-immersive-developer | agency:spatial-computing/xr-immersive-developer.md:23 (quote521) | P2 |
| bosskuai-xr-interface-architect | agency:spatial-computing/xr-interface-architect.md:22 (quote522) | P2 |
| bosskuai-zhihu-strategist | agency:marketing/marketing-zhihu-strategist.md:22 (quote516) | P2 |
