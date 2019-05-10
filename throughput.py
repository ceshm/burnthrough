import datetime

from models.base import UserTaskTree


def hour_string_to_float(hstr):
    intPart = int(hstr.split(":")[0])
    floatPart = int(hstr.split(":")[1])

    return intPart + floatPart


def get_burndown_data(user_id):
    print("getting burndown data")
    today = datetime.datetime.now()
    date_limit = today - datetime.timedelta(days=90)

    # Filter trees with time estimation && from the last 90 days?
    trees = UserTaskTree.filter(
        UserTaskTree.user == user_id,
        UserTaskTree.nodes[0]["_estimated_time"]!=None, # TODO make this more complex (search for other indexes)
        UserTaskTree.nodes[0]["_estimated_time"]!="00:00",
        UserTaskTree.date <= today,
        UserTaskTree.date > date_limit
    )

    # Arreglo de datapoints por projecto
    project_burndowns = []
    for tree in trees:
        print(tree.date)
        for root in tree.nodes:
            if root["_estimated_time"]!="00:00":
                print("  "+root["label"]+":", root["_estimated_time"])
                project_burndowns.append({
                    "name": root["label"],
                    "total": hour_string_to_float(root["_estimated_time"]),
                    "starts": tree.date
                })

    return project_burndowns