from sklearn.neighbors import KDTree

def build_tree(vec_dict):
    vec_list = []
    index_to_id = dict()
    for i, item in enumerate(vec_dict.items()):
        unique_id, vec = item
        vec_list.append(vec[0])
        index_to_id[i] = unique_id
    return KDTree(vec_list), index_to_id

# k = num neighbors
def query(vector, k, tree, index_to_id):
    try:
        _, indices = tree.query(vector, k)
    except ValueError:
        _, indices = tree.query(vector[0], k)
    ids = [index_to_id[index] for index in indices[0]]
    return ids
