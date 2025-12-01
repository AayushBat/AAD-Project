from collections import deque

def push_relabel(graph, s, t):
    n = graph.n
    cap = [dict() for _ in range(n)]
    for u in range(n):
        for v, c in graph.adj[u].items():
            if c <= 0:
                continue
            cap[u][v] = cap[u].get(v, 0) + c
            cap[v].setdefault(u, 0)

    height = [0] * n
    height[s] = n
    excess = [0] * n
    Q = deque()

    def push(u, v):
        send = min(excess[u], cap[u][v])
        if send <= 0:
            return
        cap[u][v] -= send
        cap[v][u] = cap[v].get(u, 0) + send
        excess[u] -= send
        was_zero = (excess[v] == 0)
        excess[v] += send
        if v != s and v != t and was_zero and excess[v] > 0:
            Q.append(v)

    def relabel(u):
        min_h = None
        for v, c in cap[u].items():
            if c > 0:
                if min_h is None or height[v] < min_h:
                    min_h = height[v]
        if min_h is not None:
            height[u] = min_h + 1

    for v, c in list(cap[s].items()):
        if c <= 0:
            continue
        send = c
        cap[s][v] -= send
        cap[v][s] = cap[v].get(s, 0) + send
        excess[v] += send
        excess[s] -= send
        if v != s and v != t and excess[v] > 0:
            Q.append(v)

    while Q:
        u = Q[0]
        pushed = False

        for v, c in list(cap[u].items()):
            if excess[u] == 0:
                break
            if c > 0 and height[u] == height[v] + 1:
                push(u, v)
                pushed = True

        if excess[u] > 0 and not pushed:
            relabel(u)

        if excess[u] == 0:
            Q.popleft()


    return excess[t]


def push_relabel_min_cut(graph, s, t):
    """
    Run Push-Relabel to compute max flow and return (flow, min_cut_edges)
    using the final residual capacities.
    """
    n = graph.n
    # Construct residual caps (dict-of-dicts) similar to push_relabel's internal cap
    cap = [dict() for _ in range(n)]
    for u in range(n):
        for v, c in graph.adj[u].items():
            if c <= 0:
                continue
            cap[u][v] = cap[u].get(v, 0) + c
            cap[v].setdefault(u, 0)

    height = [0] * n
    height[s] = n
    excess = [0] * n
    Q = deque()

    def push(u, v):
        send = min(excess[u], cap[u][v])
        if send <= 0:
            return
        cap[u][v] -= send
        cap[v][u] = cap[v].get(u, 0) + send
        excess[u] -= send
        was_zero = (excess[v] == 0)
        excess[v] += send
        if v != s and v != t and was_zero and excess[v] > 0:
            Q.append(v)

    def relabel(u):
        min_h = None
        for v, c in cap[u].items():
            if c > 0:
                if min_h is None or height[v] < min_h:
                    min_h = height[v]
        if min_h is not None:
            height[u] = min_h + 1

    for v, c in list(cap[s].items()):
        if c <= 0:
            continue
        send = c
        cap[s][v] -= send
        cap[v][s] = cap[v].get(s, 0) + send
        excess[v] += send
        excess[s] -= send
        if v != s and v != t and excess[v] > 0:
            Q.append(v)

    while Q:
        u = Q[0]
        pushed = False

        for v, c in list(cap[u].items()):
            if excess[u] == 0:
                break
            if c > 0 and height[u] == height[v] + 1:
                push(u, v)
                pushed = True

        if excess[u] > 0 and not pushed:
            relabel(u)

        if excess[u] == 0:
            Q.popleft()

    flow = excess[t]

    residual = cap 
    from graphy import compute_min_cut_from_residual
    cut = compute_min_cut_from_residual(graph, residual, s)
    return flow, cut
