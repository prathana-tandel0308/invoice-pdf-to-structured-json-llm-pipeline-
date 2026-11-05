# Invoice PDF to Structured JSON Using Local and Cloud LLMs

An intelligent Python-based invoice processing system that converts PDF invoices into structured JSON using a combination of local and cloud-based Large Language Models (LLMs).

The project uses **PyMuPDF4LLM** to extract text from PDF invoices, **Ollama with Llama 3.2** to identify relevant invoice information, and **Google Gemini** to extract structured data. The extracted information is validated using **Pydantic** and can be processed through a **Streamlit web application**.

---

## Project Overview

Invoices often contain information in different layouts, formats, and structures. Manually extracting invoice details can be time-consuming and error-prone.

This project automates invoice data extraction by combining local and cloud-based LLMs.

The local LLM filters the invoice content and selects relevant information, reducing the amount of text sent to the cloud model. Google Gemini then extracts the required invoice fields and returns structured JSON.

The final output is validated using a Pydantic schema.

### Key Features

- Extract text from PDF invoices using PyMuPDF4LLM.
- Support OCR for scanned PDF invoices.
- Clean extracted Markdown text.
- Use a local LLM (Llama 3.2 through Ollama) to identify relevant invoice content.
- Reduce unnecessary invoice text before sending it to the cloud LLM.
- Achieve **34% input token reduction** through local LLM-based content filtering in the tested data.
- Use Google Gemini for structured invoice data extraction.
- Validate extracted information using Pydantic.
- Handle missing or unclear invoice information using `null` values.
- Convert invoice information into structured JSON.
- Track token usage and token reduction.
- Measure invoice processing time.
- Provide an interactive Streamlit web interface.
- Process multiple invoice PDFs through the batch-processing pipeline.

---

## System Architecture

The project follows a hybrid local and cloud LLM architecture.

```text
                  PDF Invoice
                       |
                       v
             PyMuPDF4LLM + OCR
                       |
                       v
              Markdown Extraction
                       |
                       v
                 Text Cleaning
                       |
                       v
              Split into Blocks
                       |
                       v
             Local LLM (Llama 3.2)
                  via Ollama
                       |
                       v
           Relevant Content Selection
                       |
                       v
             Filtered Markdown
                       |
                       v
              Google Gemini API
                       |
                       v
           Structured Data Extraction
                       |
                       v
              Pydantic Validation
                       |
                       v
               Structured JSON
                       |
                       v
                Final Output
```

### Why Use Local and Cloud LLMs?

The project uses two LLMs for different responsibilities.

**1. Local LLM – Llama 3.2**

- Runs locally through Ollama.
- Identifies relevant invoice content.
- Selects text blocks containing information related to the required invoice fields.
- Reduces irrelevant text before cloud processing.
- Does not perform the final invoice field extraction.

**2. Cloud LLM – Google Gemini**

- Receives the filtered invoice Markdown.
- Extracts the required invoice information.
- Produces structured JSON.
- Uses the Pydantic schema to maintain the expected output structure.

This hybrid approach aims to reduce unnecessary cloud input tokens while keeping the final extraction task separate from local content filtering.

---

## Invoice Fields Extracted

The system extracts the following nine fields:

| Field | Description |
|---|---|
| `supplier_name` | Name of the invoice supplier |
| `customer_name` | Name of the customer |
| `invoice_number` | Invoice identification number |
| `invoice_date` | Date on which the invoice was issued |
| `due_date` | Payment due date |
| `subtotal` | Invoice amount before tax |
| `tax` | Tax amount |
| `total` | Final invoice amount |
| `currency` | Currency used in the invoice |

### Example JSON Output

```json
{
  "supplier_name": "Zylker",
  "customer_name": "Rob & Joe Traders",
  "invoice_number": "INV-17",
  "invoice_date": "2018-05-21",
  "due_date": "2018-05-21",
  "subtotal": "630.00",
  "tax": "32.75",
  "total": "662.75",
  "currency": "INR"
}
```

*Note: This is an illustrative example of the expected JSON structure. Actual extracted values depend on the invoice content and OCR accuracy.*

