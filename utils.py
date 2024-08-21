from markdown_pdf import MarkdownPdf, Section


def create_pdf(markdown_content: str):
    pdf = MarkdownPdf()
    pdf.meta["title"] = 'Generated Content'
    pdf.add_section(Section(markdown_content, toc=False))
    pdf.save('output.pdf')
