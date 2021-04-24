from fpdf import FPDF, set_global
import json
import os
import sys

class PDF(FPDF):
    def __init__(self, orientation, unit, format, hasSpaceLeft=False):
        # location of font folder - need to use truetype font for unicode support
        set_global('SYSTEM_TTFONTS', os.path.join(os.getcwd(), 'font'))
        self.hasSpaceLeft = hasSpaceLeft
        super().__init__(orientation, unit, format)

    def set_author(self, author):
        self.author = author

    def header(self):
        if self.page_no() is 1:
            return
        self.set_font('NotoSerif', 'I', 8)
        self.set_y(2)
        self.cell(0, 5, self.title)
        if self.author is not None:
            self.cell(0, 5, self.author, align='R')
        self.ln(10)

    def add_cover_page(self):
        self.set_font('NotoSerif', '', 24)
        self.set_y(20)
        self.multi_cell(0, 10, self.title, "", "L")
        if self.author is not None:
            self.set_font('NotoSerif', 'I', 12)
            self.cell(0, 10, self.author)
        self.add_page()

    def add_highlight(self, body, note, location):
        width = 0 if self.hasSpaceLeft else 146
        if location is not None:
            if self.hasSpaceLeft:
                self.set_x(64)
            self.set_font('NotoSerif', 'B', 6)
            self.cell(18, 5, f"Location {str(location)}", 0, 1)
        if note is not None:
            if self.hasSpaceLeft:
                self.set_x(64)
            self.set_font('NotoSerif', 'I', 10)
            self.multi_cell(width, 5, note)
            self.ln(1)
        if self.hasSpaceLeft:
            self.set_x(64)
        self.set_font('NotoSerif', '', 10)
        self.multi_cell(width, 5, body, "L")
        self.ln(5)
    
    def create(self, article, filename):
        self.add_font("NotoSerif", style="", fname="NotoSerif-Regular.ttf", uni=True)
        self.add_font("NotoSerif", style="B", fname="NotoSerif-Bold.ttf", uni=True)
        self.add_font("NotoSerif", style="I", fname="NotoSerif-Italic.ttf", uni=True)
        if article.get('title') is not None:
            self.set_title(article.get('title'))
        if article.get('authors') is not None:
            self.set_author(article.get('authors'))
        self.set_left_margin(4)
        self.set_right_margin(4)
        self.set_auto_page_break(True, 6)
        self.add_page()
        self.add_cover_page()
        for highlight in article.get('highlights'):
            self.add_highlight(highlight.get('text'), highlight.get('note'), highlight.get('location', {}).get('value'))
        self.output(filename, 'F')

if __name__ == '__main__':
    filename = sys.argv[1]
    with open(filename, 'r', encoding='utf8') as f:
        article = json.load(f)
    if article.get('highlights') is None:
        print("Error: input file does not have highlights")
        exit()
    pdf = PDF('P', 'mm', 'Letter', False)
    pdf.create(article, filename.replace(".json", ".pdf"))