"""
PDF页码分析脚本
用于确定PDF的页码偏移量
"""

try:
    import pypdf

    def analyze_pdf(pdf_path, book_name):
        """分析PDF文件"""
        print(f"\n{'='*50}")
        print(f"分析: {book_name}")
        print(f"{'='*50}")

        try:
            pdf = pypdf.PdfReader(pdf_path)
            total_pages = len(pdf.pages)
            print(f"PDF总页数: {total_pages}")

            # 检查前50页
            print("\n搜索章节内容...")
            chapter_found = False

            for i in range(min(50, total_pages)):
                page = pdf.pages[i]
                text = page.extract_text()

                if text:
                    # 查找章节标记
                    keywords = ['第一章', '第1章', 'Chapter 1', '第一章', '绪论',
                               '第二章', '第2章', '第三章', '第3章']

                    for keyword in keywords:
                        if keyword in text:
                            print(f"\n>>> 第{i+1}页找到: {keyword}")
                            # 显示周围文本
                            start = max(0, text.find(keyword) - 20)
                            end = min(len(text), text.find(keyword) + 100)
                            print(f"内容: ...{text[start:end]}...")
                            chapter_found = True
                            break

                    if chapter_found and i > 5:
                        # 找到第一章后继续检查是否为正文开始
                        break

            if not chapter_found:
                print("\n未找到明确的章节标记")
                print("这可能是扫描版PDF（图片格式）")
                print("建议：手动打开PDF，查看第一章开始页码")

            # 尝试读取目录/书签
            try:
                outline = pdf.outline
                if outline:
                    print("\nPDF包含目录/书签:")
                    print_outline(outline, level=0)
            except:
                print("\nPDF无内置目录/书签")

        except Exception as e:
            print(f"错误: {e}")

    def print_outline(outline, level):
        """打印目录结构"""
        for item in outline:
            if isinstance(item, list):
                print_outline(item, level + 1)
            else:
                indent = "  " * level
                try:
                    page_num = item.page.number + 1 if hasattr(item, 'page') and item.page else "?"
                    print(f"{indent}- {item.title} (第{page_num}页)")
                except:
                    print(f"{indent}- {item.title}")

    # 分析三本书
    books = [
        ("c:/Users/lsq/Documents/Obsidian Vault/math/数值计算方法/电子书/数值计算方法 第二版.pdf", "数值计算方法"),
        ("c:/Users/lsq/Documents/Obsidian Vault/math/简明大学物理学/电子书/简明大学物理学.pdf", "简明大学物理学"),
        ("c:/Users/lsq/Documents/Obsidian Vault/math/线性代数/电子书/线性代数.pdf", "线性代数"),
    ]

    for pdf_path, book_name in books:
        analyze_pdf(pdf_path, book_name)

except ImportError:
    print("请先安装 pypdf 库:")
    print("pip install pypdf")
