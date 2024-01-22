from pydantic import BaseModel, Field
import typing

__all__ = ["DirectedGraph"]




class Edge(BaseModel):
    
    source: int = Field(description="0-based index of token serving as relation's source")
    destination: int = Field(description="0-based index of token serving as relation's destination")
    relation: str = Field(description="label for relation")

class DirectedGraph(BaseModel):
    
    STANFORD_BASIC_DEPENDENCIES: typing.ClassVar[str] = "stanford-basic"
    STANFORD_COLLAPSED_DEPENDENCIES: typing.ClassVar[str] =  "stanford-collapsed"

    roots: list[int] = Field(description="Roots of the directed graph")
    edges: list[Edge] = Field(description="the directed edges that comprise the graph")

    """
    Storage class for directed graphs.


    Parameters
    ----------
    kind : str
        The name of the directed graph.

    deps : dict
        A dictionary of {edges: [{source, destination, relation}], roots: [int]}

    words : [str]
        A list of the word form of the tokens from the originating `Sentence`.

    Attributes
    ----------
    _words : [str]
        A list of the word form of the tokens from the originating `Sentence`.

    roots : [int]
        A list of indices for the syntactic dependency graph's roots.  Generally this is a single token index.

    edges: list[lum.clu.processors.doc.Edge]
        A list of `lum.clu.processors.doc.Edge`

    incoming : A dictionary of {int -> [int]} encoding the incoming edges for each node in the graph.

    outgoing : A dictionary of {int -> [int]} encoding the outgoing edges for each node in the graph.

    labeled : [str]
        A list of strings where each element in the list represents an edge encoded as source index, relation, and destination index ("source_relation_destination").

    unlabeled : [str]
        A list of strings where each element in the list represents an edge encoded as source index and destination index ("source_destination").

    graph : networkx.Graph
        A `networkx.graph` representation of the `DirectedGraph`.  Used by `shortest_path`

    Methods
    -------
    bag_of_labeled_dependencies_from_tokens(form)
        Produces a list of syntactic dependencies where each edge is labeled with its grammatical relation.
    bag_of_unlabeled_dependencies_from_tokens(form)
        Produces a list of syntactic dependencies where each edge is left unlabeled without its grammatical relation.
    """

    # def __init__(self, kind, deps, words):
    #     NLPDatum.__init__(self)
    #     self._words = [w.lower() for w in words]
    #     self.kind = kind
    #     self.roots = deps.get("roots", [])
    #     self.edges = [Edge(e["source"], e["destination"], e["relation"]) for e in deps["edges"]]
    #     self.incoming = self._build_incoming(self.edges)
    #     self.outgoing = self._build_outgoing(self.edges)
    #     self.labeled = self._build_labeled()
    #     self.unlabeled = self._build_unlabeled()
    #     self.directed_graph = DependencyUtils.build_networkx_graph(roots=self.roots, edges=self.edges, name=self.kind, reverse=False)
    #     self.undirected_graph = self.directed_graph.to_undirected()

    # def __unicode__(self):
    #     return self.edges

    # def __eq__(self, other):
    #     if isinstance(other, self.__class__):
    #         return self.to_JSON() == other.to_JSON()
    #     else:
    #         return False

    # def __ne__(self, other):
    #     return not self.__eq__(other)

    # def __hash__(self):
    #     return hash(self.to_JSON())

    # def shortest_paths(self, start, end):
    #     """
    #     Find the shortest paths in the syntactic depedency graph
    #     between the provided start and end nodes.

    #     Parameters
    #     ----------
    #     start : int or [int]
    #         A single token index or list of token indices serving as the start of the graph traversal.

    #     end : int or [int]
    #         A single token index or list of token indices serving as the end of the graph traversal.

    #     See Also
    #     --------
    #     `processors.paths.DependencyUtils.shortest_path`
    #     """
    #     paths = DependencyUtils.shortest_paths(self.undirected_graph, start, end)
    #     return None if not paths else [DependencyUtils.retrieve_edges(self, path) for path in paths]

    # def shortest_path(self, start, end, scoring_func=lambda path: -len(path)):
    #     """
    #     Find the shortest path in the syntactic depedency graph
    #     between the provided start and end nodes.

    #     Parameters
    #     ----------
    #     start : int or [int]
    #         A single token index or list of token indices serving as the start of the graph traversal.

    #     end : int or [int]
    #         A single token index or list of token indices serving as the end of the graph traversal.

    #     scoring_func : function
    #         A function that scores each path in a list of [(source index, directed relation, destination index)] paths.  Each path has the form [(source index, relation, destination index)].
    #         The path with the maximum score will be returned.

    #     See Also
    #     --------
    #     `processors.paths.DependencyUtils.shortest_path`
    #     """
    #     paths = self.shortest_paths(start, end)
    #     return None if not paths else max(paths, key=scoring_func)

    # def degree_centrality(self):
    #     """
    #     Compute the degree centrality for nodes.

    #     See Also
    #     --------
    #     https://networkx.github.io/documentation/development/reference/algorithms.centrality.html
    #     """
    #     return Counter(nx.degree_centrality(self.directed_graph))

    # def in_degree_centrality(self):
    #     """
    #     Compute the in-degree centrality for nodes.

    #     See Also
    #     --------
    #     https://networkx.github.io/documentation/development/reference/algorithms.centrality.html
    #     """
    #     return Counter(nx.in_degree_centrality(self.directed_graph))

    # def out_degree_centrality(self):
    #     """
    #     Compute the out-degree centrality for nodes.

    #     See Also
    #     --------
    #     https://networkx.github.io/documentation/development/reference/algorithms.centrality.html
    #     """
    #     return Counter(nx.out_degree_centrality(self.directed_graph))

    # def pagerank(self,
    #              alpha=0.85,
    #              personalization=None,
    #              max_iter=1000,
    #              tol=1e-06,
    #              nstart=None,
    #              weight='weight',
    #              dangling=None,
    #              use_directed=True,
    #              reverse=True):
    #     """
    #     Measures node activity in a `networkx.Graph` using a thin wrapper around `networkx` implementation of pagerank algorithm (see `networkx.algorithms.link_analysis.pagerank`).  Use with `lum.clu.processors.doc.DirectedGraph.graph`.
    #     Note that by default, the directed graph is reversed in order to highlight predicate-argument nodes (refer to pagerank algorithm to understand why).

    #     See Also
    #     --------
    #     `processors.paths.DependencyUtils.pagerank`
    #     Method parameters correspond to those of [`networkx.algorithms.link_analysis.pagerank`](https://networkx.github.io/documentation/development/reference/generated/networkx.algorithms.link_analysis.pagerank_alg.pagerank.html#networkx.algorithms.link_analysis.pagerank_alg.pagerank)
    #     """
    #     # check whether or not to reverse directed graph
    #     dg = self.directed_graph if not reverse else DependencyUtils.build_networkx_graph(roots=self.roots, edges=self.edges, name=self.kind, reverse=True)
    #     # determine graph to use
    #     graph = dg if use_directed else self.undirected_graph
    #     return DependencyUtils.pagerank(graph, alpha=alpha, personalization=personalization, max_iter=max_iter, tol=tol, nstart=nstart, weight=weight, dangling=dangling)

    # def _build_incoming(self, edges):
    #     dep_dict = defaultdict(list)
    #     for edge in edges:
    #         dep_dict[edge.destination].append((edge.source, edge.relation))
    #     return dep_dict

    # def _build_outgoing(self, edges):
    #     dep_dict = defaultdict(list)
    #     for edge in edges:
    #         dep_dict[edge.source].append((edge.destination, edge.relation))
    #     return dep_dict

    # def _build_labeled(self):
    #     labeled = []
    #     for out in self.outgoing:
    #         for (dest, rel) in self.outgoing[out]:
    #             labeled.append("{}_{}_{}".format(self._words[out], rel.upper(), self._words[dest]))
    #     return labeled

    # def _build_unlabeled(self):
    #     unlabeled = []
    #     for out in self.outgoing:
    #         for (dest, _) in self.outgoing[out]:
    #             unlabeled.append("{}_{}".format(self._words[out], self._words[dest]))
    #     return unlabeled

    # def _graph_to_JSON_dict(self):
    #     dg_dict = dict()
    #     dg_dict["edges"] = [e.to_JSON_dict() for e in self.edges]
    #     dg_dict["roots"] = self.roots
    #     return dg_dict

    # def to_JSON_dict(self):
    #     return {self.kind:self._graph_to_JSON_dict()}