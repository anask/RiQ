PREFIX ub: <file:///home/vsfgd/datasets/lubm/univ-bench.owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT ?x WHERE {
	GRAPH ?g {
		?x rdf:type ub:GraduateStudent .
	}
}