### Handling Missing Information

If a field is missing, unclear, or cannot be reliably identified, the system represents it as `null`.

For example:

```json
{
  "supplier_name": "Example Supplier",
  "customer_name": null,
  "invoice_number": "INV-001",
  "invoice_date": "2025-01-15",
  "due_date": null,
  "subtotal": "1000.00",
  "tax": null,
  "total": "1000.00",
  "currency": "INR"
}
```

Dates are represented in ISO format (`YYYY-MM-DD`), and monetary values are handled using Python's `Decimal` type.

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| PyMuPDF4LLM | PDF-to-Markdown conversion |
| RapidOCR | OCR support for scanned invoices |
| Ollama | Running the local LLM |
| Llama 3.2 | Local invoice content filtering |
| Google Gemini API | Cloud-based structured data extraction |
| Google Gen AI SDK | Python integration with Gemini |
| Pydantic | Data validation and schema enforcement |
| Streamlit | Interactive web application |
| Tiktoken | Token counting and comparison |
| Requests | HTTP communication where required |
| Python-dotenv | Environment variable management |

---

## Project Structure

```text
invoice-pdf-to-structured-json/
│
├── app.py
├── main.py
├── performance_evaluation.py
├── validation.py
├── requirements.txt
├── .gitignore
└── README.md
│
├── config/
│   └── settings.py
│
├── src/
│   ├── __init__.py
│   ├── pdf_extractor.py
│   ├── text_cleaner.py
│   ├── header_footer_remover.py
│   ├── markdown_block_splitter.py
│   ├── prompt_builder.py
│   ├── local_llm_filter.py
│   ├── llm_extractor.py
│   ├── schemas.py
│   └── token_counter.py
│
├── results_examples/
    ├── test_pdf_to_markdown.py
    ├── test_local_llm_filter.py
    ├── test_llm_extractor.py
    ├── test_schema.py
    ├── test_markdown_blocks.py
    ├── test_header_footer.py
    ├── test_gemini_models.py

```

*Note: This structure describes the intended project organization. Some output folders are generated when the pipeline runs.*

---

## Installation and Setup

Follow these steps to run the project locally.

### 1. Clone the Repository

```bash
git clone https://github.com/prathana-tandel0308/invoice-pdf-to-structured-json-llm-pipeline-.git
```

Navigate to the project directory:

```bash
cd invoice-pdf-to-structured-json-llm-pipeline-
```

If you already have the project folder on your computer, you can use that folder instead of cloning it again.

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Install and Set Up Ollama

Download and install Ollama:

https://ollama.com/download

Pull the Llama 3.2 model:

```bash
ollama pull llama3.2
```

Check the installed model:

```bash
ollama list
```

Make sure Ollama is running before executing the local filtering pipeline.

### 5. Configure the Gemini API Key

Obtain a Gemini API key from:

https://aistudio.google.com/apikey

Create a `.env` file in the project root directory:

```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-3.6-flash
LOCAL_LLM_MODEL=llama3.2
```

Use the Gemini model configured in your `config/settings.py` and ensure it is available to your API project.

**Important:** Never upload your `.env` file or expose your API key on GitHub.

---

## How to Run the Project

### Option 1: Run the Streamlit Web Application

Start the application using:

```bash
python -m streamlit run app.py
```

The Streamlit application provides an interface for uploading and processing invoice PDFs.

Typical workflow:

1. Open the Streamlit application.
2. Upload an invoice PDF.
3. Extract the PDF content into Markdown.
4. Clean the extracted text.
5. Filter relevant content using the local LLM.
6. Extract invoice information using Gemini.
7. Validate the extracted information.
8. View the structured JSON output.
9. Download the generated JSON.

### Option 2: Run Batch Invoice Processing

To process multiple PDF invoices from the configured input folder, execute:

```bash
python main.py
```

The batch pipeline processes invoice PDFs and saves intermediate and final outputs in the corresponding folders.

### Option 3: Run Performance Evaluation

To evaluate token reduction, execute:

