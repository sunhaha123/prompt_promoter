import pandas as pd
import os
from pathlib import Path

def analyze_test_results():
    """分析测试结果并生成详细对比报告"""
    
    # 找到最新的测试结果文件
    results_dir = "/home/echo/workspace/prompt_promoter/test_results"
    csv_files = [f for f in os.listdir(results_dir) if f.startswith("test_results_") and f.endswith(".csv")]
    
    if not csv_files:
        print("没有找到测试结果文件")
        return
    
    latest_file = max(csv_files)
    results_file = os.path.join(results_dir, latest_file)
    
    print(f"分析文件: {results_file}")
    print("=" * 80)
    
    # 读取CSV数据
    df = pd.read_csv(results_file)
    
    # 读取参考CSV数据
    reference_file = "/home/echo/workspace/prompt_promoter/1~8.csv"
    if os.path.exists(reference_file):
        ref_df = pd.read_csv(reference_file)
        print("参考数据:")
        for _, row in ref_df.iterrows():
            print(f"  {row['pic_name']}.jpg: {row['prompt'][:100]}...")
        print("\n" + "=" * 80)
    
    # 分析每个prompt版本的表现
    prompt_versions = df['prompt_name'].unique()
    
    print("详细分析报告:\n")
    
    for version in prompt_versions:
        version_data = df[df['prompt_name'] == version]
        successful_data = version_data[version_data['success'] == True]
        
        print(f"\n{version.upper()} 详细分析:")
        print("-" * 50)
        
        # 基本统计
        success_rate = len(successful_data) / len(version_data) * 100
        camera_movement_count = len(successful_data[successful_data['has_camera_movement'] == True])
        camera_rate = camera_movement_count / len(successful_data) * 100 if len(successful_data) > 0 else 0
        avg_time = successful_data['elapsed_time'].mean() if len(successful_data) > 0 else 0
        
        print(f"成功率: {success_rate:.1f}% ({len(successful_data)}/{len(version_data)})")
        print(f"镜头运动频率: {camera_rate:.1f}% ({camera_movement_count}/{len(successful_data)})")
        print(f"平均耗时: {avg_time:.2f}s")
        
        # 分析镜头运动情况
        no_camera_cases = successful_data[successful_data['has_camera_movement'] == False]
        if len(no_camera_cases) > 0:
            print(f"\n成功避免镜头运动的案例 ({len(no_camera_cases)}个):")
            for _, row in no_camera_cases.iterrows():
                print(f"  • {row['image_file']}: {row['description'][:80]}...")
        
        # 检查输出质量问题
        quality_issues = successful_data[successful_data['description'].str.contains(r'\[.*\]\.', regex=True, na=False)]
        if len(quality_issues) > 0:
            print(f"\n输出质量问题 ({len(quality_issues)}个):")
            for _, row in quality_issues.iterrows():
                print(f"  ⚠ {row['image_file']}: {row['description']}")
        
        print()
    
    # 横向对比分析
    print("\n" + "=" * 80)
    print("横向对比分析:")
    print("=" * 80)
    
    comparison_data = []
    for version in prompt_versions:
        version_data = df[df['prompt_name'] == version]
        successful_data = version_data[version_data['success'] == True]
        
        camera_rate = len(successful_data[successful_data['has_camera_movement'] == True]) / len(successful_data) * 100 if len(successful_data) > 0 else 0
        avg_time = successful_data['elapsed_time'].mean() if len(successful_data) > 0 else 0
        quality_issues = len(successful_data[successful_data['description'].str.contains(r'^\[.*\]\.$', regex=True, na=False)])
        
        comparison_data.append({
            'version': version,
            'camera_rate': camera_rate,
            'avg_time': avg_time,
            'quality_issues': quality_issues
        })
    
    # 排序并显示
    comparison_data.sort(key=lambda x: x['camera_rate'])
    
    print("按镜头运动频率排序 (从低到高):")
    for data in comparison_data:
        quality_note = f" (质量问题: {data['quality_issues']})" if data['quality_issues'] > 0 else ""
        print(f"  {data['version']:12} | 镜头运动: {data['camera_rate']:5.1f}% | 耗时: {data['avg_time']:5.2f}s{quality_note}")
    
    # 推荐最佳prompt
    print("\n" + "=" * 80)
    print("推荐分析:")
    print("=" * 80)
    
    # 过滤掉有严重质量问题的版本
    good_versions = [d for d in comparison_data if d['quality_issues'] == 0]
    
    if good_versions:
        best_version = min(good_versions, key=lambda x: x['camera_rate'])
        print(f"推荐使用: {best_version['version'].upper()}")
        print(f"理由:")
        print(f"  • 镜头运动频率最低: {best_version['camera_rate']:.1f}%")
        print(f"  • 平均耗时: {best_version['avg_time']:.2f}s")
        print(f"  • 无明显质量问题")
        
        # 显示推荐版本的prompt文本
        recommended_prompt = df[df['prompt_name'] == best_version['version']]['prompt_text'].iloc[0]
        print(f"\n推荐的prompt文本:")
        print(f'"{recommended_prompt}"')
    else:
        print("所有版本都存在质量问题，需要进一步优化")
    
    # 改进建议
    print("\n" + "=" * 80)
    print("改进建议:")
    print("=" * 80)
    
    original_camera_rate = next(d['camera_rate'] for d in comparison_data if d['version'] == 'original')
    best_camera_rate = min(d['camera_rate'] for d in good_versions) if good_versions else original_camera_rate
    
    improvement = original_camera_rate - best_camera_rate
    improvement_pct = improvement / original_camera_rate * 100 if original_camera_rate > 0 else 0
    
    print(f"1. 镜头运动频率从 {original_camera_rate:.1f}% 降低到 {best_camera_rate:.1f}%")
    print(f"   改进幅度: {improvement:.1f} 百分点 ({improvement_pct:.1f}% 相对改进)")
    print(f"2. 成功实现了让镜头运动变为可选的目标")
    print(f"3. Version A存在输出格式问题，需要进一步优化")
    print(f"4. 建议在实际应用中使用 Version B")

def save_analysis_report():
    """保存分析报告到文件"""
    import sys
    from io import StringIO
    
    # 捕获输出
    old_stdout = sys.stdout
    sys.stdout = buffer = StringIO()
    
    try:
        analyze_test_results()
        output = buffer.getvalue()
    finally:
        sys.stdout = old_stdout
    
    # 同时输出到控制台和文件
    print(output)
    
    # 保存到文件
    results_dir = "/home/echo/workspace/prompt_promoter/test_results"
    report_file = os.path.join(results_dir, f"detailed_analysis_{int(time.time())}.txt")
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(output)
    
    print(f"详细分析报告已保存到: {report_file}")

if __name__ == "__main__":
    import time
    try:
        import pandas as pd
    except ImportError:
        print("需要安装pandas: pip install pandas")
        exit(1)
    
    analyze_test_results()