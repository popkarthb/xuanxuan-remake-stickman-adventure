# AGENTS.md

## Repository Purpose

This is a **public open-source repository** for **Stickman Adventure / 火柴人大冒险**.

Everything committed to this repository must be safe for public viewing, copying, indexing, redistribution, and permanent archival.

## Public Repository Rule

Treat every file, commit, issue, pull request, comment, screenshot, log, test fixture, and example in this repository as fully public.

Do **not** commit private, personal, confidential, proprietary, credentialed, or otherwise non-public information.

## Never Commit

Do not add any of the following:

- Real private names or personally identifying information unless intentionally published for the project
- Home, work, or private addresses
- Personal phone numbers or private email addresses
- Account numbers, payment information, financial information, or transaction data
- Passwords, API keys, access tokens, cookies, session IDs, private keys, certificates, or authentication secrets
- Private repository URLs or credentials
- Internal company information, internal systems, internal hostnames, non-public IP addresses, or proprietary documentation
- Personal chat history, personal events, travel details, schedules, or other private life information
- Local paths that expose personal usernames or private directory structures when unnecessary
- Raw logs containing identifiers, tokens, device information, user data, or other sensitive values
- Screenshots containing notifications, account names, desktop content, browser tabs, file paths, email addresses, or other private information

## Sanitization Requirement

Before committing any content:

1. Assume the content will be visible to anyone on the Internet.
2. Remove or replace all private and sensitive information.
3. Use generic placeholders where examples are necessary, such as:
   - `<REDACTED>`
   - `example@example.com`
   - `user-123`
   - `example-token`
4. Review screenshots and images separately for accidental information disclosure.
5. Do not rely on the repository being small or low-profile as a privacy control.

If content cannot be safely made public, **do not commit it to this repository**.

## Project Naming

The game name is:

- English: **Stickman Adventure**
- Chinese: **火柴人大冒险**
- Repository/project title: **萱萱小游戏：火柴人大冒险重制版**

Do not use map mechanics, room layouts, or individual level concepts as the game title.

## Development Guidance

- Keep changes focused and understandable.
- Preserve working behavior when refactoring.
- Test gameplay changes before committing them when practical.
- Keep public documentation aligned with the current game behavior.
- Keep room layouts, room connections, platforms, enemies, keys, switches, and other level-specific configuration in `levels.py` rather than embedding them in `main.py`.
- Keep reusable room/entity data structures in `models.py`; keep the main loop, physics, collision, combat, input, and rendering framework in `main.py`.
- Store README screenshots and other public project images under `image/`.
- Verify all image assets are safe for public release before committing them.
