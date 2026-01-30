"""
Topological Sort Demo in Python

This script demonstrates topological sorting using two methods:
1. Kahn's Algorithm (BFS-based approach)
2. DFS-based approach

Topological sorting is used for directed acyclic graphs (DAGs) where each node
comes before all nodes it points to.
"""

from collections import defaultdict, deque


class Graph:
    """A class to represent a directed graph and perform topological sorting."""

    def __init__(self, vertices):
        """
        Initialize the graph with a given number of vertices.
        
        Args:
            vertices (int): Number of vertices in the graph
        """
        self.vertices = vertices
        self.graph = defaultdict(list)
        self.in_degree = [0] * vertices

    def add_edge(self, u, v):
        """
        Add a directed edge from vertex u to vertex v.
        
        Args:
            u (int): Starting vertex
            v (int): Ending vertex
        """
        self.graph[u].append(v)
        self.in_degree[v] += 1

    def kahn_topological_sort(self):
        """
        Perform topological sort using Kahn's algorithm (BFS-based).
        
        Returns:
            list: A list representing the topological order of vertices,
                  or an empty list if the graph has a cycle
        """
        # Create a queue and enqueue all vertices with in-degree 0
        queue = deque()
        for i in range(self.vertices):
            if self.in_degree[i] == 0:
                queue.append(i)

        result = []
        
        # Process vertices in queue
        while queue:
            # Pop a vertex from queue
            u = queue.popleft()
            result.append(u)
            
            # Decrease in-degree of all adjacent vertices
            for v in self.graph[u]:
                self.in_degree[v] -= 1
                # If in-degree becomes zero, add it to queue
                if self.in_degree[v] == 0:
                    queue.append(v)
        
        # Check if topological sort includes all vertices
        # If not, there's a cycle in the graph
        if len(result) != self.vertices:
            return []  # Cycle detected
        
        return result

    def dfs_topological_sort(self):
        """
        Perform topological sort using DFS-based approach.
        
        Returns:
            list: A list representing the topological order of vertices,
                  or an empty list if the graph has a cycle
        """
        # 0: unvisited, 1: visiting (in recursion stack), 2: visited
        state = [0] * self.vertices
        result = []

        def dfs(vertex):
            """
            Helper function to perform DFS traversal.
            
            Args:
                vertex (int): Current vertex
                
            Returns:
                bool: True if no cycle detected, False otherwise
            """
            if state[vertex] == 1:  # Back edge detected (cycle)
                return False
            if state[vertex] == 2:  # Already processed
                return True
            
            # Mark as being visited (in recursion stack)
            state[vertex] = 1
            
            # Visit all neighbors
            for neighbor in self.graph[vertex]:
                if not dfs(neighbor):
                    return False
            
            # Mark as fully visited
            state[vertex] = 2
            # Add to result (at the beginning for correct order)
            result.insert(0, vertex)
            return True

        # Call DFS for each unvisited vertex
        for i in range(self.vertices):
            if state[i] == 0:
                if not dfs(i):
                    return []  # Cycle detected
        
        return result


def print_graph(g):
    """
    Print the adjacency list representation of the graph.
    
    Args:
        g (Graph): The graph to print
    """
    print("Graph representation:")
    for i in range(g.vertices):
        print(f"Vertex {i}: {' -> '.join(map(str, g.graph[i])) or '(no outgoing edges)'}")
    print()


def demo():
    """Demonstrate topological sorting with examples."""
    print("Topological Sort Demo")
    print("=" * 30)
    
    # Example 1: Simple DAG
    print("Example 1: Simple DAG")
    print("-" * 20)
    g1 = Graph(6)
    g1.add_edge(5, 2)
    g1.add_edge(5, 0)
    g1.add_edge(4, 0)
    g1.add_edge(4, 1)
    g1.add_edge(2, 3)
    g1.add_edge(3, 1)
    
    print_graph(g1)
    
    # Kahn's Algorithm
    result_kahn = g1.kahn_topological_sort()
    print(f"Topological Sort (Kahn's Algorithm): {result_kahn}")
    
    # Reset graph for DFS approach (since in-degrees were modified)
    g1_reset = Graph(6)
    for u in range(6):
        for v in g1.graph[u]:
            g1_reset.add_edge(u, v)
    
    # DFS-based approach
    result_dfs = g1_reset.dfs_topological_sort()
    print(f"Topological Sort (DFS-based): {result_dfs}")
    print()
    
    # Example 2: Graph with cycle
    print("Example 2: Graph with Cycle")
    print("-" * 20)
    g2 = Graph(3)
    g2.add_edge(0, 1)
    g2.add_edge(1, 2)
    g2.add_edge(2, 0)  # Creates a cycle
    
    print_graph(g2)
    
    result_cycle_kahn = g2.kahn_topological_sort()
    print(f"Topological Sort (Kahn's Algorithm): {result_cycle_kahn if result_cycle_kahn else 'Cycle detected!'}")
    
    # Reset graph for DFS approach
    g2_reset = Graph(3)
    for u in range(3):
        for v in g2.graph[u]:
            g2_reset.add_edge(u, v)
    
    result_cycle_dfs = g2_reset.dfs_topological_sort()
    print(f"Topological Sort (DFS-based): {result_cycle_dfs if result_cycle_dfs else 'Cycle detected!'}")
    print()
    
    # Example 3: Real-world scenario - Course prerequisites
    print("Example 3: Course Prerequisites")
    print("-" * 20)
    print("Courses: 0:Algebra, 1:Calculus, 2:Programming, 3:Data Structures, 4:Databases, 5:Algorithms")
    g3 = Graph(6)
    g3.add_edge(0, 1)  # Algebra -> Calculus
    g3.add_edge(0, 2)  # Algebra -> Programming
    g3.add_edge(2, 3)  # Programming -> Data Structures
    g3.add_edge(2, 4)  # Programming -> Databases
    g3.add_edge(3, 5)  # Data Structures -> Algorithms
    g3.add_edge(4, 5)  # Databases -> Algorithms
    
    print_graph(g3)
    
    result_courses_kahn = g3.kahn_topological_sort()
    course_names = ["Algebra", "Calculus", "Programming", "Data Structures", "Databases", "Algorithms"]
    course_order = [course_names[i] for i in result_courses_kahn]
    print(f"Course Order (Kahn's Algorithm): {' -> '.join(course_order)}")
    
    # Reset graph for DFS approach
    g3_reset = Graph(6)
    for u in range(6):
        for v in g3.graph[u]:
            g3_reset.add_edge(u, v)
    
    result_courses_dfs = g3_reset.dfs_topological_sort()
    course_order_dfs = [course_names[i] for i in result_courses_dfs]
    print(f"Course Order (DFS-based): {' -> '.join(course_order_dfs)}")


if __name__ == "__main__":
    demo()