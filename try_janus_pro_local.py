import requests
import time
import os

API_URL = "http://localhost:8080/janus-pro"
# 使用测试目录中的本地图片文件
LOCAL_IMAGE_PATH = "/home/echo/janus-pro-deployment/test/up.jpg"

# 检查文件是否存在
if not os.path.exists(LOCAL_IMAGE_PATH):
    print(f"Error: Local image file not found at {LOCAL_IMAGE_PATH}")
    print("Please make sure the image file exists or update the path.")
    exit(1)

# 构建JSON数据
json_payload = {
    "image_path": LOCAL_IMAGE_PATH,
    "prompt": "describe this image in detail",
}

print(f"Testing API with local image: {LOCAL_IMAGE_PATH}")
print(f"API URL: {API_URL}")
print(f"Prompt: {json_payload['prompt']}")
print("-" * 50)

# 记录开始时间
start_time = time.perf_counter()

# 使用requests发送POST请求
try:
    response = requests.post(API_URL, json=json_payload)
    
    # 记录结束时间
    end_time = time.perf_counter()
    
    # 计算耗时
    elapsed_time = end_time - start_time
    
    # 打印响应内容和耗时
    if response.ok:
        result = response.json()
        print("Success!")
        print("Response:", result)
        print("-" * 50)
        print(f"Description: {result.get('description', 'No description found')}")
    else:
        print("Failed to get response:")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    
    print(f"\nRequest took {elapsed_time:.6f} seconds")

except requests.exceptions.ConnectionError:
    print("Error: Could not connect to the API server.")
    print("Please make sure the server is running on localhost:8080")
except requests.exceptions.RequestException as e:
    print(f"Request error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
