from fpdf import FPDF

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
        try:
            # Assuming the last column is numerical sales data
            total_sales = self.df.iloc[:, -1].sum()
            self.pdf.cell(0, 10, f"Total Revenue Analyzed: ${total_sales:,.2f}", 0, 1)
        except:
            self.pdf.cell(0, 10, "Total Revenue: Data Format Incompatible", 0, 1)
            
        self.pdf.cell(0, 10, f"Total Transactions: {len(self.df)}", 0, 1)
        self.pdf.ln(10)

        # Basic Table Header
        self.pdf.set_fill_color(0, 251, 255) 
        self.pdf.set_font("Arial", 'B', 10)
        cols = self.df.columns[:5]
        for col in cols:
            self.pdf.cell(38, 10, str(col), 1, 0, 'C', True)
        self.pdf.ln()

        # Data Rows
        self.pdf.set_font("Arial", '', 9)
        for _, row in self.df.head(20).iterrows():
            for col in cols:
                self.pdf.cell(38, 10, str(row[col])[:15], 1)
            self.pdf.ln()

        return self.pdf.output(dest='S').encode('latin-1')
