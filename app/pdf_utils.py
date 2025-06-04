# ➕ Create remedy PDF
import os
from pathlib import Path

from weasyprint import HTML


def create_remedy_pdf(remedy_text: str, filename: str = "remedy.pdf") -> str:
    remedy_html = remedy_text.replace('\n', '<br>')
    html_content = (f"""
<html>
  <head>
    <meta charset="utf-8">
    <style>
      body {{ font-family: sans-serif; margin: 20px; }}
      h1 {{ color: #2c3e50; }}
      p {{ line-height: 1.6; }}
    </style>
  </head>
  <body>
    <h1>Home Remedy for Kids</h1>
    <p>{remedy_html}</p>
  </body>
</html>
""")
    # Create a path object for the 'pdfs' directory
    pdf_dir = Path("./pdfs")
    pdf_dir.mkdir(parents=True, exist_ok=True)

    # Full path to the PDF file
    pdf_path = pdf_dir / filename

    # Generate the PDF
    HTML(string=html_content).write_pdf(str(pdf_path))

    return str(pdf_path)
