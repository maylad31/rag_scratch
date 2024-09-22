
import glob
from pypdf import PdfReader
from cleantext import clean
from typing import List,Generator
from tqdm import tqdm
def divide_chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]


def extract_from_pdfs(root:str,chunk_size:int=5):
    """extract data from pdfs
    """
    all_files = glob.glob("**/*.pdf",root_dir=root,recursive=True)
    for chunk in tqdm(list(divide_chunks(all_files,chunk_size))):
        res = []
        for path in chunk:
            doc = PdfReader(f"{root}/{path}")
            text=""
            for page in doc.pages[:3]: # iterate the document pages
                text += page.extract_text()
            #print(text)
            text =  clean(text,lower=False,no_line_breaks=True)
            text = " ".join(text.split()[:7000])
            res.append(text)
        yield res,chunk


if __name__=="__main__":
    for data in extract_from_pdfs("./data"):
        print(data)
        break
            
        