# imports

import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from IPython.display import Markdown, display
from openai import OpenAI

# If you get an error running this cell, then please head over to the troubleshooting notebook!

# Load environment variables in a file called .env

load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')

# Check the key

if not api_key:
    print("No API key was found - please head over to the troubleshooting notebook in this folder to identify & fix!")
elif not api_key.startswith("sk-proj-"):
    print("An API key was found, but it doesn't start sk-proj-; please check you're using the right key - see troubleshooting notebook")
elif api_key.strip() != api_key:
    print("An API key was found, but it looks like it might have space or tab characters at the start or end - please remove them - see troubleshooting notebook")
else:
    print("API key found and looks good so far!")

openai = OpenAI()

# A class to represent a Webpage
# If you're not familiar with Classes, check out the "Intermediate Python" notebook

# Some websites need you to use proper headers when fetching them:
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}


class Paper:

    def __init__(self, url):
        """
        Create this Website object from the given url using the BeautifulSoup library
        """
        self.url = url
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.title = soup.title.string if soup.title else "No title found"
        for irrelevant in soup.body(["script", "style", "img", "input"]):
            irrelevant.decompose()
        self.text = soup.body.get_text(separator="\n", strip=True)


# Insert Paper URL
res = Paper("insert url here")

system_prompt = """You are a research paper summarizer. You take the url of the research paper and extract the following:
1) Title and Author of the research paper.
2) Year it was published it
3) Objective or aim of the research to specify why the research was conducted
4) Background or Introduction to explain the need to conduct this research or any topics the readers must have knowledge about
5) Type of research/study/experiment to explain what kind of research it is.
6) Methods or methodology to explain what the researchers did to conduct the research
7) Results and key findings to explain what the researchers found
8) Conclusion tells about the conclusions that can be drawn from this research including limitations and future direction"""

# A function that writes a User Prompt that asks for summaries of websites:


def user_prompt_for(paper):
    user_prompt = f"You are looking at a website titled {paper.title}"
    user_prompt += "\nThe contents of this paper is as follows; \
please provide a short summary of this paper in markdown. \
If it includes additional headings, then summarize these too.\n\n"
    user_prompt += paper.text
    return user_prompt

# See how this function creates exactly the format above


def messages_for(paper):
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_for(paper)}
    ]


messages_for(res)

# And now: call the OpenAI API. You will get very familiar with this!


def summarize(url):
    paper = Paper(url)
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages_for(paper)
    )
    return response.choices[0].message.content

# A function to display this nicely in the Jupyter output, using markdown


def display_summary(url):
    summary = summarize(url)
    display(Markdown(summary))


# Insert Paper URL in the quotes below
display_summary(" ")
