# coding: utf-8

from selenium.webdriver import Chrome
from selenium.common.exceptions import WebDriverException
import requests
from retrying import retry

import json
import time
import pprint
import traceback


def wait_for(fn, timeout=5):
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            return fn()
        except WebDriverException:
            time.sleep(0.1)
    # one more try, which will raise any errors if they are outstanding
    return fn()


def find_by_css(selector):
    def _find():
        return driver.find_element_by_css_selector(selector)

    return wait_for(_find)


def find_linkedin_url(term):
    params = {
        'key': 'AIzaSyBs_qRMdd3UxIp6HQ9zMidKupXkRCtmZrQ',
        'cx': '007098471526848933106:c_yqy7e87hi',
        'q': term
    }
    r = requests.get(
        'https://www.googleapis.com/customsearch/v1', params=params)
    r_json = r.json()

    for item in r_json['items']:
        if 'pagemap' in item and 'person' in item['pagemap']:
            return item['link']


@retry(stop_max_delay=6000)
def get_contact_linkedin_html(name, company):
    term = u"{} {}".format(name, company)
    url = find_linkedin_url(term)
    if not url:
        raise ValueError(u"No result for {}".format(term))
    driver.get(url)
    return find_by_css('#profile').get_attribute('innerHTML'), url


driver = Chrome()
driver.set_window_size(1280, 700)
results = []


def main():
    with open('attendees.json') as f:
        attendees_raw = json.load(f)

    attendees = [(a['name'], a['info2']) for a in attendees_raw
                 if 'info2' in a]

    for name, company in attendees:
        try:
            html, link = get_contact_linkedin_html(name, company)
        except Exception:
            print traceback.print_exc()
            html = None
            link = None
        results.append({
            'name': name,
            'company': company,
            'html': html,
            'link': link
        })

    print len(results)
    with open('results.json', 'w+') as out:
        json.dump(results, out, indent=2)
    driver.quit()


if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- ran in %s seconds ---" % (time.time() - start_time))
