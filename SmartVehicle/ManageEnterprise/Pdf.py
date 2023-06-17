from fpdf import FPDF


class PDF(FPDF):

    def __init__(self, header_text):
        super().__init__()
        self.header_text = header_text

    def header(self):
        self.set_font('Times', 'BI', 13)
        #self.cell(0, 10, 'Repair Invoice', 1, 1, 'C')
        self.cell(0, 10, self.header_text , align='C')
        self.ln(20)
        self.image('reparacion.png', x=self.w - 30, y=5, w=20)

    def footer(self):
        self.set_y(-15)
        self.set_font('Times', 'I', 8)
        self.cell(0, 10, 'Página %s' % self.page_no(), 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Times', 'B', 12)
        self.cell(0, 20, title, 0, 1, 'L')
        self.ln(20)

    def date_body(self, date, space):
        self.set_font('Times', 'I', 9)
        self.set_left_margin(25)
        self.multi_cell(0, 5, date)
        if space == 1:
        
          self.ln(10)



    def chapter_body(self, content):
        self.set_font('Times', 'I', 12)

        self.set_left_margin(35)
        self.multi_cell(0, 5, content)
        self.ln(1)

    def chapter_price(self, content):
        self.set_font('Times', 'I', 12)

        self.set_left_margin(35)
        self.multi_cell(0, 5, content)
        self.ln(17)


    def chapter_body_line(self, content):
        self.set_font('Times', 'I', 12)

        self.set_left_margin(35)
        self.multi_cell(0, 5, content)
        self.ln(1)

        x1 = self.get_x()
        y1 = self.get_y()
        x2 = x1 + self.w
        self.line(x1, y1, x2-70, y1)
