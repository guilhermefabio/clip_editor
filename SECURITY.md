# Security

Run the Studio only on a trusted local machine. It is a local editing interface, not an authenticated public service. OAuth credentials, refresh tokens, SQLite feedback databases and source footage must stay private. Only load trusted model/joblib and NumPy cache artifacts.

Do not post credentials, private recordings or sensitive exploit details in public issues. Use GitHub private vulnerability reporting if the owner enables it; otherwise request a private reporting channel without including the sensitive material. No dedicated security mailbox or response-time commitment has been established.

If a real secret is discovered in Git history, revoke/rotate it before release and coordinate history cleanup with the owner. `.gitignore` and deleting the current file do not erase previous commits. Review both history and the final staged tree before making the repository public.
