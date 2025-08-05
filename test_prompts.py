import requests
import time
import os
import csv
import json
from pathlib import Path

API_URL = "http://localhost:8080/janus-pro"
PICS_DIR = "/home/echo/workspace/prompt_promoter/pics"
RESULTS_DIR = "/home/echo/workspace/prompt_promoter/test_results"

# 7个不同的prompt版本
PROMPT_VERSIONS = {
    "original": "You are a creative director for an AI video generator. This image is the first frame of a video. Your task is to write a concise, actionable prompt that describes the main subject's subsequent motion and camera movement. The prompt must follow the structure:[Motion],[Slight Camera work].",
    
    "version_a": "You are creating a video prompt from this image. Focus on describing the main subject's motion. Only add camera movement if it would enhance the scene significantly. Format: [Subject motion]. [Camera work if needed].",
    
    "version_b": "Describe what happens next in this image as a video. First describe the subject's movement, then optionally describe camera movement only if necessary. Use simple, direct language.",
    
    "version_c": "This image will become a video. Step 1: Describe how the main subject moves or acts. Step 2: Only if camera movement would improve the scene, describe it briefly. Keep it concise.",
    
    "version_d": "Generate a video description focusing on the subject's motion. Describe what the main subject does next. Camera movement is optional - only mention it if absolutely necessary for the scene.",
    
    "version_e": "Describe the subject's movement in this video scene. Focus on action and motion. Avoid camera descriptions unless essential. Keep it natural and simple.",
    
    "version_f": "What does the main subject do next? Describe their movement or action. Camera work: mention only if it significantly enhances the scene, otherwise focus purely on subject motion."
}

def ensure_results_dir():
    """确保结果目录存在"""
    os.makedirs(RESULTS_DIR, exist_ok=True)

def test_single_image_prompt(image_path, prompt, prompt_name):
    """测试单张图片和单个prompt"""
    json_payload = {
        "image_path": image_path,
        "prompt": prompt,
    }
    
    start_time = time.perf_counter()
    
    try:
        response = requests.post(API_URL, json=json_payload)
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        
        if response.ok:
            result = response.json()
            description = result.get('description', 'No description found')
            return {
                'success': True,
                'description': description,
                'elapsed_time': elapsed_time,
                'error': None
            }
        else:
            return {
                'success': False,
                'description': None,
                'elapsed_time': elapsed_time,
                'error': f"HTTP {response.status_code}: {response.text}"
            }
    except Exception as e:
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        return {
            'success': False,
            'description': None,
            'elapsed_time': elapsed_time,
            'error': str(e)
        }

def analyze_camera_movement(description):
    """分析描述中是否包含镜头运动"""
    if not description:
        return False
    
    camera_keywords = [
        'camera', 'zoom', 'push', 'pull', 'pan', 'tilt', 'rotate', 
        '镜头', '推进', '拉远', '旋转', '移动', 'tracking', 'follow',
        'shot', 'angle', 'view'
    ]
    
    description_lower = description.lower()
    return any(keyword in description_lower for keyword in camera_keywords)

