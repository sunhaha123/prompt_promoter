# 我的需求：
为了进行图生视频的任务，需要用到一张图片和result_text, 所以现在的需求是根据相关原则来给janus-pro接口设计一个新的prompt输入，使得这个接口输出的result_text能符合一下原则，原则如下：“图像已经确定了主体、场景与风格，因此提示词主要描述动态过程及运镜需求。提示词 = 运动 + 运镜,运动描述：结合图像中的元素（如人物、动物），描述其相动态的过程，如奔跑、打招呼，可以通过形容词来控制动态的程度与速度，如“快速地”、“缓慢地”。
运镜：若对镜头运动有特定要求(非必须)，通过提示词如“镜头推进”、“镜头左移”控制，若希望镜头不要发生变化，可以通过“固定镜头”来强调。

# 测试资源
测试资源是pics下的20张图片，可以利用接口轮询并分析结果

/home/echo/workspace/prompt_promoter/try_janus_pro_local.py 的janus-pro接口。它的输入是一段prompt和一张图片，输出是一段result_text.

1~8.csv的结果可以仅供参考，只求神似

# 开发环境
conda activate agent

# 我的担忧
janus-pro这个模型只有1b，能力较弱，可能再语义遵从和改写上不尽如人意

# 我之前实验过的prompt
You are a creative director for an AI video generator. This image is the first frame of a video. Your task is to write a concise, actionable prompt that describes the main subject's subsequent motion and camera movement. The prompt must follow the structure:[Motion],[Slight Camera work].
但这个prompt的不好地方在于100%会输出镜头运动，但这其实并不是必须的


Describe what happens next in this image as a video. First describe the subject's movement, then optionally describe camera movement only if necessary. Use simple, direct language.
目前较好

# 期望的得到的结果
对比pics下面的图片再不同prompt下输出的结果，选出最好的，如果都不行，再改进prompt
