#!/usr/bin/env python3
"""GPT-image-2 generation script. Supports text-to-image and image-to-image."""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.json")


def load_config():
    """Load API config from config.json."""
    if not os.path.exists(CONFIG_PATH):
        return None, "config.json not found at: " + CONFIG_PATH
    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)
    return config, None


def call_api(config, prompt, size="1:1", n=1, images=None):
    """Call the GPT-image-2 API."""
    data = {
        "model": "gpt-image-2",
        "prompt": prompt,
        "n": n,
        "size": size,
        "response_format": "url",
    }
    if images:
        data["image"] = images if isinstance(images, list) else [images]

    payload = json.dumps(data).encode("utf-8")
    headers = {
        "Authorization": f"Bearer {config['api_key']}",
        "Content-Type": "application/json",
    }

    req = urllib.request.Request(config["api_url"], data=payload, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            urls = [item["url"] for item in result["data"]]
            return urls, None
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        return None, f"HTTP {e.code}: {body}"
    except urllib.error.URLError as e:
        return None, f"Network error: {e.reason}"
    except Exception as e:
        return None, str(e)


def download_image(url, output_path):
    """Download image from URL to local path."""
    try:
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Referer": url,
        })
        with urllib.request.urlopen(req, timeout=60) as resp:
            with open(output_path, "wb") as f:
                f.write(resp.read())
        return True, None
    except Exception as e:
        return False, str(e)


def main():
    parser = argparse.ArgumentParser(description="GPT-image-2 generation")
    parser.add_argument("--mode", choices=["text2img", "img2img"], required=True)
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--size", default="1:1")
    parser.add_argument("--output", required=True)
    parser.add_argument("--images", nargs="*", help="Reference image URLs for img2img")
    parser.add_argument("--n", type=int, default=1, help="Number of images to generate")
    args = parser.parse_args()

    config, err = load_config()
    if err:
        print(json.dumps({"success": False, "error": err}))
        sys.exit(1)

    images = args.images if args.mode == "img2img" else None
    urls, err = call_api(config, args.prompt, args.size, args.n, images)
    if err:
        print(json.dumps({"success": False, "error": err}))
        sys.exit(1)

    # Download the first image to the output path
    ok, dl_err = download_image(urls[0], args.output)
    if not ok:
        print(json.dumps({"success": False, "error": f"Download failed: {dl_err}", "urls": urls}))
        sys.exit(1)

    print(json.dumps({"success": True, "urls": urls, "local_path": os.path.abspath(args.output)}))


if __name__ == "__main__":
    main()
