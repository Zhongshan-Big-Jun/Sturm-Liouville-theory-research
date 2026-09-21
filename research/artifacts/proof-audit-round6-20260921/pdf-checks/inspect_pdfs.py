from pathlib import Path
import pymupdf as fitz, json,hashlib,re,sys
R=Path('/mnt/f/LaTeX/BVE research');O=Path('/mnt/f/tools/math-audit-round6-20260921/pdf-inspection');O.mkdir(exist_ok=True)
Result=[]
for Name in sys.argv[1:]:
	P=R/'docs'/(Name+'.pdf');Doc=fitz.open(P);D=O/Name;D.mkdir(exist_ok=True);Pages=[]
	for I,Page in enumerate(Doc):
		Text=Page.get_text();assert Text.strip(),(Name,I,'empty page')
		assert '\ufffd' not in Text,(Name,I,'replacement glyph')
		Bad=[]
		for B in Page.get_text('dict')['blocks']:
			for Line in B.get('lines',[]):
				for Span in Line['spans']:
					Rect=fitz.Rect(Span['bbox'])
					if not (Page.rect+(-2,-2,2,2)).contains(Rect):Bad.append(Span)
		Pages.append({'page':I+1,'characters':len(Text),'outside_page_spans':Bad})
		(D/('page-'+str(I+1)+'.txt')).write_text(Text)
	for Start in range(0,len(Doc),4):
		Sheet=fitz.open();Page=Sheet.new_page(width=1200,height=1760)
		for J in range(min(4,len(Doc)-Start)):
			Col,Row=J%2,J//2;Box=fitz.Rect(Col*600,Row*880+22,(Col+1)*600,(Row+1)*880)
			Page.insert_text((Col*600+12,Row*880+16),Name+' page '+str(Start+J+1),fontsize=11)
			Page.show_pdf_page(Box,Doc,Start+J)
		Page.get_pixmap(matrix=fitz.Matrix(1,1)).save(D/('sheet-'+str(Start//4+1)+'.png'))
	Result.append({'name':Name,'pdf_sha256':hashlib.sha256(P.read_bytes()).hexdigest(),'pages':Pages})
(O/'structural-check.json').write_text(json.dumps(Result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps([{'name':D['name'],'pages':len(D['pages']),'out_of_page':sum(len(P['outside_page_spans']) for P in D['pages'])} for D in Result]))
