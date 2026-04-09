import requests
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

# ===== 配置 =====
URLS = [
    "https://raw.githubusercontent.com/femboyenjoy/myscript/main/raw/service_2026-04-09_11-32-02.log",
    "https://raw.githubusercontent.com/femboyenjoy/myscript/main/raw/service_2026-04-09_17-49-10.log",
    "https://raw.githubusercontent.com/femboyenjoy/myscript/main/raw/service_2026-04-09_17-49-22.log",
    "https://raw.githubusercontent.com/femboyenjoy/myscript/main/raw/service_2026-04-09_17-49-35.log",
    "https://raw.githubusercontent.com/femboyenjoy/myscript/main/raw/service_2026-04-09_17-49-46.log",
    "https://raw.githubusercontent.com/femboyenjoy/myscript/main/raw/service_2026-04-09_17-50-00.log",
    "https://raw.githubusercontent.com/femboyenjoy/myscript/main/raw/service_2026-04-09_17-50-11.log",
    "https://raw.githubusercontent.com/femboyenjoy/myscript/main/raw/service_2026-04-09_17-50-24.log",
]
TIMEOUT = 10
MAX_WORKERS = 5  # 并发下载数量，可根据网络调整

# ===== 正则 =====
pattern = re.compile(r'([a-zA-Z0-9.-]+\.browserleaks\.org)')

def fetch(url):
    """下载单个 URL 内容"""
    try:
        print(f"[*] 正在下载: {url}")
        resp = requests.get(url, timeout=TIMEOUT)
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        print(f"[!] 下载失败 {url}: {e}")
        return ""

def extract_domains(text):
    """提取域名并去重"""
    return set(pattern.findall(text))

def main():
    all_domains = set()

    # 使用线程池并发下载
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_url = {executor.submit(fetch, url): url for url in URLS}
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                text = future.result()
                domains = extract_domains(text)
                all_domains.update(domains)
                print(f"[+] {url} 提取 {len(domains)} 个域名")
            except Exception as e:
                print(f"[!] 处理 {url} 出错: {e}")

    print(f"\n[*] 共提取 {len(all_domains)} 个唯一域名:\n")
    for d in sorted(all_domains):
        print(d)

if __name__ == "__main__":
    main()
