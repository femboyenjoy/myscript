import requests
import re
from bs4 import BeautifulSoup

# 仓库目录 URL（浏览器打开的目录页面）
GITHUB_DIR_URL = "https://github.com/femboyenjoy/myscript/blob/main/raw"
GITHUB_RAW_PREFIX = "https://github.com/femboyenjoy/myscript/raw/main/raw/"

# 正则匹配 .browserleaks.org
pattern = re.compile(r"([a-zA-Z0-9.-]+\.browserleaks\.org)")

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0"
})

def get_file_list():
    print("[*] 获取 GitHub 仓库文件列表...")
    r = session.get(GITHUB_DIR_URL)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")
    files = []

    # GitHub 文件名都在 <a class="js-navigation-open"> 标签里
    for a in soup.find_all("a", class_="js-navigation-open"):
        href = a.get("title")  # title 属性就是文件名
        if href:
            files.append(href)

    print(f"[+] 共发现 {len(files)} 个文件")
    return files

def download_file(file_name):
    url = GITHUB_RAW_PREFIX + file_name
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
