

def sum_timestr(ts1, ts2):
    t1 = ts1.split(":")
    t2 = ts2.split(":")
    hsum = int(t1[0]) + int(t2[0])
    msum = int(t1[1]) + int(t2[1])
    return "{0:02d}:{1:02d}".format(hsum + msum//60, msum%60)


def traverse_json_tree_list(trees):

    for tree in trees:
        print("")
        print("Traversing:",tree["label"])
        traverse_json_tree(tree)
        print("")


def traverse_json_tree(tree, level=1):
    padding = "   " * level
    et = tree.get("estimated_time", None)

    children_et = []
    for node in tree["children"]:
        print(padding,node["label"]," ",node.get("estimated_time", ""))
        r_et = traverse_json_tree(node, level=level+1)
        children_et.append(r_et)

    children_et_sum = "00:00"
    if not et:
        for cet in children_et:
            children_et_sum = sum_timestr(children_et_sum, cet)
        et = children_et_sum
        print(padding,et)
        # Do the annotation
        tree["_estimated_time"] = et
    return et

#def basic_travese(tree):
#   print(tree)

