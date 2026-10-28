# Live threat intel

Query these at review time. Record the source and the date of each result. Training data goes stale; a feed result beats memory every time.

## Free feeds (no key needed)

| Feed | Use it for | How |
|------|-----------|-----|
| OSV.dev | Is this package version affected? Covers npm, PyPI, Go, Maven, crates.io, RubyGems, Packagist and more | `curl -s -d '{"package":{"name":"<name>","ecosystem":"<Ecosystem>"},"version":"<version>"}' https://api.osv.dev/v1/query` |
| GitHub Advisory Database | Reviewed advisories and malware by ecosystem, package, severity, date or EPSS | `gh api "/advisories?ecosystem=npm&affects=<pkg>@<version>"`; newest in your ecosystem: `gh api "/advisories?ecosystem=npm&sort=published&direction=desc&per_page=20"`; malicious packages: add `&type=malware` |
| CISA KEV | Is this CVE exploited in the wild right now? A KEV hit in your stack is urgent | `curl -s https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json` and filter on `cveID`, `vendorProject`, `product` |

Gotchas:

- OSV ecosystem names are case-sensitive (`PyPI`, not `pypi`). Give the version in `version` or in a versioned purl, not both, or the API returns 400.
- `gh api` needs `gh auth login`. If it is not signed in, say so and use OSV only.
- An advisory with no fixed version still matters: note the workaround or the exposure, not just "no patch".

## Scanners (use only if already installed)

| Stack | Command |
|-------|---------|
| Any (lockfiles, SBOMs) | `osv-scanner scan source -r .` |
| npm / pnpm / yarn | `npm audit --omit=dev` / `pnpm audit --prod` / `yarn npm audit` |
| Python | `pip-audit` |
| PHP | `composer audit` |
| Go | `govulncheck ./...` |
| Rust | `cargo audit` |
| Containers and IaC | `trivy fs .` / `trivy image <image>` |
| Secrets in git | `gitleaks detect` |

If none is installed, query the feeds directly and list the scanner you would add as a recommendation. Do not install it without the user's go-ahead.

## Variant hunt from a new advisory

1. Read the advisory's root cause: the sink, the missing check, or the misused API (its CWE helps).
2. Search your code for the same shape: `grep` or `graft grep` for the function, the option name, the unsafe default.
3. Check each hit's reachability from untrusted input. List it as fixed, a finding, or not reachable with the reason.
4. If your code wraps or forks the affected library, check your copy too; scanners only see the manifest.
