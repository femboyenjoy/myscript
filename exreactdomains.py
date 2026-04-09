import requests
import re

# ===== 配置 =====
URL = "你的远程日志URL"   # ← 改这里
TIMEOUT = 10

# ===== 正则 =====
pattern = re.compile(r'([a-zA-Z0-9.-]+\.browserleaks\.org)')

def fetch():
    print("[*] 正在下载日志...")
    resp = requests.get(URL, timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.text

def extract(text):
    print("[*] 提取域名...")
    domains = pattern.findall(text)
    return set(domains)  # 去重

def main():
    text = fetch()
    domains = extract(text)

    print(f"\n[*] 共提取 {len(domains)} 个唯一域名:\n")

    for d in sorted(domains):
        print(d)

if __name__ == "__main__":
    main()
