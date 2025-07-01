import pdfplumber

def extract_text_pdfplumber(file_path):
    print(f"🚀 Starting PDF Extraction using pdfplumber...")
    print(f"🔵 Opening file: {file_path}")

    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            total_pages = len(pdf.pages)
            print(f"✅ PDF has {total_pages} pages.")

            for i, page in enumerate(pdf.pages):
                print(f"➡️ Reading page {i + 1}...")
                page_text = page.extract_text()

                # 🔍 Diagnostic Print: Show the raw extracted content
                print(f"📝 Raw extracted content from page {i + 1}: {repr(page_text)}")

                if page_text:
                    print(f"🟢 Page {i + 1} text extracted successfully.")
                    text += page_text + "\n\n"
                else:
                    print(f"⚠️ Page {i + 1} has no extractable text.")

    except Exception as e:
        print(f"❌ Error opening PDF: {e}")
        return ""

    if text.strip():
        print("✅ Text extraction completed successfully using pdfplumber.")
    else:
        print("⚠️ No text extracted from the PDF.")

    return text


if __name__ == "__main__":
    file_path = "sample.pdf"  # 👉 Replace with your actual PDF file name
    extracted_text = extract_text_pdfplumber(file_path)

    print(f"\n🟢 Total extracted text length: {len(extracted_text)} characters.")

    if extracted_text.strip():
        print("\n✅ Final Extracted Text Preview (First 1000 Characters):\n")
        print(extracted_text[:1000])
    else:
        print("\n❌ No text could be extracted from the provided PDF.")
