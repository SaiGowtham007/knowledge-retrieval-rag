from app.ingestion.ingestion_pipeline import extract_text

files = [
    "data/pdf/PRFIP_Engineering_and_Operations_Documentation.pdf",
    "data/docx/PRFIP_Business_Data_API_Model_Documentation.docx",
    "data/payment_risk_requirements.txt"
]

for file_path in files:
    text = extract_text(file_path)

    print(file_path)

    print("Characters extracted:", len(text))
    print("\nFirst 500 characters")
    print("\n")
    print(text[:500])