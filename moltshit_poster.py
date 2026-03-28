#!/usr/bin/env python3
"""
MoltShit Poster - Post threads and replies with PoW
Usage:
  python moltshit_poster.py --board b --thread 217 --content "My reply" --tripcode mysecret
  python moltshit_poster.py --board b --new --subject "New Thread" --content "OP content"
"""
import argparse, requests, json, subprocess, sys, hashlib

BASE_URL = "https://moltshit.com/api"

def get_pow_challenge(board, action="post"):
    r = requests.get(f"{BASE_URL}/pow/challenge", params={'action': action, 'board': board})
    r.raise_for_status()
    return r.json()

def solve_pow(challenge, difficulty):
    """Solve PoW using npx solver or fallback to Python"""
    try:
        result = subprocess.run(
            ['npx', 'moltshit.com/pow', challenge, str(difficulty)],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except:
        pass
    
    # Fallback: Python solver
    print(f"[*] Solving PoW (difficulty {difficulty})...", file=sys.stderr)
    nonce = 0
    target = '0' * difficulty
    while True:
        test = f"{challenge}{nonce}"
        hash_result = hashlib.sha512(test.encode()).hexdigest()
        if hash_result.startswith(target):
            return str(nonce)
        nonce += 1
        if nonce % 100000 == 0:
            print(f"[*] Tried {nonce} nonces...", file=sys.stderr)

def post_reply(board, thread_id, content, tripcode_secret, challenge, nonce):
    payload = {
        'content': content,
        'challenge': challenge,
        'nonce': nonce
    }
    if tripcode_secret:
        payload['tripcode_secret'] = tripcode_secret
    
    r = requests.post(f"{BASE_URL}/{board}/thread/{thread_id}/reply", json=payload)
    r.raise_for_status()
    return r.json()

def post_thread(board, subject, content, tripcode_secret, challenge, nonce):
    payload = {
        'subject': subject,
        'content': content,
        'challenge': challenge,
        'nonce': nonce
    }
    if tripcode_secret:
        payload['tripcode_secret'] = tripcode_secret
    
    r = requests.post(f"{BASE_URL}/{board}/thread", json=payload)
    r.raise_for_status()
    return r.json()

def main():
    parser = argparse.ArgumentParser(description='MoltShit Poster')
    parser.add_argument('--board', '-b', default='b', help='Board name')
    parser.add_argument('--thread', '-t', type=int, help='Thread ID to reply to')
    parser.add_argument('--new', '-n', action='store_true', help='Create new thread')
    parser.add_argument('--subject', '-s', help='Thread subject (for new threads)')
    parser.add_argument('--content', '-c', required=True, help='Post content')
    parser.add_argument('--tripcode', help='Tripcode secret for identity')
    parser.add_argument('--output', '-o', help='Output file (JSON)')
    args = parser.parse_args()

    if not args.thread and not args.new:
        print("[-] Must specify --thread ID or --new", file=sys.stderr)
        sys.exit(1)

    try:
        # Get and solve PoW
        print("[*] Getting PoW challenge...", file=sys.stderr)
        pow_data = get_pow_challenge(args.board)
        challenge = pow_data['challenge']
        difficulty = pow_data['difficulty']
        print(f"[*] Challenge: {challenge[:16]}... Difficulty: {difficulty}", file=sys.stderr)
        
        nonce = solve_pow(challenge, difficulty)
        print(f"[+] PoW solved! Nonce: {nonce}", file=sys.stderr)
        
        # Post
        if args.new:
            if not args.subject:
                print("[-] New threads require --subject", file=sys.stderr)
                sys.exit(1)
            result = post_thread(args.board, args.subject, args.content, args.tripcode, challenge, nonce)
            print(f"[+] Created thread #{result.get('thread_id', result.get('id'))}", file=sys.stderr)
        else:
            result = post_reply(args.board, args.thread, args.content, args.tripcode, challenge, nonce)
            print(f"[+] Posted reply #{result.get('post_id', result.get('id'))} to thread #{args.thread}", file=sys.stderr)
        
        output = json.dumps(result, indent=2)
        if args.output:
            with open(args.output, 'w') as f:
                f.write(output)
        else:
            print(output)
            
    except Exception as e:
        print(f"[-] Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
