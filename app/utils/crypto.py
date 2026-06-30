from cryptography.fernet import Fernet
import json
import os
from pathlib import Path
VAULT_KEY = Path("./data/vault.key")
ENC_FILE = Path("./.env.enc")
_cached_env = None
def generate_key():
    VAULT_KEY.parent.mkdir(exist_ok=True)
    if not VAULT_KEY.exists():
        VAULT_KEY.write_bytes(Fernet.generate_key())
def get_cipher() -> Fernet:
    generate_key()
    return Fernet(VAULT_KEY.read_bytes())
def encrypt_env(raw_dict: dict):
    global _cached_env
    cipher = get_cipher()
    data = json.dumps(raw_dict).encode("utf8")
    ENC_FILE.write_bytes(cipher.encrypt(data))
    _cached_env = raw_dict
def decrypt_env() -> dict:
    global _cached_env
    if _cached_env is not None: return _cached_env
    if not ENC_FILE.exists(): return dict(os.environ)
    try:
        cipher = get_cipher()
        raw = cipher.decrypt(ENC_FILE.read_bytes())
        _cached_env = json.loads(raw.decode("utf8"))
        return _cached_env
    except Exception: return dict(os.environ)
def get_secret(k: str) -> str | None:
    return decrypt_env().get(k) if k else None
