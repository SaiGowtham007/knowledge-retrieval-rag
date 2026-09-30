import pymupdf

def extract_text_from_pdf(file_path: str) ->  str:
    document = pymupdf.open(file_path)

    pages = []
    for page_number, page in enumerate(document, start=1):
        text = page.get_text().strip()

        if text:
            pages.append(
                "text" = text,
                "page_number" = page_number
            )

    document.close()

    return "\n".join(pages)