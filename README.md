# pubmed-fetcher
Overview
This project fetches research papers from PubMed based on a user-specified query. It filters papers with at least one author affiliated with a pharmaceutical or biotech company and returns the results in a CSV file.

1 Install Poetry
Poetry is used for dependency management. Install it using:
pip install poetry

2 Clone the Repository
git clone https://github.com/Rafiquepasha30/pubmed-fetcher.git
cd pubmed-fetcher

3 Install Dependencies
Run the following command inside the project directory:
poetry install

# Running the CLI Tool

The CLI tool allows you to fetch research papers based on a query and save the results.
Basic Usage
poetry run get-papers-list "cancer research"
This will fetch research papers related to "cancer research" and print the results in the console.

Save Results to a CSV File
poetry run get-papers-list "cancer research" -f results.csv
This will save the results to results.csv.

Enable Debug Mode
poetry run get-papers-list "cancer research" -d
This prints additional debugging information.

View Help Menu
poetry run get-papers-list -h
This displays available options and usage instructions.

# Logic Behind Filtering Non-Academic Authors

The program identifies non-academic authors based on their affiliations. Here’s how it works:

1 Extract Author Information:
The program retrieves the list of authors from the PubMed API response.

2 Check for Non-Academic Institutions:
If an author's affiliation contains words like university, school, college, or lab, they are considered academic.
If an author does not have these keywords in their affiliation, they are considered non-academic.

3 Return Non-Academic Authors & Company Names:
The program extracts the names of non-academic authors and their affiliated companies.

