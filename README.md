# Search Engine on 30K Wiki documents

The content of the repository is composed in this way:

README.md: a Markdown file that explains the content of your repository. 
collector.py: a python file that contains the line of code needed to collect your data from the html page (from which you get the urls) and Wikipedia.

collector_utils.py: a python file that stores the function used in collector.py.

parser.py: a python file that contains the line of code needed to parse the entire collection of html pages and save those in tsv files.

parser_utils.py: a python file that gathers the function used in parser.py.

index.py: a python file that once executed generate the indexes of the Search engines.

index_utils.py: a python file that contains the functions used for creating indexes.

main.ipynb: a Jupyter notebook explaines the strategies you adopted solving the homework and the Bonus point (visualization task). 

main.py: a python file that once executed build up the search engine. 

exercise_4.py: python file that contains the implementation of the algorithm that solves problem 4.

exercise_4(2).py: python file that contains the implementation of the algorithm that solves problem 4 in another way
utils.py: a python file that gather functions of cleaning text

