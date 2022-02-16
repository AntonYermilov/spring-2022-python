FROM python:3.9

RUN apt-get update
RUN apt-get install -y graphviz texlive-latex-base

WORKDIR /
ADD src/gentex.py /

ADD requirements.txt /
RUN python3.9 -m pip install -r requirements.txt
RUN python3.9 -m pip install -i https://test.pypi.org/simple/ simple-ast-drawer==1.0.2

CMD python3.9 gentex.py && pdflatex -output-directory artifacts artifacts/main.tex && rm artifacts/main.log artifacts/main.aux