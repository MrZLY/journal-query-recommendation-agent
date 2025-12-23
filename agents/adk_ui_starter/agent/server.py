import arxiv
import json
import os
from typing import List
from mcp.server.fastmcp import FastMCP
import requests
from duckduckgo_search import DDGS
from dotenv import load_dotenv
from tavily import TavilyClient

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

PAPER_DIR = "papers"

# Initialize FastMCP server
#mcp = FastMCP("research", host = "localhost", port=50001)
mcp = FastMCP("research", host="0.0.0.0", port=50001)

@mcp.tool()
def search_papers(topic: str, max_results: int = 5) -> List[str]:
    """
    Search for papers on arXiv based on a topic and store their information.

    Args:
        topic: The topic to search for
        max_results: Maximum number of results to retrieve (default: 5)

    Returns:
        List of paper IDs found in the search
    """

    # Use arxiv to find the papers
    client = arxiv.Client()

    # Search for the most relevant articles matching the queried topic
    search = arxiv.Search(
        query=topic,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )

    papers = client.results(search)

    # Create directory for this topic
    path = os.path.join(PAPER_DIR, topic.lower().replace(" ", "_"))
    os.makedirs(path, exist_ok=True)

    file_path = os.path.join(path, "papers_info.json")

    # Try to load existing papers info
    try:
        with open(file_path, "r") as json_file:
            papers_info = json.load(json_file)
    except (FileNotFoundError, json.JSONDecodeError):
        papers_info = {}

    # Process each paper and add to papers_info  
    paper_ids = []
    for paper in papers:
        paper_ids.append(paper.get_short_id())
        paper_info = {
            'title': paper.title,
            'authors': [author.name for author in paper.authors],
            'summary': paper.summary,
            'pdf_url': paper.pdf_url,
            'published': str(paper.published.date())
        }
        papers_info[paper.get_short_id()] = paper_info

    # Save updated papers_info to json file
    with open(file_path, "w") as json_file:
        json.dump(papers_info, json_file, indent=2)

    print(f"Results are saved in: {file_path}")

    return paper_ids

@mcp.tool()
def extract_info(paper_id: str) -> str:
    """
    Search for information about a specific paper across all topic directories.

    Args:
        paper_id: The ID of the paper to look for

    Returns:
        JSON string with paper information if found, error message if not found
    """

    for item in os.listdir(PAPER_DIR):
        item_path = os.path.join(PAPER_DIR, item)
        if os.path.isdir(item_path):
            file_path = os.path.join(item_path, "papers_info.json")
            if os.path.isfile(file_path):
                try:
                    with open(file_path, "r") as json_file:
                        papers_info = json.load(json_file)
                        if paper_id in papers_info:
                            return json.dumps(papers_info[paper_id], indent=2)
                except (FileNotFoundError, json.JSONDecodeError) as e:
                    print(f"Error reading {file_path}: {str(e)}")
                    continue

    return f"There's no saved information related to paper {paper_id}."

@mcp.tool()
def web_search(query: str) -> str:
    """
    使用 Tavily API 执行网络搜索。
    Args:
        query: 要搜索的关键词。
    Returns:
        一个包含搜索结果的字符串。
    """
    print(f"正在使用 Tavily API 执行网络搜索: {query}...")
    tavily_api_key = os.environ.get("TAVILY_API_KEY")
    if not tavily_api_key:
        return "错误: TAVILY_API_KEY 环境变量未设置。"

    try:
        client = TavilyClient(api_key=tavily_api_key)
        # 使用 Tavily 的高级搜索功能，它会进行更深入的研究并返回摘要
        response = client.search(query=query, search_depth="advanced")
        
        # Tavily 的 search_depth="advanced" 会返回一个包含"answer"键的字典
        # 如果有答案，直接返回答案
        if response.get("answer"):
            return response["answer"]

        # 如果没有直接的答案，格式化返回搜索结果
        results = response.get("results", [])
        if not results:
            return "Tavily API 没有返回相关结果。"

        formatted_results = []
        for res in results:
            formatted_results.append(f"标题: {res.get('title', 'N/A')}\n链接: {res.get('url', 'N/A')}\n内容: {res.get('content', 'N/A')}\n---")
        
        return "\n".join(formatted_results)

    except Exception as e:
        return f"使用 Tavily API 搜索时出错: {e}"
@mcp.tool()
# def web_search(query: str) -> str:
#     """
#     使用 DuckDuckGo 执行网络搜索并返回结果。
#     Args:
#         query: 要搜索的关键词。
#     Returns:
#         一个包含搜索结果摘要的字符串。
#     """
#     print(f"正在执行网络搜索: {query}...")
#     try:
#         # 使用 with DDGS() 来确保会话被正确关闭
#         with DDGS() as ddgs:
#             # 我们获取前5个结果
#             results = list(ddgs.text(query, max_results=5))
        
#         if not results:
#             return "网络搜索没有找到相关结果。"
        
#         # 将结果格式化为易于阅读的字符串
#         formatted_results = []
#         for i, res in enumerate(results, 1):
#             formatted_results.append(f"结果 {i}:\n标题: {res.get('title', 'N/A')}\n链接: {res.get('href', 'N/A')}\n摘要: {res.get('body', 'N/A')}\n---")
        
#         return "\n".join(formatted_results)

#     except Exception as e:
#         return f"网络搜索时出错: {e}"
@mcp.tool()
def doaj_journal_info(journal_title: str) -> str:
    """
    从 DOAJ (Directory of Open Access Journals) 搜索开放获取期刊的信息。
    Args:
        journal_title: 要查询的期刊标题。
    Returns:
        一个包含期刊信息的 JSON 字符串，如果找不到则返回提示信息。
    """
    print(f"正在 DOAJ 中搜索期刊: {journal_title}...")
    try:
        # DOAJ API 的地址
        api_url = f"https://doaj.org/api/search/journals/{requests.utils.quote(journal_title)}"
        
        response = requests.get(api_url)
        response.raise_for_status()  # 确保请求成功
        
        data = response.json()
        
        if data.get("total", 0) > 0:
            # 我们只返回最相关的第一个结果的详细信息
            journal_data = data["results"][0]
            bibjson = journal_data.get("bibjson", {})
            
            # 提取关键信息
            info = {
                "title": bibjson.get("title"),
                "publisher": bibjson.get("publisher"),
                "issns": bibjson.get("issn"),
                "apc": journal_data.get("apc"),
                "subjects": [subj.get("term") for subj in bibjson.get("subject", [])],
                "url": bibjson.get("ref", {}).get("url"),
            }
            return json.dumps(info, indent=2, ensure_ascii=False)
        else:
            return f"在 DOAJ 中没有找到标题为 '{journal_title}' 的开放获取期刊。"

    except requests.RequestException as e:
        return f"调用 DOAJ API 时出错: {e}"
    except Exception as e:
        return f"处理 DOAJ 数据时发生未知错误: {e}"


if __name__ == "__main__":
    # Initialize and run the server
    #mcp.run(transport='streamable-http')
    mcp.run(transport='sse')
