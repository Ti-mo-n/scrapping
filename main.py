import sqlite3
from bs4 import BeautifulSoup
import requests

# Create a SQLite database and table
conn = sqlite3.connect('jobs.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_name TEXT,
        skills TEXT,
        more_info TEXT
    )
''')
conn.commit()

while True:
    print('Put skill that you are familiar with (or type "exit" to end)')
    familiar_skill = input('>')
    if familiar_skill.lower() == 'exit':
        break

    print(f'Filtering jobs that require {familiar_skill}')


    def find_jobs(skill):
        html_text = requests.get(
            f'https://www.timesjobs.com/candidate/job-search.html?'
            f'searchType=personalizedSearch&from=submit&txtKeywords={skill}&txtLocation=').text
        soup = BeautifulSoup(html_text, 'lxml')
        jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')

        for index, job in enumerate(jobs):
            published_date = job.find('span', class_='sim-posted').span.text
            if 'few' in published_date:
                company_name = job.find('h3', class_='joblist-comp-name').text.strip()
                skills = job.find('span', class_='srp-skills').text.strip()
                more_info = job.header.h2.a['href']
                if skill in skills:
                    cursor.execute("INSERT INTO jobs (company_name, skills, more_info) VALUES (?, ?, ?)",
                                   (company_name, skills, more_info))
                    conn.commit()
                    print(f'Job data inserted into database: {index}')


    find_jobs(familiar_skill)

# Close the database connection when done
conn.close()
