PREFIX : <http://www.semanticweb.org/avt/ontologies/2024/5/untitled-ontology-149/>

SELECT (COUNT(?language) as ?languageCount)
WHERE {
  :Eduardo :person_speaks ?language .
}

SELECT (COUNT(?individual) AS ?individualCount)
WHERE {
  ?individual a owl:NamedIndividual .
}

SELECT (COUNT(?individual) AS ?individualCount)
WHERE {
  ?individual a :Person .
}

SELECT ?name
WHERE {
  ?individual a :Person .
  ?individual :person_is_learning "Alemao".
  ?person :person_name ?name.
}

SELECT *
WHERE {
  ?ind a :Person .
  ?ind :person_name "Hanna".
}