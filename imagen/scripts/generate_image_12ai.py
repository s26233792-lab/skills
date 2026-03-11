#!/usr/bin/env python3
"""
Image Generation using 12ai API (OpenAI-compatible format)

Usage:
    python generate_image_12ai.py "prompt" [output_path]
"""

import argparse
import base64
import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path


# Configuration
API_BASE_URL = "https://new.12ai.org/v1"
API_KEY = "sk-DYw0ELJlzl6g6Z7JbgX3x6BMNSp2DXtZ1cZ17VkWPGwxfMFV"
DEFAULT_MODEL = "gemini-3-pro-image-preview"
DEFAULT_SIZE = "1024x1024"


def create_output_dir(output_path: Path) -> None:
    """Create output directory if it doesn't exist."""
    output_dir = output_path.parent
    if output_dir and not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)


def make_api_request(prompt: str, model: str = DEFAULT_MODEL, size: str = DEFAULT_SIZE) -> dict:
    """Make the API request and return the response."""
    url = f"{API_BASE_URL}/images/generations"

    request_data = {
        "model": model,
        "prompt": prompt,
        "n": 1,
        "size": size
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    req = urllib.request.Request(url, data=json.dumps(request_data).encode("utf-8"), headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=180) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else ""
        print(f"Error: API request failed with HTTP status {e.code}", file=sys.stderr)
        print(f"Response: {error_body}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Error: Failed to connect to API: {e.reason}", file=sys.stderr)
        sys.exit(1)


def extract_image_url(response: dict) -> str:
    """Extract image URL from the API response."""
    try:
        if "data" in response and len(response["data"]) > 0:
            return response["data"][0].get("url", "")
        raise ValueError("No image data in response")
    except (KeyError, IndexError) as e:
        print(f"Error: Failed to parse response: {e}", file=sys.stderr)
        print(f"Response: {json.dumps(response, indent=2)}", file=sys.stderr)
        sys.exit(1)


def download_image(url: str, output_path: Path) -> None:
    """Download image from URL and save to file."""
    try:
        with urllib.request.urlopen(url, timeout=60) as response:
            image_data = response.read()
            output_path.write_bytes(image_data)
    except Exception as e:
        print(f"Error: Failed to download image: {e}", file=sys.stderr)
        sys.exit(1)


def get_file_size(path: Path) -> str:
    """Get human-readable file size."""
    size = path.stat().st_size
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"


def main():
    parser = argparse.ArgumentParser(description="Generate images using 12ai API")
    parser.add_argument("prompt", help="Text description of the image to generate")
    parser.add_argument("output", nargs="?", default="./generated-image.png",
                        help="Output file path (default: ./generated-image.png)")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"Model to use (default: {DEFAULT_MODEL})")
    parser.add_argument("--size", default=DEFAULT_SIZE, help=f"Image size (default: {DEFAULT_SIZE})")

    args = parser.parse_args()

    output_path = Path(args.output)
    create_output_dir(output_path)

    print(f"Generating image with prompt: \"{args.prompt}\"")
    print(f"Model: {args.model}")
    print(f"Output path: {output_path}")
    print()

    # Make API request
    response = make_api_request(args.prompt, args.model, args.size)

    # Extract image URL
    image_url = extract_image_url(response)
    if not image_url:
        print("Error: No image URL received from API", file=sys.stderr)
        sys.exit(1)

    print(f"Image URL: {image_url}")
    print()

    # Download and save image
    download_image(image_url, output_path)

    # Verify and report success
    if output_path.exists() and output_path.stat().st_size > 0:
        file_size = get_file_size(output_path)
        print("Success! Image generated and saved.")
        print(f"File: {output_path}")
        print(f"Size: {file_size}")
    else:
        print(f"Error: Failed to save image to {output_path}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
