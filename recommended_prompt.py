#!/usr/bin/env python3
"""
推荐的janus-pro prompt配置
基于测试结果选出的最优prompt

测试结果摘要:
- 原始prompt镜头运动频率: 100%
- 推荐prompt镜头运动频率: 37.5%
- 改进幅度: 62.5%
- 平均耗时: 0.86s
"""

# 最优prompt (Version E)
RECOMMENDED_PROMPT = "Describe the subject's movement in this video scene. Focus on action and motion. Avoid camera descriptions unless essential. Keep it natural and simple."

# 备选prompt (如果需要更快执行)
ALTERNATIVE_FAST_PROMPT = "What does the main subject do next? Describe their movement or action. Camera work: mention only if it significantly enhances the scene, otherwise focus purely on subject motion."

# 使用示例
def create_video_prompt_payload(image_path, use_alternative=False):
    """创建API请求载荷"""
    prompt = ALTERNATIVE_FAST_PROMPT if use_alternative else RECOMMENDED_PROMPT
    
    return {
        "image_path": image_path,
        "prompt": prompt
    }

# 测试对比结果
PERFORMANCE_COMPARISON = {
    "original": {
        "camera_movement_rate": 100.0,
        "avg_time": 0.74,
        "description": "强制输出镜头运动"
    },
    "recommended": {
        "camera_movement_rate": 37.5,
        "avg_time": 0.86,
        "description": "最佳平衡版本"
    },
    "alternative_fast": {
        "camera_movement_rate": 50.0,
        "avg_time": 0.80,
        "description": "快速执行版本"
    }
}

if __name__ == "__main__":
    print("推荐的janus-pro prompt:")
    print(f'"{RECOMMENDED_PROMPT}"')
    print("\n性能对比:")
    for name, stats in PERFORMANCE_COMPARISON.items():
        print(f"  {name}: 镜头运动率 {stats['camera_movement_rate']}%, 耗时 {stats['avg_time']}s")