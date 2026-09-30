from app.ingestion.pdf_loader import extract_text_from_pdf

file_path = "data/pdf/PRFIP_Engineering_and_Operations_Documentation.pdf"

pages = extract_text_from_pdf(file_path)

print(f"Total pages: {len(pages)}")

for page in pages[:3]:
    print("==" * 20)
    print(f"Page {page['page_number']}:")
    print("==" * 20)
    print(page['text'][:500])  # Print the first 500 characters of each page
    print("\n---\n")