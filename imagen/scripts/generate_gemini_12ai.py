#!/usr/bin/env python3
"""
Image Generation using 12ai API with Gemini native format

Usage:
    python generate_gemini_12ai.py "prompt" [output_path]
"""

import argparse
import base64
import json
import os
import sys
import urllib.request
import urllib.error
import urllib.parse
from pathlib import Path


# Configuration
API_BASE_URL = "https://new.12ai.org/v1beta"
API_KEY = "sk-DYw0ELJlzl6g6Z7JbgX3x6BMNSp2DXtZ1cZ17VkWPGwxfMFV"
DEFAULT_MODEL = "gemini-3-pro-image-preview"
DEFAULT_IMAGE_SIZE = "1K"


def create_output_dir(output_path: Path) -> None:
    """Create output directory if it doesn't exist."""
    output_dir = output_path.parent
    if output_dir and not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)


def make_api_request(prompt: str, model: str = DEFAULT_MODEL, image_size: str = DEFAULT_IMAGE_SIZE) -> dict:
    """Make the API request and return the response."""
    # URL encode the API key to handle special characters
    encoded_key = urllib.parse.quote(API_KEY, safe='')
    url = f"{API_BASE_URL}/models/{model}:streamGenerateContent?key={encoded_key}"

    request_data = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": prompt}]
            }
        ],
        "generationConfig": {
            "responseModalities": ["IMAGE", "TEXT"],
            "imageConfig": {
                "image_size": image_size
            }
        }
    }

    headers = {
        "Content-Type": "application/json"
    }

    req = urllib.request.Request(url, data=json.dumps(request_data).encode("utf-8"), headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=180) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else ""
        print(f"Error: API request failed with HTTP status {e.code}", file=sys.stderr)
        print(f"Response: {error_body[:500]}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Error: Failed to connect to API: {e.reason}", file=sys.stderr)
        sys.exit(1)


def extract_image_data(response: dict) -> str:
    """Extract base64 image data from the API response."""
    try:
        candidates = response.get("candidates", [])
        if not candidates:
            raise ValueError("No candidates in response")

        parts = candidates[0].get("content", {}).get("parts", [])

        for part in parts:
            if "inlineData" in part:
                return part["inlineData"].get("data", "")

        raise ValueError("No image data found in response parts")
    except (KeyError, IndexError, TypeError) as e:
        print(f"Error: Failed to parse response: {e}", file=sys.stderr)
        print(f"Response: {json.dumps(response, indent=2)[:1000]}", file=sys.stderr)
        sys.exit(1)


def save_image(image_data: str, output_path: Path) -> None:
    """Decode and save the base64 image data."""
    try:
        image_bytes = base64.b64decode(image_data)
        output_path.write_bytes(image_bytes)
    except Exception as e:
        print(f"Error: Failed to save image: {e}", file=sys.stderr)
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
    parser = argparse.ArgumentParser(description="Generate images using 12ai Gemini API")
    parser.add_argument("prompt", help="Text description of the image to generate")
    parser.add_argument("output", nargs="?", default="./generated-image.png",
                        help="Output file path (default: ./generated-image.png)")
    parser.add_argument("--model", default=DEFAULT_MODEL, help=f"Model to use (default: {DEFAULT_MODEL})")
    parser.add_argument("--size", choices=["512", "1K", "2K"], default=DEFAULT_IMAGE_SIZE,
                        help=f"Image size (default: {DEFAULT_IMAGE_SIZE})")

    args = parser.parse_args()

    output_path = Path(args.output)
    create_output_dir(output_path)

    print(f"Generating image with prompt: \"{args.prompt[:100]}...\"")
    print(f"Model: {args.model}")
    print(f"Image size: {args.size}")
    print(f"Output path: {output_path}")
    print()

    # Make API request
    response = make_api_request(args.prompt, args.model, args.size)

    # Extract image data
    image_data = extract_image_data(response)
    if not image_data:
        print("Error: No image data received from API", file=sys.stderr)
        sys.exit(1)

    print("Image data received, decoding and saving...")

    # Save image
    save_image(image_data, output_path)

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
