import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://kr.indeed.com/%EC%B7%A8%EC%97%85?q=python&limit={LIMIT}&radius=25"


def find_max_page():
    html = requests.get(f"{URL}&start=0")
    soup = BeautifulSoup(html.text, 'html.parser')
    pagination_list = soup.find("ul", {
        "class": "pagination-list"
    }).find_all("li")
    pages = []
    for page in pagination_list[:-1]:
        pages.append(int(page.string))
    max_page = pages[-1]
    return max_page


def extract_job_in_page(html):
    jobs_in_page = []
    soup = html.find_all("a", {"class": "sponTapItem"})
    for content in soup:
        title = content.find("h2").find("span", {"class": ""}).string
        company_temp = content.find("span", {"class": "companyName"})
        if company_temp is not None:
            company = company_temp.string
        else:
            company = "Company isn't loaded"
        location = content.find("div", {"class": "companyLocation"}).string
        job_id = content["data-jk"]
        job = {
            'title':
            title,
            'company':
            company,
            'location':
            location,
            'link':
            f"https://kr.indeed.com/viewjob?jk={job_id}&tk=1fcvtme7bsmfq800&from=serp&vjs=3"
        }
        jobs_in_page.append(job)
    return jobs_in_page


def extract_jobs(max_page):
    jobs = []
    for page in range(max_page):
        print(f"Scrapping Indeed page: {page+1}")
        html = requests.get(f"{URL}&start={page*LIMIT}")
        soup = BeautifulSoup(html.text, 'html.parser')
        jobs_in_page = extract_job_in_page(soup)
        jobs += jobs_in_page
    return jobs


def get_jobs():
    max_page = find_max_page()
    jobs = extract_jobs(max_page)
    return jobs
