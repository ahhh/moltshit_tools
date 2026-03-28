#!/usr/bin/env python3
"""
MoltShit Board Monitor - Fetch and search board content
Usage:
  python moltshit_monitor.py --board b --output catalog.json
  python moltshit_monitor.py --board b --grep "hack|exploit|security"
  python moltshit_monitor.py --board b --thread 217
"""
import argparse, requests, json, re, sys
from datetime import datetime

BASE_URL = "https://moltshit.com/api"

def fetch_catalog(board):
    r = requests.get(f"{BASE_URL}/{board}/catalog")
    r.raise_for_status()
    return r.json()

def fetch_thread(board, thread_id):
    r = requests.get(f"{BASE_URL}/{board}/thread/{thread_id}")
    r.raise_for_status()
    return r.json()

def grep_threads(threads, pattern):
    regex = re.compile(pattern, re.IGNORECASE)
    matches = []
    for t in threads:
        subject = t.get('subject', '') or ''
        content = t.get('content', '') or t.get('preview', '') or ''
        if regex.search(subject) or regex.search(content):
            matches.append({
                'thread_id': t.get('id') or t.get('thread_id'),
                'subject': subject,
                'matched_in': 'subject' if regex.search(subject) else 'content',
                'preview': content[:200]
            })
    return matches

def main():
    parser = argparse.ArgumentParser(description='MoltShit Board Monitor')
    parser.add_argument('--board', '-b', default='b', help='Board name (default: b)')
    parser.add_argument('--thread', '-t', type=int, help='Fetch specific thread ID')
    parser.add_argument('--grep', '-g', help='Regex pattern to search for')
    parser.add_argument('--output', '-o', help='Output file (JSON)')
    parser.add_argument('--pretty', '-p', action='store_true', help='Pretty print JSON')
    args = parser.parse_args()

    try:
        if args.thread:
            data = fetch_thread(args.board, args.thread)
            print(f"[+] Fetched thread #{args.thread}", file=sys.stderr)
        else:
            data = fetch_catalog(args.board)
            print(f"[+] Fetched /{args.board}/ catalog: {len(data.get('threads', data))} threads", file=sys.stderr)
            
            if args.grep:
                threads = data.get('threads', data) if isinstance(data, dict) else data
                matches = grep_threads(threads, args.grep)
                data = {'pattern': args.grep, 'matches': matches, 'count': len(matches)}
                print(f"[+] Grep '{args.grep}': {len(matches)} matches", file=sys.stderr)

        output = json.dumps(data, indent=2 if args.pretty else None)
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(output)
            print(f"[+] Saved to {args.output}", file=sys.stderr)
        else:
            print(output)
            
    except Exception as e:
        print(f"[-] Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
