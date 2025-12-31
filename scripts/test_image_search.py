"""
Test Image Search với file ảnh local
=====================================
Script này sẽ:
1. Đọc file ảnh từ máy tính
2. Convert sang base64
3. Gọi API search

Usage:
    python scripts/test_image_search.py D:\path\to\image.jpg
"""
import sys
import base64
import json
import requests

# ============================================
# CONFIGURATION - CẬP NHẬT URL CỦA BẠN!
# ============================================
API_URL = "https://YOUR_API_ID.execute-api.us-east-1.amazonaws.com/search"


def test_image_search(image_path: str):
    print("=" * 60)
    print("🖼️ Image Search Test")
    print("=" * 60)
    
    # 1. Đọc file ảnh
    print(f"\n1. Đọc file: {image_path}")
    try:
        with open(image_path, "rb") as f:
            image_bytes = f.read()
        print(f"   ✅ File size: {len(image_bytes):,} bytes")
    except FileNotFoundError:
        print(f"   ❌ File không tồn tại!")
        return
    
    # 2. Convert sang base64
    print("\n2. Convert sang base64...")
    base64_string = base64.b64encode(image_bytes).decode("utf-8")
    print(f"   ✅ Base64 length: {len(base64_string):,} chars")
    print(f"   Preview: {base64_string[:50]}...")
    
    # 3. Kiểm tra base64 có hợp lệ không
    print("\n3. Validate base64...")
    try:
        decoded = base64.b64decode(base64_string)
        print(f"   ✅ Valid! Decoded size: {len(decoded):,} bytes")
    except Exception as e:
        print(f"   ❌ Invalid base64: {e}")
        return
    
    # 4. Gửi API
    print("\n4. Gọi API...")
    print(f"   URL: {API_URL}")
    
    if "YOUR_API_ID" in API_URL:
        print("   ⚠️ Vui lòng cập nhật API_URL trong script!")
        print("\n📋 Base64 string (copy để test trong Postman):")
        print("-" * 60)
        print(base64_string[:500] + "..." if len(base64_string) > 500 else base64_string)
        print("-" * 60)
        print(f"\n📄 Full base64 saved to: test_base64.txt")
        with open("test_base64.txt", "w") as f:
            f.write(base64_string)
        return
    
    payload = {
        "search_type": "image",
        "image_base64": base64_string,
        "modalities": ["visual"],
        "top_k": 3
    }
    
    try:
        response = requests.post(API_URL, json=payload, timeout=60)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ SUCCESS! Found {data['total_results']} results")
            for r in data['results']:
                print(f"   - Score: {r['score']:.4f} | Segment {r['segment_id']} | {r['start_time']:.1f}s")
        else:
            print(f"\n❌ ERROR: {response.text}")
    except Exception as e:
        print(f"\n❌ Exception: {e}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python test_image_search.py <image_path>")
        print("Example: python test_image_search.py D:\\images\\test.jpg")
        return
    
    image_path = sys.argv[1]
    test_image_search(image_path)


if __name__ == "__main__":
    main()
