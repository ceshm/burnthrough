
def sum_timestr(ts1, ts2):
    t1 = ts1.split(":")
    t2 = ts2.split(":")
    hsum = int(t1[0]) + int(t2[0])
    msum = int(t1[1]) + int(t2[1])
    return "{0:02d}:{1:02d}".format(hsum + msum//60, msum%60)


def traverse_json_tree_list(trees, actions=list()):
    all_results = []
    for tree in trees:
        print("")
        print("Traversing:",tree["label"])
        et, results = traverse_json_tree(tree, actions, path="/"+tree["label"])
        all_results = all_results + results
        print("")

    return all_results


def traverse_json_tree(tree, actions, level=1, path="/"):
    padding = "   " * level
    et = tree.get("estimated_time", None)

    results = []
    for action in actions:
        result = action(tree, path)
        if result:
            results.append({"key":action.__name__, "value":result})

    children_et = []
    for node in tree["children"]:
        print(padding,node["label"]," ",node.get("estimated_time", ""),path)
        r_et, r_results = traverse_json_tree(node, actions, level=level+1, path=path+"/"+node["label"])
        results = results + r_results
        children_et.append(r_et)

    children_et_sum = "00:00"
    if not et:
        for cet in children_et:
            children_et_sum = sum_timestr(children_et_sum, cet)
        et = children_et_sum
        print(padding,et)
        # Do the annotation
        tree["_estimated_time"] = et
    return et, results
