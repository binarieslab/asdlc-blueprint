# Glossary

Use these terms exactly as written in specs. Add a term here before using it in more than one spec. The terms below are examples; replace them with your product's.

| Term | Meaning |
|---|---|
| {{PROJECT_NAME}} | The product's name as users see it in the stores and in the app's texts. |
| App | The client in this repository, on every platform it ships to. In an "Applies to" column it means all of them. |
| Account | A person's identity: an email address and a password. One account can be used on many devices. |
| Login | A signed-in session of an account on one device. It ends when the user signs out or the backend ends it. |
| Token | The credential the backend issues at sign-in; the app stores it and sends it on every signed-in request. |
| Role | What a person may do. The backend decides every action; the app reads the role only to decide what to show ([principles](principles.md), PRIN-002). |
