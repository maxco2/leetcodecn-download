import json
import os
import time
from functools import partial

from selenium import webdriver
from seleniumrequests import Chrome
from tqdm import tqdm


def login(driver: webdriver.Chrome):
    driver.get("https://leetcode-cn.com/accounts/login/")
    # login via chrome window
    time.sleep(15)


def graphql(driver: Chrome, gql: str):
    # driver.get("https://leetcode-cn.com/problemset/all/")
    token = driver.get_cookie("csrftoken")['value']
    # print('token:', token)
    url = "https://leetcode-cn.com/graphql/"
    data = json.loads(gql)
    response = driver.request('POST', url, headers={
        "x-csrftoken": token,
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36",
        'origin': 'https://leetcode-cn.com',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
    }, json=data)
    time.sleep(0.3)
    return response.json()


def get_accepted_list(driver: Chrome, max_attempt=20):
    from graphql_accepted import get_accepted_gql
    accepted_list = []
    skip = 0
    for i in range(max_attempt):
        x = graphql(driver, get_accepted_gql(skip=str(skip)))
        x: list = x["data"]["problemsetQuestionList"]["questions"]
        for c in x:
            d = {}
            d["title"] = c["title"]
            d["titleCn"] = c["titleCn"]
            d["titleSlug"] = c["titleSlug"]
            accepted_list.append(d)
        skip += len(x)
    return accepted_list


def get_submission_list(driver: Chrome, accepted_list: list):
    from graphql_submissions import get_submission_gql
    # ".data | .submissionList | .submissions | .[] | select(.statusDisplay == \"Accepted\") | {url,lang}"
    submission_list = []
    url = "https://leetcode-cn.com"
    for ac_problem in tqdm(accepted_list):
        slug = ac_problem["titleSlug"]
        # print("getting slug:", slug)
        while True:
            try:
                x = graphql(driver, get_submission_gql(question_slug=slug))
                break
            except:
                time.sleep(0.5)
                continue

        x = x["data"]["submissionList"]["submissions"]
        d = {}
        for c in x:
            if c["statusDisplay"] == "Accepted":
                d["url"] = url + c["url"]
                d["id"] = c["url"][20:-1]
                d["lang"] = c["lang"]
                break
        submission_list.append(d)

    return submission_list


def get_database_json(path: str, func):
    if not os.path.exists(path):
        j = func()
        with open(path, 'w') as f:
            json.dump(j, f)
    else:
        with open(path) as f:
            j = json.load(f)
    return j


def write_code_to_file(code, problem_id, slug, lang, cn_name):
    lang_comment = {
        "python3": "#",
        "python": "#",
        "java": "//",
        "cpp": "//",
        "c": "//",
        "bash": "#"
    }
    lang_extension = {
        "python3": "py",
        "python": "py",
        "java": "java",
        "cpp": "cpp",
        "c": "c",
        "bash": "sh"
    }
    comment = lang_comment.get(lang, "#")
    with open(f'./code/{slug}.{lang_extension.get(lang, "cpp")}', mode="w", encoding="utf-8", newline="") as f:
        f.writelines(
            f"{comment}\n{comment} @lc app=leetcode.cn id={problem_id} lang={lang}\n{comment}\n{comment} [{problem_id}] {slug} [{cn_name}]\n{comment}\n")
        f.writelines(code)
        f.writelines(f"\n{comment} @lc code=end")


def code_downloader(accepted_list: list, submission_list: list):
    from graphql_submission_detail import get_submission_detail_gql
    for problem_name, problem_submission in tqdm(zip(accepted_list, submission_list), total=len(accepted_list)):
        problem_id = problem_submission["id"]
        problem_slug = problem_name["titleSlug"]
        problem_cn_name = problem_name["titleCn"]
        lang = problem_submission["lang"]
        code = None
        sleep_time = 0.5
        while True:
            try:
                x = graphql(driver, get_submission_detail_gql(problem_id=problem_id))
                code = x["data"]["submissionDetail"]["code"]
                break
            except:
                sleep_time *= 2
                sleep_time = min(sleep_time, 5)
                time.sleep(sleep_time)
                continue
        write_code_to_file(code=code, problem_id=problem_id, slug=problem_slug, lang=lang, cn_name=problem_cn_name)


if __name__ == "__main__":
    driver = Chrome()
    login(driver)
    accepted_list_path = "./database/accepted_list.json"
    submission_list_path = "./database/submission_list.json"
    get_accepted_list = partial(get_accepted_list, driver=driver)
    accepted_list = get_database_json(accepted_list_path, get_accepted_list)
    get_submission_list = partial(get_submission_list, driver=driver, accepted_list=accepted_list)
    submission_list = get_database_json(submission_list_path, get_submission_list)
    code_downloader(accepted_list, submission_list)
