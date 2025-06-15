from collections import defaultdict
from itertools import combinations

class TrieNode:
    def __init__(self):
        self.children = {}
        self.ids = set()

def insert(trie, string, string_id):
    node = trie
    for ch in string:
        if ch not in node.children:
            node.children[ch] = TrieNode()
        node = node.children[ch]
        node.ids.add(string_id)

def dfs(node, prefix, result):
    if len(node.ids) >= 2:
        for i, j in combinations(sorted(node.ids), 2):
            result[(i, j)] = prefix  # κάθε ζεύγος έχει ως max κοινό πρόθεμα το prefix

    for ch, child in node.children.items():
        dfs(child, prefix + ch, result)

def longest_common_prefixes(strings):
    trie = TrieNode()
    for i, s in enumerate(strings):
        insert(trie, s, i)
    
    result = {}
    dfs(trie, "", result)
    return result
	
#e.g.
#strings = ["banana", "bandana", "band", "ban", "bang"]
#lcp_pairs = longest_common_prefixes(strings)

#for pair in sorted(lcp_pairs):
#    print(f"{pair}: '{lcp_pairs[pair]}'")