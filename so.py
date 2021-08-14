import requests
from bs4 import BeautifulSoup

URL = "https://stackoverflow.com/jobs?tl=python"


def find_max_page():
    html = requests.get(f"{URL}")
    soup = BeautifulSoup(html.text, 'html.parser')
    pagination_list = soup.find("div", {
        "class": "s-pagination"
    }).find_all("span")
    pages = []
    for page in pagination_list[:-1]:
        pages.append(page.string)
    max_page = int(pages[-1])
    return max_page


def extract_job_in_page(html):
    jobs_in_page = []
    soup = html.find_all("div", {"class": "-job"})
    for content in soup:
        title = content.find("h2").find("a")["title"]
        company, location = content.find("h3").find_all("span", recursive=False)
        company = company.get_text().strip()
        location = location.get_text().strip()
        job_id = content["data-jobid"]
        job = {
            'title':
            title,
            'company':
            company,
            'location':
            location,
            'link':
            f"https://stackoverflow.com/jobs/{job_id}"
        }
        jobs_in_page.append(job)
    return jobs_in_page


def extract_jobs(max_page):
    jobs = []
    for page in range(max_page):
        print(f"Scrapping SO page: {page+1}")
        html = requests.get(f"{URL}&pg={page+1}")
        soup = BeautifulSoup(html.text, 'html.parser')
        jobs_in_page = extract_job_in_page(soup)
        jobs += jobs_in_page
    return jobs


def get_jobs():
    max_page = find_max_page()
    jobs = extract_jobs(max_page)
    return jobs
