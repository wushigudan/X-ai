import requests
import json
import time
from datetime import datetime

class FunArticleGenerator:
    """
    有趣文章生成器
    用于生成生动有趣且专业的技术文章
    支持批量处理MD文件中的标题
    """
    
    def __init__(self):
        """初始化生成器，设置API密钥和代理"""
        # API配置
        self.api_key = "you-key"
        self.url = 'https://api.x.ai/v1/chat/completions'
        
        # 请求头设置
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        
        # 代理设置（用于解决网络访问问题）
        self.proxies = {
            'http': 'http://127.0.0.1:10809',
            'https': 'http://127.0.0.1:10809'
        }
        
    def generate_fun_article(self, title):
        """
        生成有趣且详细的文章
        
        Args:
            title (str): 文章标题
            
        Returns:
            str: 生成的文件名，失败返回None
        """
        try:
            # 系统角色设定：定义AI的写作风格和能力
            system_prompt = """你是一位极其专业且风趣幽默的技术作家，擅长：
1. 用生动有趣的方式解释复杂的技术概念
2. 善于使用类比和比喻
3. 能把枯燥的内容变得引人入胜
4. 在保持专业性的同时让读者感到轻松愉快
5. 文章结构清晰，内容充实
6. 擅长讲故事，善于引用实际案例"""

            # 用户提示词：详细的文章要求
            user_prompt = f"""请为主题"{title}"写一篇详尽的技术文章，要求：

1. 文章结构：
   - 开场：用一个有趣的故事或比喻引入主题
   - 背景介绍：解释为什么这个主题重要
   - 核心内容：分3-4个部分详细展开
   - 实际案例：至少2个真实的案例分析
   - 技术细节：深入但易懂的技术讲解
   - 总结：幽默而发人深省的结尾

2. 写作风格：
   - 像跟朋友聊天一样自然
   - 适当使用俏皮话和双关语
   - 多用生动的比喻
   - 可以加入一些梗和笑点
   - 段落之间要有良好的过渡

3. 内容要求：
   - 每个概念都要配合例子
   - 技术讲解要循序渐进
   - 适当加入小贴士和注意事项
   - 包含一些实用的最佳实践
   - 预测未来发展趋势

4. 互动元素：
   - 设置一些思考问题
   - 加入一些小测验
   - 提供实践建议
   - 鼓励读者参与讨论

请确保文章既专业又有趣，让读者在轻松愉快中学到知识。"""
            
            # 构建API请求
            payload = {
                "messages": [
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ],
                "model": "grok-beta",  # 使用grok-beta模型
                "stream": False,        # 不使用流式输出
                "temperature": 0.8      # 增加创造性，取值范围0-1
            }
            
            # 发送API请求
            print(f"\n正在为 '{title}' 生成文章...")
            response = requests.post(
                self.url,
                headers=self.headers,
                json=payload,
                proxies=self.proxies,
                verify=False,           # 忽略SSL验证
                timeout=60              # 60秒超时
            )
            
            # 处理响应
            if response.status_code == 200:
                # 提取生成的内容
                content = response.json()['choices'][0]['message']['content']
                
                # 生成文件名
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                safe_title = title.replace('?', '').replace('/', '_').replace(':', '_')
                filename = f"fun_article_{safe_title}_{timestamp}.md"
                
                # 保存文章
                with open(filename, 'w', encoding='utf-8') as f:
                    # 写入标题和时间
                    f.write(f"# {title}\n\n")
                    f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                    f.write("---\n\n")  # 分隔线
                    # 写入主要内容
                    f.write(content)
                    # 添加结束语
                    f.write("\n\n---\n\n")
                    f.write("欢迎在评论区分享你的想法和经验！")
                    
                print(f"\n文章已生成: {filename}")
                print(f"使用token数: {response.json()['usage']['total_tokens']}")
                return filename
                
            else:
                print(f"生成失败: {response.status_code}")
                print(response.text)
                return None
                
        except Exception as e:
            print(f"生成文章时出错: {str(e)}")
            return None

    def process_md_file(self, filename):
        """
        处理MD文件中的标题
        
        Args:
            filename (str): MD文件名
        """
        try:
            # 读取文件内容
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 解析所有标题（以#开头的行）
            titles = []
            for line in content.split('\n'):
                if line.startswith('#'):
                    title = line.lstrip('#').strip()
                    if title:
                        titles.append(title)
                        
            if not titles:
                print("未找到标题")
                return
                
            # 显示找到的标题
            print(f"\n找到 {len(titles)} 个标题:")
            for i, title in enumerate(titles, 1):
                print(f"{i}. {title}")
                
            # 用户选择要处理的标题
            choice = input("\n请选择要处理的标题编号 (输入'all'处理所有): ")
            
            if choice.lower() == 'all':
                # 批量处理所有标题
                for i, title in enumerate(titles, 1):
                    print(f"\n=== 处理第 {i}/{len(titles)} 个标题 ===")
                    self.generate_fun_article(title)
                    time.sleep(2)  # 避免请求过快
            else:
                # 处理单个标题
                try:
                    idx = int(choice) - 1
                    if 0 <= idx < len(titles):
                        self.generate_fun_article(titles[idx])
                    else:
                        print("无效的选择")
                except ValueError:
                    print("请输入有效的数字")
                    
        except Exception as e:
            print(f"处理文件失败: {str(e)}")

def main():
    """主函数：处理用户交互和文件选择"""
    generator = FunArticleGenerator()
    
    # 列出当前目录下的所有md文件
    import os
    md_files = [f for f in os.listdir('.') if f.endswith('.md')]
    
    if not md_files:
        print("当前目录下没有找到MD文件")
        return
        
    # 显示可用的MD文件
    print("找到以下MD文件:")
    for i, file in enumerate(md_files, 1):
        print(f"{i}. {file}")
        
    # 用户选择文件
    try:
        choice = int(input("\n请选择要处理的文件编号: "))
        if 1 <= choice <= len(md_files):
            generator.process_md_file(md_files[choice-1])
        else:
            print("无效的选择")
    except ValueError:
        print("请输入有效的数字")

if __name__ == "__main__":
    main() 
