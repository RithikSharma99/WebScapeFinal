import requests
from bs4 import BeautifulSoup as bs
import json
import os
from collections import OrderedDict

if not os.path.isdir("./Data/"):
    os.mkdir("Data1")

print("\nRequesting Data...")
# Request Data
try:
    URL = "http://www.gk-questions.leadthecompetition.in/"
    r = requests.get(URL)
    content = r.content
except:
    print("Connection Failed!")

print("\nFetching Data...")
# Soup Creation
soup = bs(content, "html.parser")
div_ids = ["general", "daysandyears", "banking", "constitution"]
topics = {}  # The links required to be scraped

for ids in div_ids:
    for topic in soup.find_all("div", id=ids):
        for links in topic.find_all("a"):
            topics[links.text.strip(" ")] = URL + links['href']

all_data = []
match_ans = {
    "a": 1,
    "b": 2,
    "c": 3,
    "d": 4
}
for topic, link in topics.items():
    final_data = OrderedDict()
    final_data["Topic"] = topic
    final_data["Subject"] = "General Knowledge"
    data_ques = []

    r = requests.get(link)
    soup = bs(r.content, "html.parser")
    for mcqs in soup.find_all("div", class_="portfolio-item"):
        ques_on = 0
        answer_cnt = 1
        data = []
        for ele in mcqs.find_all("p"):
            to_append = OrderedDict()
            question = ele.text[3:].strip(" ").replace("\n", "").replace("\t", "")\
                .replace("\r", "")
            if "Choice Questions" not in question:
                to_append['Question'] = question
                # print(to_append)
                try:
                    opts = mcqs.find_all("ol", class_="alpha")[
                        ques_on].find_all("li")
                    for num, opt in enumerate(opts):
                        to_append[f"op{num+1}"] = opt.text.strip(" ").replace("\n", "")\
                            .replace("\t", "").replace("\r", "")

                    answer = mcqs.find_all("strong")[answer_cnt].text[8]
                    to_append["Answer"] = match_ans[answer]
                    answer_cnt += 1
                    ques_on += 1
                except:
                    ques_on += 1
                    answer_cnt += 1

                data.append(to_append)
        data_ques.extend(data[:-1])
    final_data["Data"] = data_ques

    print("\nWriting Data to JSON...")
    with open(f"./Data/{topic}.json", "w") as file:
        json.dump(final_data, file)

print("\nDone!!!")
