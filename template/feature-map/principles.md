# Principles

Rules that apply to every feature. A spec does not repeat them; it only states where it needs an exception, and an exception needs a decision record in [decisions/](decisions/).

The principles below are examples taken from a production app. Keep the ones that hold for your product, change the rest, and keep their IDs stable once agents and tests cite them.

| ID | Principle |
|---|---|
| PRIN-001 | Every client platform implements the same product behavior. A deliberate difference is listed in the spec's "Platform differences" table with its reason. |
| PRIN-002 | The backend decides every action. The app reads the caller's role only to decide what to show; it never treats a cached role as permission, and a refusal from the backend always wins. |
| PRIN-003 | Every user-visible text exists in each supported language: {{LANGUAGES}}. The app follows the device's language and falls back to {{DEFAULT_LANGUAGE}}. |
| PRIN-004 | A screen shows what the backend holds. After a successful write, every screen that shows the changed data loads it again; the app never shows a value it guessed from its own write. |
| PRIN-005 | Usage analytics run only while the user's consent is granted. Analytics events and error reports carry no name, no email address and no message text; a person is identified by an id only. |
| PRIN-006 | Every screen meets the accessibility baseline: icon-only buttons have labels, states differ by text and shape as well as colour, touch targets are at least 44 × 44 pt on iOS and 48 × 48 dp on Android, and text wraps instead of being cut off at the largest text sizes. |
| PRIN-007 | Layouts work on phones, tablets and wide screens at the largest text sizes. Content never runs edge to edge on a wide screen. |
