import requests
from bs4 import BeautifulSoup
import re

def get_direct_link(download_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(download_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        scripts = soup.find_all("script")
        pattern = re.compile(r'https://fuckingfast\.co/dl/[a-zA-Z0-9_-]+')
        for script in scripts:
            if script.string:
                match = pattern.search(script.string)
                if match:
                    return match.group()
    except requests.RequestException as e:
        print(f"[!] Failed to fetch {download_url}: {e}")
    return None

def generate_html(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            raw_links = [line.strip() for line in f if line.strip()]

        direct_links = []
        for link in raw_links:
            direct = get_direct_link(link)
            if direct:
                direct_links.append((link, direct))
                print(f"[+] {link} -> {direct}")
            else:
                print(f"[-] No direct link found for: {link}")

        js_array = ",\n      ".join(f'"{direct}"' for _, direct in direct_links)
        html_list = "\n        ".join(f'<li><a href="{direct}" target="_blank">{link}</a></li>' for link, direct in direct_links)

        html_content = f"""<!DOCTYPE html>
<html>
<head>
  <title>Open Direct Links in Batches</title>
  <script>
    const links = [
      {js_array}
    ];

    function openBatch(startIndex, count) {{
      const batch = links.slice(startIndex, startIndex + count);
      batch.forEach(url => window.open(url, '_blank'));
    }}

    function createButtons() {{
      const container = document.getElementById('buttons');
      for (let i = 0; i < links.length; i += 10) {{
        const btn = document.createElement('button');
        btn.textContent = `Open ${{i + 1}}–${{Math.min(i + 10, links.length)}}`;
        btn.onclick = () => openBatch(i, 10);
        container.appendChild(btn);
      }}
    }}

    window.onload = createButtons;
  </script>
</head>
<body>
  <h2>Open Direct Links in Batches of 10</h2>
  <div id="buttons"></div>
  <h3>Link List:</h3>
  <ol>
    {html_list}
  </ol>
</body>
</html>"""

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"\n✅ HTML file '{output_file}' generated with {len(direct_links)} direct links.")
    except Exception as e:
        print(f"❌ Error: {e}")

# Prompt user for filenames
if __name__ == "__main__":
    print("🚀 Welcome to the Ultimate fitgirl Repacks Downloader!")
    print("🔍 Let's turn your plain text file into a sleek HTML download page.\n  Right now this just support fuckingfast host.\n  ")
    print("📝 Please provide the file containing list of links:")
    input_file = input("📂 Enter input filename (see links_example.txt and create like that!): ").strip()
    print(f"✅ Got it!  Reading links from: {input_file}")

    output_file = input("💾 Enter output HTML filename (e.g., links.html): ").strip()
    print(f"🎯 Perfect! Your download page will be saved as: {output_file}\n")

    print("🛠️ Generating your HTML file with direct download links...")
    generate_html(input_file, output_file)
    print(f"\n🎉 All done! Your file '{output_file}' is ready to use.")
    print("📎 Open it in your browser and start downloading like a pro! \n Make sure to allow popups for this file to work completely.")

