# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.2.x   | :white_check_mark: |
| < 0.2   | :x:                |

## Reporting a Vulnerability

Please report security vulnerabilities by opening a [GitHub Security Advisory](https://github.com/olaflaitinen/citysense/security/advisories/new) or by emailing the maintainers privately.

Do not open public issues for security vulnerabilities.

## Response Timeline

- **Acknowledgment**: Within 48 hours
- **Initial assessment**: Within 7 days
- **Fix or mitigation**: Depends on severity; critical issues prioritised

## Best Practices

- Do not commit API keys, tokens, or credentials to the repository
- Use environment variables or `citysense.toml` (excluded from version control) for secrets
- Keep dependencies updated: `pip install -U -e ".[dev]"`
