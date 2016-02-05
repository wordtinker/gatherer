#
# Script for parsing and getting page content from sites
#

import sqlite3
import httplib2
import os

from walla import *
from guardian import *
from register import *

MIN_WORDS = 40  # Minimum number of words in the article
PROJECT2OBJ = {
    'Walla': Walla,
    'Guardian': Guardian,
    'Register': Register
}

PROJECTS = (
    # {'site': 'Walla', 'section': '/category/2689'},  # Army and Safety
    # {'site': 'Walla', 'section': '/category/2686'},  # Politics
    # {'site': 'Walla', 'section': '/category/1'},  # Country
    # {'site': 'Walla', 'section': '/category/2'},  # World
    # {'site': 'Walla', 'section': '/category/5700'},  # Science
    # {'site': 'Walla', 'section': '/category/4996'},  # Religion
    {'site': 'Guardian', 'section': '/uk-news'},  # UK-news
    {'site': 'Register', 'section': ''},
)


def create_project(site, section):
    project = PROJECT2OBJ[site]
    return project(section)

conn = sqlite3.connect('projects.db')

# Initial DB setup #############################################################
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS articles(
    project TEXT,
    link TEXT PRIMARY KEY,
    visited BOOLEAN
    )''')
conn.commit()
# ##############################################################################

h = httplib2.Http('.cache')

# Gather new links from the pages
for description in PROJECTS:
    project = create_project(description['site'], description['section'])
    _, content = h.request(project.main_page, 'GET')
    content = content.decode(project.encoding)
    available_links = project.parse_page(content)
    for link in available_links:
        c.execute('''INSERT OR IGNORE INTO articles
            (project, link, visited) VALUES (?,?,?)''',
                  (project.name, link, False))
conn.commit()

# Get the page content
for row in c.execute('SELECT rowid, project, link FROM articles WHERE visited=0').fetchall():
    id, site, page = row

    print("Going to parse {}".format(page))
    project = create_project(site, '')
    _, content = h.request(page, 'GET')
    content = content.decode(project.encoding)
    article = project.parse_link(content)
    word_count = len(article.split())

    prj_dir = os.path.join(project.lang, 'corpus', project.name)
    if not os.path.exists(prj_dir):
        os.makedirs(prj_dir)
    if word_count >= MIN_WORDS:
        with open(os.path.join(prj_dir, str(id) + '.txt'), mode='w', encoding='utf-8') as f:
            f.write(article)
    c.execute('''UPDATE articles
     SET visited=1
     WHERE link=?
     ''', (page,))
    conn.commit()
