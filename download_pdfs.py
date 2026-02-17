"""Download all publication PDFs into static/files/pdfs/ for self-hosting."""
import os
import urllib.request

OUT = os.path.join(os.path.dirname(__file__), "static", "files", "pdfs")

# Map: paper_number -> (filename, source_url)
PDFS = {
    27: ("paper_27.pdf", "https://www.gao.caltech.edu/uploads/2/6/7/2/26723767/sciadv.adw9024.pdf"),
    26: ("paper_26.pdf", "https://www.gao.caltech.edu/uploads/2/6/7/2/26723767/scitranslmed.adt0882.pdf"),
    25: ("paper_25.pdf", "https://www.gao.caltech.edu/uploads/2/6/7/2/26723767/sciadv.adx6491.pdf"),
    24: ("paper_24.pdf", "https://www.gao.caltech.edu/uploads/2/6/7/2/26723767/s41928-025-01407-0.pdf"),
    23: ("paper_23.pdf", "https://www.gao.caltech.edu/uploads/2/6/7/2/26723767/s41563-024-02096-4.pdf"),
    22: ("paper_22.pdf", "https://www.jihong-min.com/_files/ugd/f42095_afc5027565c94409bf77435c8e65d52b.pdf"),
    21: ("paper_21.pdf", "https://www.jihong-min.com/_files/ugd/f42095_3c5edb183ca7445bab650e7d86126e13.pdf"),
    20: ("paper_20.pdf", "https://www.jihong-min.com/_files/ugd/f42095_840ecd1a12324991a8eb630dbbf273c0.pdf"),
    19: ("paper_19.pdf", "https://www.jihong-min.com/_files/ugd/f42095_e2745a9050d94644bb45cbe5b85df457.pdf"),
    18: ("paper_18.pdf", "https://www.jihong-min.com/_files/ugd/f42095_1fb105dd805f407495622a62987b6f8f.pdf"),
    17: ("paper_17.pdf", "https://www.jihong-min.com/_files/ugd/f42095_2da1baf727ca4ab7af14048d40ce7cc6.pdf"),
    16: ("paper_16.pdf", "https://www.jihong-min.com/_files/ugd/f42095_5596ab71a3124742a2d7229431c0ad89.pdf"),
    15: ("paper_15.pdf", "https://www.jihong-min.com/_files/ugd/f42095_521d1155efe74befaba35a0f56f24827.pdf"),
    # 14: no PDF
    13: ("paper_13.pdf", "https://www.jihong-min.com/_files/ugd/f42095_124abca61d91465f9cc26a765b1211fa.pdf"),
    # 12: no PDF
    11: ("paper_11.pdf", "https://www.jihong-min.com/_files/ugd/f42095_fd56707b87a64d91848d9051bbc01e92.pdf"),
    10: ("paper_10.pdf", "https://www.jihong-min.com/_files/ugd/f42095_f2fb2c75ba5c41f8820162b2653590d0.pdf"),
    9:  ("paper_09.pdf", "https://www.jihong-min.com/_files/ugd/f42095_bb6f5448d4404162ad6e684ac1dd2261.pdf"),
    8:  ("paper_08.pdf", "https://www.jihong-min.com/_files/ugd/f42095_224b9814265f4f2bb139b428508c83a9.pdf"),
    7:  ("paper_07.pdf", "https://www.jihong-min.com/_files/ugd/f42095_488f222d52354c7d9eac4a0e0bfcd646.pdf"),
    6:  ("paper_06.pdf", "https://www.jihong-min.com/_files/ugd/f42095_9d0aa597a5f64e41883fcdff7d304820.pdf"),
    5:  ("paper_05.pdf", "https://www.jihong-min.com/_files/ugd/f42095_5913a11c27b44414aa11bf96c1d52627.pdf"),
    4:  ("paper_04.pdf", "https://www.jihong-min.com/_files/ugd/f42095_182c87144d4f4fbf81aee4120d8f095e.pdf"),
    3:  ("paper_03.pdf", "https://www.jihong-min.com/_files/ugd/f42095_dc83b437a37a4a0b870d06c8d289cafd.pdf"),
    2:  ("paper_02.pdf", "https://www.jihong-min.com/_files/ugd/f42095_13d68607335542c4b73a83f99770749b.pdf"),
    1:  ("paper_01.pdf", "https://www.jihong-min.com/_files/ugd/f42095_13d68607335542c4b73a83f99770749b.pdf"),
}

def main():
    os.makedirs(OUT, exist_ok=True)
    total = len(PDFS)
    done = 0
    failed = 0
    for num, (filename, url) in sorted(PDFS.items(), reverse=True):
        dest = os.path.join(OUT, filename)
        try:
            urllib.request.urlretrieve(url, dest)
            size_kb = os.path.getsize(dest) / 1024
            done += 1
            print(f"  [{done}/{total}] Paper {num}: {filename} ({size_kb:.0f} KB)")
        except Exception as e:
            failed += 1
            print(f"  FAILED: Paper {num}: {filename} - {e}")
    print(f"\nDone! {done} downloaded, {failed} failed.")

if __name__ == "__main__":
    main()