def test_all_prompts():
    """测试所有prompt版本"""
    ensure_results_dir()
    
    # 获取所有图片文件
    image_files = sorted([f for f in os.listdir(PICS_DIR) if f.endswith('.jpg')])
    
    # 只测试前8张图片（对应CSV参考数据）
    test_images = image_files[:8]
    
    all_results = []
    
    print(f"开始测试 {len(test_images)} 张图片，{len(PROMPT_VERSIONS)} 个prompt版本")
    print("=" * 60)
    
    for img_file in test_images:
        image_path = os.path.join(PICS_DIR, img_file)
        img_num = img_file.split('.')[0]
        
        print(f"\n测试图片: {img_file}")
        print("-" * 30)
        
        for prompt_name, prompt_text in PROMPT_VERSIONS.items():
            print(f"  测试prompt: {prompt_name}")
            
            result = test_single_image_prompt(image_path, prompt_text, prompt_name)
            
            # 分析镜头运动
            has_camera_movement = analyze_camera_movement(result['description']) if result['success'] else False
            
            # 记录结果
            result_record = {
                'image_file': img_file,
                'image_number': img_num,
                'prompt_name': prompt_name,
                'prompt_text': prompt_text,
                'success': result['success'],
                'description': result['description'],
                'has_camera_movement': has_camera_movement,
                'elapsed_time': result['elapsed_time'],
                'error': result['error']
            }
            
            all_results.append(result_record)
            
            if result['success']:
                print(f"    ✓ 成功 ({result['elapsed_time']:.2f}s)")
                print(f"    镜头运动: {'是' if has_camera_movement else '否'}")
                print(f"    描述: {result['description'][:100]}...")
            else:
                print(f"    ✗ 失败: {result['error']}")
            
            time.sleep(1)  # 避免请求过快
    
    # 保存详细结果
    results_file = os.path.join(RESULTS_DIR, f"test_results_{int(time.time())}.csv")
    
    with open(results_file, 'w', newline='', encoding='utf-8') as f:
        fieldnames = ['image_file', 'image_number', 'prompt_name', 'prompt_text', 
                     'success', 'description', 'has_camera_movement', 'elapsed_time', 'error']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_results)
    
    print(f"\n详细结果已保存到: {results_file}")
    
    # 生成统计报告
    generate_summary_report(all_results)
    
    return all_results

def generate_summary_report(results):
    """生成统计报告"""
    print("\n" + "=" * 60)
    print("测试统计报告")
    print("=" * 60)
    
    # 按prompt版本统计
    for prompt_name in PROMPT_VERSIONS.keys():
        prompt_results = [r for r in results if r['prompt_name'] == prompt_name]
        successful_results = [r for r in prompt_results if r['success']]
        camera_movement_count = sum(1 for r in successful_results if r['has_camera_movement'])
        
        success_rate = len(successful_results) / len(prompt_results) * 100 if prompt_results else 0
        camera_rate = camera_movement_count / len(successful_results) * 100 if successful_results else 0
        avg_time = sum(r['elapsed_time'] for r in successful_results) / len(successful_results) if successful_results else 0
        
        print(f"\n{prompt_name.upper()}:")
        print(f"  成功率: {success_rate:.1f}% ({len(successful_results)}/{len(prompt_results)})")
        print(f"  镜头运动频率: {camera_rate:.1f}% ({camera_movement_count}/{len(successful_results)})")
        print(f"  平均耗时: {avg_time:.2f}s")
    
    # 保存统计报告
    summary_file = os.path.join(RESULTS_DIR, f"summary_report_{int(time.time())}.txt")
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("Prompt测试统计报告\n")
        f.write("=" * 40 + "\n\n")
        
        for prompt_name in PROMPT_VERSIONS.keys():
            prompt_results = [r for r in results if r['prompt_name'] == prompt_name]
            successful_results = [r for r in prompt_results if r['success']]
            camera_movement_count = sum(1 for r in successful_results if r['has_camera_movement'])
            
            success_rate = len(successful_results) / len(prompt_results) * 100 if prompt_results else 0
            camera_rate = camera_movement_count / len(successful_results) * 100 if successful_results else 0
            avg_time = sum(r['elapsed_time'] for r in successful_results) / len(successful_results) if successful_results else 0
            
            f.write(f"{prompt_name.upper()}:\n")
            f.write(f"  成功率: {success_rate:.1f}%\n")
            f.write(f"  镜头运动频率: {camera_rate:.1f}%\n")
            f.write(f"  平均耗时: {avg_time:.2f}s\n\n")
    
    print(f"\n统计报告已保存到: {summary_file}")

if __name__ == "__main__":
    print("开始批量测试prompt版本...")
    test_all_prompts()