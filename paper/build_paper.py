"""Typeset the complete canonical comment; excluded from computational snapshot."""
from pathlib import Path
import os,re,shutil,subprocess

root=Path(__file__).resolve().parents[1]
paper=root/'paper';latex=paper/'latex'
text=(paper/'manuscript.md').read_text(encoding='utf-8')
assert re.findall(r'^## (\d+)\.',text,re.M)==list(map(str,range(1,7)))
assert text.count('## Abstract\n')==text.count('## References\n')==1
assert not re.search(r'[\x00-\x08\x0b\x0c\x0e-\x1f]',text)
assert (latex/'main.tex').exists()
pandoc=os.environ.get('PANDOC') or shutil.which('pandoc')
if not pandoc:raise RuntimeError('Set PANDOC or install Pandoc.')
subprocess.run([pandoc,str(paper/'manuscript.md'),'-f',
    'markdown+tex_math_dollars+raw_tex+autolink_bare_uris-implicit_figures',
    '-t','latex','--no-highlight','-o',str(latex/'body.tex')],check=True)
body=(latex/'body.tex').read_text(encoding='utf-8').replace('../figures/','images/')
title=text.splitlines()[0].removeprefix('# ')
body=body.replace(r'\section{',r'\section['+title+r']{\raggedright ',1)
body=re.sub(r'\\texttt\{([^{}\n ]+)\}',lambda m:r'\nolinkurl{'+m[1].replace(r'\_','_')+'}',body)
assert r'\begin{longtable}' not in body
def keep_figure(m):
    return r'\begin{minipage}{\linewidth}'+'\n'+m[0]+'\n'+r'\end{minipage}'
body,n=re.subn(r'\\pandocbounded\{\\includegraphics\[[^\n]+\}\}\n\nFigure [12]\. .*?(?=\n\n)',keep_figure,body,flags=re.S)
assert n==2,n
refs=r'\subsection{References}\label{references}'
assert body.count(refs)==1
body=body.replace(refs,r'\clearpage'+'\n'+r'\begingroup\small\raggedright'+'\n'+refs)+'\n'+r'\endgroup'+'\n'
(latex/'body.tex').write_text(body,encoding='utf-8',newline='\n')
(latex/'images').mkdir(exist_ok=True)
for image in (root/'figures').glob('*.png'):shutil.copy2(image,latex/'images'/image.name)
print(dict(body_words_regex=len(re.findall(r'\b[\w-]+\b',text.split('## References')[0])),figures=n,tables=0))
