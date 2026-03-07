# X API v2 Sample Code

[![X API v2](https://img.shields.io/endpoint?url=https%3A%2F%2Ftwbadges.glitch.me%2Fbadges%2Fv2)](https://developer.x.com/en/docs/twitter-api)

Working code samples for the **X API v2** in Python, JavaScript, Ruby, Java, and R.

## 📁 Repository Structure

```
├── python/           # 65 Python examples
├── javascript/       # 59 JavaScript examples  
├── ruby/             # 58 Ruby examples
├── java/             # 19 Java examples
├── r/                # 5 R examples
├── llms.txt          # LLM-friendly documentation
└── api-index.json    # Machine-readable endpoint catalog
```

## 🚀 Quick Start

### 1. Get API Credentials

Sign up at the [X Developer Portal](https://developer.x.com/en/portal/dashboard).

### 2. Set Environment Variables

**For read-only operations (search, lookup):**
```bash
export BEARER_TOKEN='your_bearer_token'
```

**For user actions (post, like, repost, bookmark, etc.):**
```bash
export CLIENT_ID='your_client_id'
export CLIENT_SECRET='your_client_secret'
```

**For OAuth 1.0a (legacy endpoints):**
```bash
export CONSUMER_KEY='your_consumer_key'
export CONSUMER_SECRET='your_consumer_secret'
```

### 3. Run an Example

```bash
# Python
cd python && pip install -r requirements.txt
python posts/search_recent.py

# JavaScript  
cd javascript
node posts/search_recent.js

# Ruby
cd ruby && bundle install
ruby posts/search_recent.rb

# Java
cd java
javac -cp ".:lib/*" posts/RecentSearchDemo.java
java -cp ".:lib/*" RecentSearchDemo
```

## 📚 Examples by Category

| Category | Python | JavaScript | Ruby | Java | R |
|----------|--------|------------|------|------|---|
| Posts (search, create, delete, likes, reposts) | ✅ | ✅ | ✅ | ✅ | ✅ |
| Users (lookup, followers, following, blocks, mutes) | ✅ | ✅ | ✅ | ✅ | ✅ |
| Timelines (user, mentions, home) | ✅ | ✅ | ✅ | ✅ | |
| Streams (filtered, sampled) | ✅ | ✅ | ✅ | ✅ | |
| Lists (lookup, manage, members, follow) | ✅ | ✅ | ✅ | | |
| Spaces (lookup, search) | ✅ | ✅ | ✅ | ✅ | |
| Bookmarks | ✅ | ✅ | ✅ | | |
| Direct Messages | ✅ | | | | |
| Media Upload | ✅ | | | | |
| Compliance | ✅ | ✅ | | | |
| Usage | ✅ | ✅ | | ✅ | |

## 🔐 Authentication

| Type | Use Case | Env Vars |
|------|----------|----------|
| Bearer Token | Read-only (search, lookup) | `BEARER_TOKEN` |
| OAuth 2.0 PKCE | User actions (post, like, repost, bookmark, mute, etc.) | `CLIENT_ID`, `CLIENT_SECRET` |
| OAuth 1.0a | Legacy endpoints (if applicable) | `CONSUMER_KEY`, `CONSUMER_SECRET` |

## 🤖 For LLMs

- **`llms.txt`** - Context file for AI assistants
- **`api-index.json`** - Machine-readable endpoint catalog

## 🔗 Resources

- [X API Documentation](https://developer.x.com/en/docs/twitter-api)
- [Developer Portal](https://developer.x.com/en/portal/dashboard)

## 📄 License

Apache 2.0
