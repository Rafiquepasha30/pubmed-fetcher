import requests
import pandas as pd
import re
from typing import List, Dict, Tuple

PUBMED_SEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
PUBMED_SUMMARY_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"

def fetch_pubmed_ids(query: str) -> List[str]:
    """Fetch paper IDs from PubMed based on the query."""
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": 10  # Fetch up to 10 results
    }
    response = requests.get(PUBMED_SEARCH_URL, params=params)
    response.raise_for_status()
    data = response.json()

    return data.get("esearchresult", {}).get("idlist", [])

def fetch_paper_details(pubmed_ids: List[str]) -> List[Dict[str, str]]:
    """Fetch details for a list of PubMed IDs."""
    if not pubmed_ids:
        return []

    params = {
        "db": "pubmed",
        "id": ",".join(pubmed_ids),
        "retmode": "json"
    }
    response = requests.get(PUBMED_SUMMARY_URL, params=params)
    response.raise_for_status()
    data = response.json()

    papers = []
    for pubmed_id in pubmed_ids:
        details = data["result"].get(pubmed_id, {})
        title = details.get("title", "Unknown")
        pub_date = details.get("pubdate", "Unknown")
        authors = details.get("authors", []) or []  # Ensures authors is always a list

        non_academic_authors, company_affiliations = extract_non_academic_authors(authors)

        paper_info = {
            "PubmedID": pubmed_id,
            "Title": title,
            "Publication Date": pub_date,
            "Non-academic Author(s)": ", ".join(non_academic_authors) if non_academic_authors else "None",
            "Company Affiliation(s)": ", ".join(company_affiliations) if company_affiliations else "None",
            "Corresponding Author Email": "Not Available"
        }
        papers.append(paper_info)

    return papers

def extract_non_academic_authors(authors: List[Dict[str, str]]) -> Tuple[List[str], List[str]]:
    """Identify non-academic authors based on their affiliations."""
    non_academic_authors = []
    company_affiliations = []

    for author in authors:
        name = author.get("name", "Unknown")
        affiliation = author.get("affiliation", "")

        if affiliation and not re.search(r"university|school|college|lab", affiliation, re.IGNORECASE):
            non_academic_authors.append(name)
            company_affiliations.append(affiliation)

    return non_academic_authors, company_affiliations

def save_to_csv(papers: List[Dict[str, str]], filename: str):
    """Save the list of papers to a CSV file."""
    df = pd.DataFrame(papers)
    df.to_csv(filename, index=False)
    print(f"Results saved to {filename}")
