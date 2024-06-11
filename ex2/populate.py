from rdflib import Namespace, URIRef, Graph, Literal
from rdflib.namespace import RDF, OWL, XSD
import json
import ast
import shutil

# Create a translation table for removing LS and PS characters
unusual_characters = {
    ord('\u2028'): None,  # LS (Line Separator)
    ord('\u2029'): None,  # PS (Paragraph Separator)
}

def clean_string(s):
    return s.translate(unusual_characters)

# Initialize the graph and namespace
g = Graph()
g.parse("./ex2/books_base.ttl")
ns = Namespace("http://www.semanticweb.org/ontologies/2024/books_recurso/")

# File path to the JSON data
file_path = 'dataset.json'

# Read and parse the JSON file
try:
    with open(file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()
    if file_content.strip():
        data = json.loads(file_content)
    else:
        print("The JSON file is empty")
except FileNotFoundError:
    print(f"File not found: {file_path}")
    data = []
except json.JSONDecodeError as e:
    print(f"JSON decoding error: {e}")
    data = []
except Exception as e:
    print(f"An error occurred: {e}")
    data = []

# Copy the base TTL file to a new TTL file
source_file = './ex2/books_base.ttl'
destination_file = './ex2/books.ttl'
shutil.copyfile(source_file, destination_file)

# List of attributes to process
lst_ = [
    "bookId", "title", "series", "author", "rating", "description",
    "language", "isbn", "genres", "characters", "bookFormat", "edition",
    "pages", "publisher", "publishDate", "firstPublishDate", "awards",
    "numRatings", "ratingsByStars", "likedPercent", "setting", "coverImg",
    "bbeScore", "bbeVotes", "price"
]

char_set = set()
genre_set = set()

# Process each book entry
for book in data:
    id = book["bookId"]
    bookUri = URIRef(f'{ns}{clean_string(id).replace(" ","_").replace("#", "").replace(".", "")}')
    g.add((bookUri, RDF.type, OWL.NamedIndividual))
    g.add((bookUri, RDF.type, ns.Book))

    for attr in lst_:
        value_of_attr = book[attr]
        value_of_attr = clean_string(value_of_attr) if isinstance(value_of_attr, str) else value_of_attr
        print(value_of_attr)

        if attr in ["genres", "characters", "awards", "ratingsByStars", "setting"]:
            try:
                actual_list = ast.literal_eval(value_of_attr)
                if attr == "characters":
                    for c in actual_list:
                        
                        c_ID = c
                        for a in ['/', '#', '"', '<', '>', '\\', " ", "[", "]"]:
                            c_ID = c_ID.replace(a, "_")
                        
                        c_ID_ = URIRef(f'{ns}{c_ID}')

                        if c not in char_set:
                            char_set.add(c)
                            g.add((c_ID_, RDF.type, OWL.NamedIndividual))
                            g.add((c_ID_, RDF.type, ns.Chars))
                            g.add((c_ID_, ns.char_id, Literal(c_ID)))

                        g.add((bookUri, ns.book_has_char, c_ID_))

                elif attr == "genres":
                    for c in actual_list:

                        c_ID = c
                        for a in ['/', '#', '"', '<', '>', '\\', " ", "[", "]"]:
                            c_ID = c_ID.replace(a, "_")

                        c_ID_ = URIRef(f'{ns}{c_ID}')

                        if c not in genre_set:
                            genre_set.add(c)
                            g.add((c_ID_, RDF.type, OWL.NamedIndividual))
                            g.add((c_ID_, RDF.type, ns.Genre))
                            g.add((c_ID_, ns.genre_id, Literal(c_ID)))

                        g.add((bookUri, ns.book_has_genre, c_ID_))

            except (ValueError, SyntaxError):
                print(f"Error parsing list for {attr}: {value_of_attr}")
        else:
            str_attr = "book_" + attr
            g.add((bookUri, ns[str_attr], Literal(value_of_attr)))


g.serialize(format="ttl", destination="./ex2/books.ttl")
