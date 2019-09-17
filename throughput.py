import datetime

from models.base import UserTaskTree


def hour_string_to_float(hstr):
    intPart = int(hstr.split(":")[0])
    floatPart = int(hstr.split(":")[1]) / 60
    return intPart + floatPart


def get_hour_dispersion(total, ratio):
    data = []
    while total > 0:
        print(total)
        data.append(total)
        total = total - ratio
    data.append(0)
    return data


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

    daily_throughput = 4
    ptp_ratio = daily_throughput / trees.count()

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
                    "starts": tree.date,
                    "labels": ["mon","tus","w","th","f","s","d"],
                    "data": get_hour_dispersion(hour_string_to_float(root["_estimated_time"]), ptp_ratio),
                    "dataProg": [12.5, 9, 9, 8.5]
                })

    return daily_throughput, ptp_ratio, project_burndowns