```bash
python performance_evaluation.py
```

The performance evaluation compares token counts before and after local LLM filtering.

### Option 4: Run Validation

To validate the generated JSON files against expected invoice data, execute:

```bash
python validation.py
```

---

## Token Reduction and Performance Evaluation

One of the main objectives of this project is to evaluate whether local LLM-based filtering reduces the amount of invoice text sent to the cloud LLM.

The project compares:

- Token count of cleaned invoice Markdown.
- Token count of filtered invoice Markdown.
- Percentage reduction in input text tokens.

### Token Reduction Formula

```text
Token Reduction (%) =
((Original Tokens - Filtered Tokens) / Original Tokens) × 100
```

### Achieved Token Reduction

<badge color="success" size="lg">34% Token Reduction</badge>

The local LLM filtering stage achieved a **34% reduction in input tokens** in the tested invoice data.

This means that the filtered Markdown contained approximately 34% fewer tokens than the original cleaned Markdown.

The result demonstrates how local LLM-based content selection can reduce the amount of invoice text that needs to be sent to Google Gemini for structured data extraction.

**Important:** Tiktoken's `cl100k_base` encoding is used for token comparison in the current implementation. Its counts are estimates and may differ from the actual token counts reported by Gemini.

Actual Gemini usage metadata is the appropriate source for measuring API-reported token consumption.

---

## Validation and Testing

The project includes test scripts for checking individual pipeline components.

| Test File | Purpose |
|---|---|
| `test_pdf_to_markdown.py` | Tests PDF-to-Markdown conversion |
| `test_local_llm_filter.py` | Tests local LLM filtering |
| `test_llm_extractor.py` | Tests Gemini extraction |
| `test_schema.py` | Tests the Pydantic invoice schema |
| `test_markdown_blocks.py` | Tests Markdown block splitting |
| `test_header_footer.py` | Tests repeated header and footer removal |
| `test_gemini_models.py` | Checks available Gemini models |

Run an individual test using:

```bash
python test_pdf_to_markdown.py
```

Replace the filename to run another test script.

---

## Expected Benefits

- Automates invoice information extraction.
- Reduces manual data-entry work.
- Supports different invoice layouts.
- Supports OCR-based extraction for scanned invoices.
- Separates local content filtering from cloud-based data extraction.
- Achieved **34% input token reduction** through local LLM-based invoice content filtering in the tested data.
- Aims to reduce unnecessary cloud input tokens.
- Produces consistent JSON output.
- Validates extracted information using a predefined schema.
- Supports batch processing and web-based interaction.

---

## Limitations

- OCR accuracy depends on PDF quality, scan resolution, and document layout.
- Complex tables and unusual invoice formats may affect extraction accuracy.
- Local LLM filtering may accidentally omit relevant information.
- Gemini API usage is subject to model-specific quotas and rate limits.
- Token counts from Tiktoken may differ from Gemini's reported usage.

---

## Future Improvements

Potential improvements include:

- Add caching to avoid repeated Gemini API requests for unchanged invoices.
- Add quota-aware error handling and retry mechanisms.
- Improve local LLM filtering accuracy.
- Add support for more invoice formats and languages.
- Improve extraction accuracy for complex invoice tables.
- Add automated evaluation of extraction accuracy.
- Add detailed processing-time and token-usage reports.
- Support exporting invoice data to CSV and Excel.
- Add a history of previously processed invoices.

---

## Security and Privacy

- Store API credentials in environment variables.
- Keep `.env` excluded from Git.
- Avoid uploading real invoices containing sensitive customer or supplier information to public repositories.
- Review extracted invoice data before using it in business operations.
- Be aware that filtered invoice content is sent to Google's Gemini API for cloud-based extraction.

---

## Author

**Project:** Invoice PDF to Structured JSON Using Local and Cloud LLMs

**GitHub Repository:**  
https://github.com/prathana-tandel0308/invoice-pdf-to-structured-json-llm-pipeline-

---

## License

This project is intended for learning, experimentation, and demonstration purposes. Add a license file if you intend to distribute or reuse the project under specific license terms.
