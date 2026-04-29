from fpdf import FPDF
import base64

class PDFReport:
    def __init__(self, dataframe):
        self.df = dataframe
        self.pdf = FPDF()

    def generate(self):
        self.pdf.add_page()
        self.pdf.set_font("Arial", 'B', 16)
        
        # Header
        self.pdf.cell(0, 10, "Sales Intel Intelligence Report", 0, 1, 'C')
        self.pdf.ln(10)
        
        # Summary Stats
        self.pdf.set_font("Arial", '', 12)
        total_sales = self.df.iloc[:, -1].sum() # Assuming last column is sales
        self.pdf.cell(0, 10, f"Total Revenue Analyzed: ${total_sales:,.2f}", 0, 1)
        self.pdf.cell(0, 10, f"Total Transactions: {len(self.df)}", 0, 1)
        self.pdf.ln(10)

        # Table Header
        self.pdf.set_fill_color(0, 251, 255) # Neon Cyan matching your theme
        self.pdf.set_text_color(0)
        self.pdf.set_font("Arial", 'B', 10)
        
        # Columns (Sirf pehle 5 columns dikhatay hain PDF mein fit karne ke liye)
        cols = self.df.columns[:5]
        for col in cols:
            self.pdf.cell(38, 10, str(col), 1, 0, 'C', True)
        self.pdf.ln()

        # Data Rows
        self.pdf.set_font("Arial", '', 9)
        self.pdf.set_text_color(50)
        for _, row in self.df.head(20).iterrows(): # Sirf top 20 rows
            for col in cols:
                self.pdf.cell(38, 10, str(row[col])[:15], 1)
            self.pdf.ln()

        return self.pdf.output(dest='S').encode('latin-1')
