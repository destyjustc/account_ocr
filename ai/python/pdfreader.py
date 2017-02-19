from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO


def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = file(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()
    fstr = ''
    count = 0
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages,    password=password,caching=caching, check_extractable=True):
        count += 1
        interpreter.process_page(page)

        currentpage = retstr.getvalue()
        text_file = open("/home/yong.zhang/Dropbox/OCR/results/Output" + str(count) + ".txt", "w")
        text_file.write(currentpage)
        text_file.close()
        fstr += currentpage

    fp.close()
    device.close()
    retstr.close()
    return fstr

txt = convert_pdf_to_txt("/home/yong.zhang/Dropbox/OCR/results/fund.pdf")
text_file = open("/home/yong.zhang/Dropbox/OCR/results/Output.txt", "w")
text_file.write(txt)
text_file.close()
print(txt)