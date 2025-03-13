import argparse
from pubmed_fetcher.fetch_papers import fetch_pubmed_ids, fetch_paper_details, save_to_csv

def main():
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed.")
    parser.add_argument("query", type=str, help="Search query for PubMed")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("-f", "--file", type=str, help="Specify output CSV filename")

    args = parser.parse_args()

    if args.debug:
        print(f"Fetching papers for query: {args.query}")

    pubmed_ids = fetch_pubmed_ids(args.query)
    if not pubmed_ids:
        print("No papers found.")
        return

    papers = fetch_paper_details(pubmed_ids)
    
    if args.file:
        save_to_csv(papers, args.file)
    else:
        for paper in papers:
            print(paper)

if __name__ == "__main__":
    main()
