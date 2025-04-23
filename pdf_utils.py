# ➕ Create remedy PDF
import os

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
    os.makedirs("pdfs", exist_ok=True)
    pdf_path = f"./pdfs/{filename}"
    HTML(string=html_content).write_pdf(pdf_path)
    return pdf_path
