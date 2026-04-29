from fpdf import FPDF

class PDFReport:
    def __init__(self, dataframe):
        self.df = dataframe
        self.pdf = FPDF()

    def generate(self):
        self.pdf.add_page()
        self.pdf.set_fill_color(10, 10, 12)
        self.pdf.rect(0, 0, 210, 40, 'F')
        self.pdf.set_font("Arial", 'B', 20)
        self.pdf.set_text_color(0, 251, 255)
        self.pdf.cell(0, 20, "SALES INTEL TERMINAL REPORT", 0, 1, 'C')
        self.pdf.ln(20)
        self.pdf.set_text_color(0)
        self.pdf.set_font("Arial", 'B', 14)
        self.pdf.cell(0, 10, f"Total Transactions: {len(self.df)}", 0, 1)
        return self.pdf.output(dest='S').encode('latin-1')
