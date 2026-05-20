# SQL Injection

SQL Injection (SQLi) is one of the most common and well-known web application vulnerabilities. It allows an attacker to interfere with the queries an application makes to its database — potentially reading, modifying, or deleting data they should not have access to.

> ⚠️ **This document is for educational purposes only.** All examples should be tested in controlled environments such as DVWA, SQLite local databases, or dedicated labs.

---

## How It Works

Web applications often take user input (login forms, search boxes, URLs) and pass it directly into a SQL query. If that input is not properly sanitized, an attacker can inject their own SQL code into the query.

**Normal flow:**
```
User types:   username = "admin"  password = "secret"
Query built:  SELECT * FROM users WHERE username='admin' AND password='secret'
```

**Injected flow:**
```
User types:   username = "admin'--"  password = ""
Query built:  SELECT * FROM users WHERE username='admin'--' AND password=''
```
The `--` is a SQL comment. Everything after it is ignored — the password check is completely bypassed.

---

## Example 1 — Authentication Bypass

**Vulnerable login query (Python-style pseudocode):**
```python
query = "SELECT * FROM users WHERE username='" + username + "' AND password='" + password + "'"
```

**Injected input:**
```
username: admin'--
password: (anything)
```

**Resulting query:**
```sql
SELECT * FROM users WHERE username='admin'--' AND password='anything'
```
The attacker logs in as `admin` without knowing the password.

---

## Example 2 — OR 1=1 (Always True)

**Injected input:**
```
username: ' OR 1=1--
password: (anything)
```

**Resulting query:**
```sql
SELECT * FROM users WHERE username='' OR 1=1--' AND password='anything'
```
`1=1` is always true — the query returns all rows. The attacker may get access to the first account in the database (often an admin).

---

## Example 3 — Data Extraction via UNION

If the attacker can append a `UNION` statement, they can pull data from other tables.

**Injected input:**
```
' UNION SELECT username, password FROM users--
```

**Resulting query:**
```sql
SELECT name, description FROM products WHERE id='' UNION SELECT username, password FROM users--'
```
This returns usernames and passwords from the `users` table alongside the normal product results.

---

## Example 4 — Destructive Query (DROP TABLE)

```sql
'; DROP TABLE users;--
```

**Resulting query:**
```sql
SELECT * FROM users WHERE username=''; DROP TABLE users;--'
```
If the database allows stacked queries, the `users` table is deleted. This is why SQLi is considered critical severity.

---

## How to Detect SQLi Vulnerability (Manual Testing)

Simple payloads to test if an input field is vulnerable:

| Payload | Expected behavior if vulnerable |
|---|---|
| `'` | Database error or broken page |
| `''` | Page returns to normal |
| `' OR 1=1--` | Returns all results / logs in |
| `' OR 1=2--` | Returns nothing / different result |

If results differ between `1=1` and `1=2`, the input is likely injectable.

---

## How to Defend Against SQL Injection

### ✅ 1. Prepared Statements (Parameterized Queries)
The most effective defense. User input is never treated as SQL code.

```python
# Vulnerable
query = "SELECT * FROM users WHERE username='" + username + "'"

# Safe — parameterized
cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
```

```php
// Safe in PHP (PDO)
$stmt = $pdo->prepare("SELECT * FROM users WHERE username = ?");
$stmt->execute([$username]);
```

### ✅ 2. Input Validation & Sanitization
Reject or escape unexpected characters (`'`, `"`, `;`, `--`, `/*`) before they reach the query.

### ✅ 3. Principle of Least Privilege
The database user used by the application should only have the permissions it actually needs — no `DROP`, no access to other tables.

### ✅ 4. Web Application Firewall (WAF)
A WAF can detect and block common SQLi patterns at the network level — useful as an additional layer, but not a substitute for secure coding.

### ✅ 5. Error Handling
Never expose raw database errors to the user. They reveal table names, query structure, and database type — all useful for an attacker.

---

## Tools Used for Testing

| Tool | Purpose |
|---|---|
| [DVWA](https://github.com/digininja/DVWA) | Intentionally vulnerable web app for safe SQLi practice |
| [SQLMap](https://sqlmap.org/) | Automated SQLi detection and exploitation |
| [Burp Suite](https://portswigger.net/burp) | Intercepting and modifying HTTP requests |
| Browser DevTools | Inspecting form inputs and URL parameters |

---

## References

- [OWASP SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection)
- [PortSwigger SQLi Labs](https://portswigger.net/web-security/sql-injection)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
