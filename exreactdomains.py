import requests
import re

# GitHub API
API_URL = "https://api.github.com/repos/femboyenjoy/myscript/contents/raw"
RAW_PREFIX = "https://raw.githubusercontent.com/femboyenjoy/myscript/main/raw/"

pattern = re.compile(r"([a-zA-Z0-9.-]+\.browserleaks\.org)")

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0"
})

def get_file_list():
    print("[*] 获取 GitHub 仓库文件列表...")

    r = session.get(API_URL)
    r.raise_for_status()

    data = r.json()
    files = []

    for item in data:
        if item["type"] == "file":
            files.append(item["name"])

    print(f"[+] 共发现 {len(files)} 个文件")
    return files

def download_file(file_name):
    url = RAW_PREFIX + file_name
    try:
        r = session.get(url, timeout=10)
        r.raise_for_status()
        return r.text
    except Exception as e:
        print(f"[!] 下载失败 {url}: {e}")
        return ""

def main():
    all_domains = set()
    files = get_file_list()

    for f in files:
        print(f"[*] 下载 {f}")
        content = download_file(f)
        domains = pattern.findall(content)
        all_domains.update(domains)

    print(f"\n[*] 共提取 {len(all_domains)} 个唯一域名：")
    for d in sorted(all_domains):
        print(d)

if __name__ == "__main__":
    main()
