PREFIX : <http://www.semanticweb.org/ontologies/2024/books_recurso/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

#Quantas livros estão presentes na ontologia?
SELECT (COUNT(?book) AS ?bookCount)
WHERE {
  ?book a :Book .
}
#-------------


#Quais os títulos dos livros em que um dos autores tem apelido "Austen"? (lista de títulos ordenada alfabeticamente)
SELECT ?bookTitle
WHERE {
  ?book a :Book ;
        :book_author ?author .
  FILTER(REGEX(?author, "Austen$", "i"))
  OPTIONAL {
    ?book :book_title ?bookTitle .
  }
}
ORDER BY ?bookTitle
#-------------


#Qual a distribuição de livros por autor? (lista de autores sem repetições e ordenada
alfabeticamente em que a cada autor está associado o número de livros escritos por esse
autor);
SELECT ?author (COUNT(?book) as ?numBooks)
WHERE {
  ?book a :Book .
  ?book :book_author ?author .
}
GROUP BY ?author
ORDER BY ?author
#-------------




#Qual a distribuição de livros por género? (lista de géneros sem repetições e ordenada
alfabeticamente em que a cada género está associado o número de livros pertencente a esse
género)
SELECT ?genre (COUNT(?book) AS ?numBooks)
WHERE {
  ?book :book_has_genre ?genre .
}
GROUP BY ?genre
ORDER BY ASC(?genre)
#-------------



#Produz uma lista de pares, nome do personagem e a lista de livros onde esse personagem
aparece, ordenada alfabeticamente por nome de personagem;
SELECT ?character (GROUP_CONCAT(?bookTitle; separator=", ") AS ?books)
WHERE {
  ?book :book_has_char ?character .
  ?book :book_title ?bookTitle .
}
GROUP BY ?character
ORDER BY ASC(?character)
#-------------


#Quais os títulos dos livros pertencentes ao género "Adventure"? (lista ordenada
alfabeticamente de títulos)
SELECT ?title
WHERE {
  ?book :book_has_genre :Adventure .
  ?book :book_title ?title .
}
ORDER BY ASC(?title)
#-------------


#Cria uma query CONSTRUCT que associe os co-autores (autores do mesmo livro) pela
relação hasCoAuthor. No fim, acrescenta estes triplos à ontologia;
CONSTRUCT {
  ?book :book_has_coauthor ?coAuthor .
}
WHERE {
  ?book :book_author ?author .
  ?book :book_author ?coAuthor .
  FILTER (?author != ?coAuthor)
}
