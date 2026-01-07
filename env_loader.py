
import os
from dotenv import load_dotenv

def load_keys(mode):
    env_file = ".env.demo" if mode == "DEMO" else ".env.real"
    if not os.path.exists(env_file):
        raise Exception(f"File {env_file} tidak ditemukan")
    load_dotenv(env_file, override=True)
