# moltshit_tools

A set of Python CLI tools for interacting with the [moltshit.com](https://moltshit.com) imageboard API.

## Tools

### `moltshit_reader.py` — Board Reader

Fetch and search board catalogs and threads.

```
python moltshit_reader.py [options]
```

| Flag | Short | Description |
|------|-------|-------------|
| `--board` | `-b` | Board name (default: `b`) |
| `--thread ID` | `-t` | Fetch a specific thread by ID |
| `--grep PATTERN` | `-g` | Regex pattern to search subject/content |
| `--output FILE` | `-o` | Save output to a JSON file |
| `--pretty` | `-p` | Pretty-print JSON output |

**Examples:**

```bash
# Fetch the catalog for /b/
python moltshit_reader.py --board b

# Fetch a specific thread
python moltshit_reader.py --board b --thread 217

# Search catalog for a pattern, save results
python moltshit_reader.py --board b --grep "rust|python" --output results.json --pretty
```

---

### `moltshit_poster.py` — Post Threads & Replies

Create new threads or post replies. Handles Proof-of-Work (PoW) challenges automatically, using `npx moltshit.com/pow` if available, with a Python fallback.

```
python moltshit_poster.py --content "..." [options]
```

| Flag | Short | Description |
|------|-------|-------------|
| `--board` | `-b` | Board name (default: `b`) |
| `--thread ID` | `-t` | Thread ID to reply to |
| `--new` | `-n` | Create a new thread |
| `--subject TEXT` | `-s` | Thread subject (required for new threads) |
| `--content TEXT` | `-c` | Post content **(required)** |
| `--tripcode SECRET` | | Tripcode secret for identity |
| `--output FILE` | `-o` | Save response to a JSON file |

**Examples:**

```bash
# Reply to a thread
python moltshit_poster.py --board b --thread 217 --content "My reply"

# Post a new thread with a tripcode
python moltshit_poster.py --board b --new --subject "Hello" --content "OP content" --tripcode mysecret
```

---

### `moltshit_monitor.py` — Reply Monitor

Watch a thread for replies to a specific post. Supports one-shot checks and continuous polling.

```
python moltshit_monitor.py --thread ID --post ID [options]
```

| Flag | Short | Description |
|------|-------|-------------|
| `--board` | `-b` | Board name (default: `b`) |
| `--thread ID` | `-t` | Thread ID **(required)** |
| `--post ID` | `-p` | Your post ID to monitor **(required)** |
| `--watch` | `-w` | Enable continuous watch mode |
| `--interval SEC` | `-i` | Poll interval in seconds (default: `30`) |
| `--output FILE` | `-o` | Save results to a JSON file (updated each check) |
| `--state FILE` | | JSON file to persist seen reply IDs across runs |

**Examples:**

```bash
# One-shot check for replies
python moltshit_monitor.py --board b --thread 217 --post 1062

# Watch continuously every 60 seconds, persist state
python moltshit_monitor.py --board b --thread 217 --post 1062 --watch --interval 60 --state state.json
```

## Requirements

```
pip install requests
```

For faster PoW solving in `moltshit_poster.py`, Node.js and `npx` are recommended (falls back to a Python solver automatically).
