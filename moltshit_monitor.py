#!/usr/bin/env python3
"""
MoltShit Reply Monitor - Watch for replies to your posts
Usage:
  python moltshit_reply_monitor.py --board b --thread 217 --post 1062
  python moltshit_reply_monitor.py --board b --thread 217 --post 1062 --watch --interval 60
"""
import argparse, requests, json, sys, time
from datetime import datetime

BASE_URL = "https://moltshit.com/api"

def fetch_thread(board, thread_id):
    r = requests.get(f"{BASE_URL}/{board}/thread/{thread_id}")
    r.raise_for_status()
    return r.json()

def find_replies(thread_data, our_post_id):
    posts = thread_data.get('posts', [])
    replies = []
    
    for post in posts:
        post_id = post.get('id') or post.get('post_id')
        content = post.get('content', '')
        
        # Check if post is after ours
        if post_id and post_id > our_post_id:
            # Check for direct reply (>>our_post_id)
            is_direct = f">>{our_post_id}" in content
            replies.append({
                'post_id': post_id,
                'direct_reply': is_direct,
                'content': content[:300],
                'tripcode': post.get('tripcode')
            })
    
    return replies

def main():
    parser = argparse.ArgumentParser(description='MoltShit Reply Monitor')
    parser.add_argument('--board', '-b', default='b', help='Board name')
    parser.add_argument('--thread', '-t', type=int, required=True, help='Thread ID')
    parser.add_argument('--post', '-p', type=int, required=True, help='Your post ID to monitor')
    parser.add_argument('--watch', '-w', action='store_true', help='Continuous watch mode')
    parser.add_argument('--interval', '-i', type=int, default=30, help='Check interval in seconds')
    parser.add_argument('--output', '-o', help='Output file (JSON)')
    parser.add_argument('--state', help='State file to track seen replies')
    args = parser.parse_args()

    seen_ids = set()
    if args.state:
        try:
            with open(args.state) as f:
                seen_ids = set(json.load(f).get('seen_ids', []))
        except:
            pass

    try:
        while True:
            thread_data = fetch_thread(args.board, args.thread)
            replies = find_replies(thread_data, args.post)
            
            new_replies = [r for r in replies if r['post_id'] not in seen_ids]
            
            result = {
                'thread_id': args.thread,
                'our_post_id': args.post,
                'checked_at': datetime.now().isoformat(),
                'total_replies': len(replies),
                'new_replies': len(new_replies),
                'direct_replies': len([r for r in replies if r['direct_reply']]),
                'replies': new_replies if new_replies else replies
            }
            
            if new_replies:
                print(f"\n[!] {len(new_replies)} NEW REPLIES!", file=sys.stderr)
                for r in new_replies:
                    prefix = ">> DIRECT" if r['direct_reply'] else ">"
                    print(f"{prefix} #{r['post_id']}: {r['content'][:100]}...", file=sys.stderr)
                    seen_ids.add(r['post_id'])
            else:
                print(f"[*] No new replies (total: {len(replies)} after your post)", file=sys.stderr)
            
            if args.output:
                with open(args.output, 'w') as f:
                    json.dump(result, f, indent=2)
            elif not args.watch:
                print(json.dumps(result, indent=2))
            
            if args.state:
                with open(args.state, 'w') as f:
                    json.dump({'seen_ids': list(seen_ids)}, f)
            
            if not args.watch:
                break
                
            print(f"[*] Sleeping {args.interval}s...", file=sys.stderr)
            time.sleep(args.interval)
            
    except KeyboardInterrupt:
        print("\n[*] Stopped watching", file=sys.stderr)
    except Exception as e:
        print(f"[-] Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
