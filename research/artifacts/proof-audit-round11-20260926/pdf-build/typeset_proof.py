"""Deterministic Markdown presentation, preserving every TeX math span."""
from pathlib import Path
import re,json,hashlib,sys
from markdown_it import MarkdownIt
O=Path(__file__).resolve().parent
Source=Path(sys.argv[1]);Target=Path(sys.argv[2])
Raw=Source.read_text();Math=[]
def protect(Match):
	Math.append(Match.group(0));return 'ZXQMATH'+str(len(Math)-1)+'TOKEN'
Text=re.sub(r'\\\[.*?\\\]',lambda M:'\n\n'+protect(M)+'\n\n',Raw,flags=re.S)
Text=re.sub(r'\\\(.*?\\\)',protect,Text,flags=re.S)
Text=re.sub(r'(?<!\\)\$(?!\$)[^\n$]+?(?<!\\)\$',protect,Text)
Layout=[]
for I,Span in enumerate(Math):
	if r'\tag{1.1}' in Span:
		Before=Span
		Span=Span.replace('\\[\n','\\[\n\\begin{gathered}\n',1).replace(' \\qquad\n \\mathcal Bf=', ' \\\\\n \\mathcal Bf=',1).replace(' \\tag{1.1}', '\\end{gathered}\n \\tag{1.1}',1)
		Layout.append({'tag':'1.1','before_sha256':hashlib.sha256(Before.encode()).hexdigest(),'after_sha256':hashlib.sha256(Span.encode()).hexdigest(),'change':'two display rows, mathematical tokens unchanged except spacing commands'})
		Math[I]=Span
	elif r'\tag{5.8}' in Span:
		Before=Span
		Span=Span.replace('\\[\n','\\[\n\\begin{gathered}\n',1).replace(' \\quad\n M_o(L)=',' \\\\\n M_o(L)=',1).replace(' \\tag{5.8}', '\\end{gathered}\n \\tag{5.8}',1)
		Layout.append({'tag':'5.8','before_sha256':hashlib.sha256(Before.encode()).hexdigest(),'after_sha256':hashlib.sha256(Span.encode()).hexdigest(),'change':'two display rows, mathematical tokens unchanged except spacing commands'})
		Math[I]=Span
Tokens=MarkdownIt('commonmark').enable('table').parse(Text)
Escapes={'\\':r'\textbackslash{}','&':r'\&','%':r'\%','$':r'\$','#':r'\#','_':r'\_','{':r'\{','}':r'\}','~':r'\textasciitilde{}','^':r'\textasciicircum{}','≤':r'\(\le\)','≥':r'\(\ge\)','→':r'\(\to\)','∞':r'\(\infty\)','∈':r'\(\in\)','∉':r'\(\notin\)'}
def escape(S):
	S=''.join(Escapes.get(C,C) for C in S)
	return re.sub(r'ZXQMATH(\d+)TOKEN',lambda M:Math[int(M.group(1))],S)
def inline(Children):
	Parts=[]
	for T in Children or []:
		if T.type=='text':Parts.append(escape(T.content))
		elif T.type=='code_inline':Parts.append(r'\texttt{'+escape(T.content)+'}')
		elif T.type=='strong_open':Parts.append(r'\textbf{')
		elif T.type=='em_open':Parts.append(r'\emph{')
		elif T.type in ('strong_close','em_close'):Parts.append('}')
		elif T.type in ('softbreak','hardbreak'):Parts.append('\n' if T.type=='softbreak' else r'\\'+'\n')
		elif T.type=='link_open':Parts.append(r'\href{'+T.attrGet('href').replace('%',r'\%').replace('#',r'\#')+'}{')
		elif T.type=='link_close':Parts.append('}')
		else:raise ValueError('Unsupported inline token '+T.type)
	return ''.join(Parts)
Parts=[];Cell=0;InTable=False
for K,T in enumerate(Tokens):
	if T.type=='inline':Parts.append(inline(T.children))
	elif T.type=='paragraph_open':Parts.append('\n')
	elif T.type=='paragraph_close':Parts.append('\n\n')
	elif T.type=='heading_open':
		Cmd={'h1':'section','h2':'section','h3':'subsection','h4':'subsubsection'}[T.tag]
		Parts.append('\n\\'+Cmd+'*{')
	elif T.type=='heading_close':Parts.append('}\n')
	elif T.type=='bullet_list_open':Parts.append('\n\\begin{itemize}\n')
	elif T.type=='bullet_list_close':Parts.append('\n\\end{itemize}\n')
	elif T.type=='ordered_list_open':Parts.append('\n\\begin{enumerate}\n')
	elif T.type=='ordered_list_close':Parts.append('\n\\end{enumerate}\n')
	elif T.type=='list_item_open':Parts.append('\n\\item ')
	elif T.type=='list_item_close':Parts.append('\n')
	elif T.type=='blockquote_open':Parts.append('\n\\begin{quote}\n')
	elif T.type=='blockquote_close':Parts.append('\n\\end{quote}\n')
	elif T.type=='hr':Parts.append('\n\\medskip\\hrule\\medskip\n')
	elif T.type in ('fence','code_block'):
		Parts.append('\n{\\small\\ttfamily\\raggedright\n'+r'\par '.join(escape(Line) for Line in T.content.splitlines())+'\\par}\n')
	elif T.type=='table_open':
		Row=[]
		for U in Tokens[K+1:]:
			if U.type=='tr_close':break
			if U.type=='th_open':Row.append(U)
		N=len(Row);Width=.90/N
		Parts.append('\n\\begin{longtable}{@{}'+''.join('>{\\raggedright\\arraybackslash}p{%.4f\\linewidth}'%Width for _ in Row)+'@{}}\n\\toprule\n');InTable=True
	elif T.type=='table_close':Parts.append('\n\\bottomrule\n\\end{longtable}\n');InTable=False
	elif T.type=='tr_open':Cell=0
	elif T.type in ('th_open','td_open'):
		if Cell:Parts.append(' & ')
		Cell+=1
	elif T.type=='tr_close':Parts.append(' \\\\\n')
	elif T.type=='thead_close':Parts.append('\\midrule\n')
	elif T.type in ('thead_open','tbody_open','tbody_close','th_close','td_close'):pass
	else:raise ValueError('Unsupported block token '+T.type)
Body=''.join(Parts)
if 'ZXQMATH' in Body:raise ValueError('Unrestored math token')
Header=r'''% !TEX program = xelatex
% Generated from the bound Markdown author proof; mathematics is not changed.
\documentclass[UTF8,fontset=fandol,11pt,a4paper]{ctexart}
\usepackage{amsmath,amssymb}
\usepackage[margin=2.25cm]{geometry}
\usepackage{longtable,booktabs,array,enumitem}
\usepackage[hyphens]{url}
\usepackage[hidelinks,unicode]{hyperref}
\setlist{nosep,leftmargin=2em}
\allowdisplaybreaks
\setlength{\emergencystretch}{3em}
\begin{document}
'''
Output=Header+Body+'\n\\end{document}\n'
Target.parent.mkdir(parents=True,exist_ok=True);Target.write_text(Output)
Record=dict(source=str(Source),source_sha256=hashlib.sha256(Source.read_bytes()).hexdigest(),target=str(Target),target_sha256=hashlib.sha256(Target.read_bytes()).hexdigest(),math_spans=len(Math),layout_changes=Layout,method='MarkdownIt block structure, protected TeX spans with listed display line breaks; derived presentation, no proof changes')
Target.with_suffix('.typesetting.json').write_text(json.dumps(Record,indent=2)+'\n')
print(json.dumps(Record),flush=True)
