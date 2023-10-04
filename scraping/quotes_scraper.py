import requests
from lxml import html
import matplotlib.pyplot as plt
from collections import Counter
import random
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Generate a random page number (1 to 10 in this example)
random_page = random.randint(1, 10)

# Create the URL with the random page number
url = f"http://quotes.toscrape.com/page/{random_page}/"

# Make an HTTP request
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content
    tree = html.fromstring(response.text)
else:
    print("Failed to retrieve the page.")
    exit()

# Extract Data
# Extract quotes and authors using XPath
quotes = tree.xpath('//span[@class="text"]/text()')
authors = tree.xpath('//small[@class="author"]/text()')

# Count Author Occurrences
# Count the number of quotes per author
author_counts = Counter(authors)

# Create a bar chart
# Get the top authors and their counts (e.g., top 10 authors)
top_authors = author_counts.most_common(10)

# Separate author names and counts
author_names, counts = zip(*top_authors)

# Create a pie chart for top authors
fig, axs = plt.subplots(1, 2, figsize=(12, 6))
axs[0].barh(author_names, counts)
axs[0].set_xlabel("Number of Quotes")
axs[0].set_ylabel("Authors")
axs[0].set_title("Top Authors by Number of Quotes")

axs[1].pie(counts, labels=author_names, autopct="%1.1f%%", startangle=140)
axs[1].axis("equal")
axs[1].set_title("Distribution of Quotes Among Top Authors")

# Create a Tkinter window to display the charts and quotes
root = tk.Tk()
root.title("Quotes and Charts")

# Create a label to display the quotes by the most quoted author
most_quoted_author = top_authors[0][0]
most_quoted_author_quotes = [quote for i, quote in enumerate(quotes) if authors[i] == most_quoted_author]
quotes_text = "\n\n".join([f"{i+1}. {quote}" for i, quote in enumerate(most_quoted_author_quotes)])
quote_label = tk.Text(root, wrap=tk.WORD, width=40, height=10)
quote_label.insert(tk.END, f"Quotes by the author with the highest number of quotes ({most_quoted_author}):\n\n{quotes_text}")
quote_label.pack()

# Embed the matplotlib figure in the Tkinter window
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# Run the Tkinter main loop
root.mainloop()
