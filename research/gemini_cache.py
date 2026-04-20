"""
Gemini flash-lite systemInstruction cache helper.

Creates a cachedContents entry for the stable systemInstruction portion of a
prompt and reuses it across calls within a 1h TTL. Caller sends the per-call
user message to generateContent with `cachedContent` set, paying $0.01/1M on
the cached prefix instead of $0.10/1M.

Break-even vs uncached: ~11 reads/hour on a 2500-token cache (storage is
$1/1M tokens/hr). Above that we save; below, caching is a net loss.

flash-lite minimum cache size is 2048 tokens. Below that, or on any API
error, this module returns None and the caller MUST fall back to an
uncached call (systemInstruction inline) so there is no behavior change.

Persistent state at gemini_cache_state.json survives service restarts so an
in-flight cache is not needlessly recreated on each ODIN restart.
"""
import hashlib
import json
import os
import time
import urllib.error
import urllib.request

MIN_CACHE_TOKENS = 2048
DEFAULT_TTL      = 3600
STATE_FILE       = '/root/.openclaw/workspace/research/gemini_cache_state.json'
MODEL            = 'gemini-2.5-flash-lite'
BASE             = 'https://generativelanguage.googleapis.com/v1beta'


def _hash(text):
    return hashlib.sha256(text.encode()).hexdigest()[:16]


def _load_state():
    if not os.path.exists(STATE_FILE):
        return {}
    try:
        with open(STATE_FILE) as f:
            return json.load(f)
    except Exception:
        return {}


def _save_state(state):
    tmp = STATE_FILE + '.tmp'
    with open(tmp, 'w') as f:
        json.dump(state, f)
    os.replace(tmp, STATE_FILE)


def _count_tokens(text, api_key):
    url = f'{BASE}/models/{MODEL}:countTokens?key={api_key}'
    payload = json.dumps({'contents': [{'parts': [{'text': text}]}]}).encode()
    req = urllib.request.Request(
        url, data=payload, headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read())['totalTokens']


def _create_cache(system_instruction, api_key, ttl):
    url = f'{BASE}/cachedContents?key={api_key}'
    payload = json.dumps({
        'model': f'models/{MODEL}',
        'systemInstruction': {'parts': [{'text': system_instruction}]},
        'ttl': f'{ttl}s',
    }).encode()
    req = urllib.request.Request(
        url, data=payload, headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


def get_cache_name(scope, system_instruction, api_key, ttl=DEFAULT_TTL):
    """Return a cachedContents/<id> ref or None. On None, caller falls back
    to uncached generateContent with systemInstruction inline."""
    h = _hash(system_instruction)
    now = time.time()
    state = _load_state()
    entry = state.get(scope, {})

    # Reuse if content unchanged and TTL has margin
    if (entry.get('cache_name') and entry.get('hash') == h and
            entry.get('expires_at', 0) > now + 60):
        return entry['cache_name']

    # Avoid spammy skip re-checks: if we recently determined the content is
    # too small to cache AND the hash matches, keep returning None without
    # another countTokens call for 5 minutes.
    if (entry.get('skip_reason') == 'too_small' and entry.get('hash') == h
            and (now - entry.get('checked_at', 0)) < 300):
        return None

    try:
        tokens = _count_tokens(system_instruction, api_key)
    except Exception:
        return None

    if tokens < MIN_CACHE_TOKENS:
        state[scope] = {
            'skip_reason': 'too_small',
            'tokens': tokens, 'hash': h, 'checked_at': now,
        }
        _save_state(state)
        return None

    try:
        resp = _create_cache(system_instruction, api_key, ttl)
    except urllib.error.HTTPError as e:
        state[scope] = {
            'skip_reason': 'http_err',
            'code': e.code, 'hash': h, 'checked_at': now,
        }
        _save_state(state)
        return None
    except Exception:
        return None

    name = resp.get('name')
    if not name:
        return None

    state[scope] = {
        'cache_name': name,
        'hash': h,
        'tokens': tokens,
        'created_at': now,
        'expires_at': now + ttl - 60,
        'ttl': ttl,
    }
    _save_state(state)
    return name
