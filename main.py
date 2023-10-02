import sqlite3
from bs4 import BeautifulSoup
import requests
import time

print('Put skill that you are familiar with')
familiar_skill = input('>')
print(f'Filtering jobs that require {familiar_skill}')

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

def find_jobs():
    html_text = requests.get(f'https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords={familiar_skill}&txtLocation=').text
    soup = BeautifulSoup(html_text, 'lxml')
    jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')

    for index, job in enumerate(jobs):
        published_date = job.find('span', class_='sim-posted').span.text
        if 'few' in published_date:
            company_name = job.find('h3', class_='joblist-comp-name').text.strip()
            skills = job.find('span', class_='srp-skills').text.strip()
            more_info = job.header.h2.a['href']
            if familiar_skill in skills:
                cursor.execute("INSERT INTO jobs (company_name, skills, more_info) VALUES (?, ?, ?)",
                               (company_name, skills, more_info))
                conn.commit()
                print(f'Job data inserted into database: {index}')

if __name__ == '__main__':
    while True:
        find_jobs()
        time_wait = 10
        print(f'Waiting {time_wait} minutes...')
        time.sleep(time_wait * 60)

# Close the database connection when done
conn.close()
