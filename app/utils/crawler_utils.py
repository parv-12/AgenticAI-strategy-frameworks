import requests
import json
import os

crawler_url = "http://localhost:7002/browseddg"
crawler_output_path = "D:/UserData/z0049n3z/SIBC Hackathon/spider/out"

def get_top_n_json_from_jsonl(file_path, n=10):
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for _ in range(n):
            # Read each line and parse it as JSON
            line = file.readline()
            if not line:
                break  # End of file reached
            json_data = json.loads(line)
            data.append(json_data)
    return data

def crawl_web(topic:str) -> dict:
    search_items = {
        "About": f"About {topic}",
        "Latest_news": f"Latest news on {topic}",
        "Companies": f"Companies working on {topic}",
        "Products": f"Best products in the market for {topic}"
    }
    search_results = {}
    for key, search_item in search_items.items():
        os.remove(f"{crawler_output_path}/{key}.jsonl")
        payload = {
            "searchTerm": search_item,
            "outputFile": f"out/{key}.jsonl"
        }
        requests.post(crawler_url, json=payload)
        search_result = ""
        top_5_json = get_top_n_json_from_jsonl(f"{crawler_output_path}/{key}.jsonl", n=10)
        count=0
        for i in top_5_json:
            search_result = search_result + f"{str(count+1)}. {i['title']}\nLink: {i['hyperlink']}\nSnippet:{i['snippet']}"
            count += 1
        search_results[search_item] = search_result
    return search_results



