from collections import defaultdict
import matplotlib.pyplot as plt
from algorithms.test.similarity_type import SimilarityType

title = {
    SimilarityType.jaccard: "Jaccard",
    SimilarityType.cosine_binary: "Cosine for binary matrix",
    SimilarityType.cosine: "Cosine",
    SimilarityType.cosine_normalized: "Cosine for normalized data"
}


def add_data(key_to_files, end_index=15):
    n = defaultdict(list)
    elapsed_time = defaultdict(list)
    ratio = defaultdict(list)
    mae = defaultdict(list)
    rmse = defaultdict(list)

    for (key, file) in key_to_files.items():
        with open(file) as f:
            lines = f.readlines()
            for line in lines[:end_index]:
                line = line.strip().split(" ")
                n[key].append(int(line[0]))
                elapsed_time[key].append(float(line[1]))
                ratio[key].append(float(line[2]) * 100)
                mae[key].append(float(line[3]))
                rmse[key].append(float(line[4]))

    return n, elapsed_time, ratio, mae, rmse


def active_users_vs_all_users():
    key_to_files = {"active users": "filtered_results/AlgorithmType.item_based/cosine_False",
                    "all users": "results/AlgorithmType.item_based/cosine_False"}
    n, elapsed_time, ratio, mae, rmse = add_data(key_to_files)

    plt.figure()
    plt.title("MAE for: cosine version, hotel based, arithmetic average")
    plt.xlabel("n")
    plt.ylabel("MAE")
    for key in key_to_files:
        plt.plot(n[key], mae[key], label=key)
    plt.legend(title="Dataset", loc="upper left")
    plt.grid(True)
    plt.savefig(f"graphs/mae/mae-active-users-vs-all-users.png")
    plt.close()

    plt.figure()
    plt.title("RMSE for: cosine version, hotel based, arithmetic average")
    plt.xlabel("n")
    plt.ylabel("RMSE")
    for key in key_to_files:
        plt.plot(n[key], rmse[key], label=key)
    plt.legend(title="Dataset", loc="upper left")
    plt.grid(True)
    plt.savefig(f"graphs/rmse/rmse-active-users-vs-all-users.png")
    plt.close()

    plt.figure()
    plt.title("RATIO for: cosine version, hotel based, arithmetic average")
    plt.xlabel("n")
    plt.ylabel("RATIO [%]")
    for key in key_to_files:
        plt.plot(n[key], ratio[key], label=key)
    plt.legend(title="Dataset", loc="upper left")
    plt.grid(True)
    plt.savefig(f"graphs/ratio/ratio-active-users-vs-all-users.png")
    plt.close()


def positive_ratings_analysis():
    key_to_files = {"standard": "results/AlgorithmType.item_based/cosine_True"}
    for positive_threshold in [3, 4, 5]:
        key_to_files[
            f"binary p={positive_threshold}"] = f"results/AlgorithmType.item_based/cosine_binary_True_{positive_threshold}"

    n, elapsed_time, ratio, mae, rmse = add_data(key_to_files)
    plt.figure()
    plt.title("MAE for: cosine version, hotel based, weighted average")
    plt.xlabel("n")
    plt.ylabel("MAE")
    for key in key_to_files:
        plt.plot(n[key], mae[key], label=key)
    plt.legend(title="Utility matrix", loc="lower right")
    plt.grid(True)
    plt.savefig(f"graphs/mae/mae-positive-ratings-analysis.png")
    plt.close()

    plt.figure()
    plt.title("RMSE for: cosine version, hotel based, weighted average")
    plt.xlabel("n")
    plt.ylabel("RMSE")
    for key in key_to_files:
        plt.plot(n[key], rmse[key], label=key)
    plt.legend(title="Utility matrix", loc="lower right")
    plt.grid(True)
    plt.savefig(f"graphs/rmse/rmse-positive-ratings-analysis.png")
    plt.close()

    plt.figure()
    plt.title("RATIO for: cosine version, hotel based, weighted average")
    plt.xlabel("n")
    plt.ylabel("RATIO [%]")
    for key in key_to_files:
        plt.plot(n[key], ratio[key], label=key)
    plt.legend(title="Utility matrix", loc="lower right")
    plt.grid(True)
    plt.savefig(f"graphs/ratio/ratio-positive-ratings-analysis.png")
    plt.close()


def item_vs_user_based():
    key_to_files = {"hotel": "results/AlgorithmType.item_based/jaccard_False_3",
                    "user": "results/AlgorithmType.user_based/jaccard_False_3"}
    n, elapsed_time, ratio, mae, rmse = add_data(key_to_files, 20)
    for key in key_to_files:
        plt.figure()
        plt.title(f"MAE for: jaccard version p = 3, {key} based, arithmetic average")
        plt.xlabel("n")
        plt.ylabel("MAE")
        plt.plot(n[key], mae[key], label=key)
        plt.grid(True)
        plt.savefig(f"graphs/mae/mae-{key}-based.png")
        plt.close()

        plt.figure()
        plt.title(f"RATIO for: jaccard version p = 3, {key} based, arithmetic average")
        plt.xlabel("n")
        plt.ylabel("RATIO")
        plt.plot(n[key], ratio[key], label=key)
        plt.grid(True)
        plt.savefig(f"graphs/ratio/ratio-{key}-based.png")
        plt.close()

        plt.figure()
        plt.title(f"Time for: jaccard version p = 3, {key} based, arithmetic average")
        plt.xlabel("n")
        plt.ylabel("Time [s]")
        plt.plot(n[key], elapsed_time[key], label=key)
        plt.grid(True)
        plt.savefig(f"graphs/time/time-{key}-based.png")
        plt.close()


def hybrid_vs_cf():
    key_to_files = {"hybrid": "results/hybrid/True",
                    "cosine version": "results/AlgorithmType.item_based/cosine_True"}
    n, elapsed_time, ratio, mae, rmse = add_data(key_to_files, 100)

    plt.figure()
    plt.title(f"MAE for hybrid and cosine version (hotel based) with weighted average")
    plt.xlabel("n")
    plt.ylabel("MAE")
    for key in key_to_files:
        plt.plot(n[key], mae[key], label=key)
    plt.legend(title="Algorithm", loc="lower right")
    plt.grid(True)
    plt.savefig(f"graphs/mae/mae-hybrid-vs-cf.png")
    plt.close()

    plt.figure()
    plt.title(f"RMSE for hybrid and cosine version (hotel based) with weighted average")
    plt.xlabel("n")
    plt.ylabel("RMSE")
    for key in key_to_files:
        plt.plot(n[key], rmse[key], label=key)
    plt.legend(title="Algorithm", loc="lower right")
    plt.grid(True)
    plt.savefig(f"graphs/rmse/rmse-hybrid-vs-cf.png")
    plt.close()

    plt.figure()
    plt.title(f"RATIO for hybrid and cosine version (hotel based) with weighted average")
    plt.xlabel("n")
    plt.ylabel("RATIO")
    for key in key_to_files:
        plt.plot(n[key], ratio[key], label=key)
    plt.legend(title="Algorithm", loc="lower right")
    plt.grid(True)
    plt.savefig(f"graphs/ratio/ratio-hybrid-vs-cf.png")
    plt.close()

    plt.figure()
    plt.title(f"Time for hybrid and cosine version (hotel based) with weighted average")
    plt.xlabel("n")
    plt.ylabel("Time [s]")
    for key in key_to_files:
        plt.plot(n[key], elapsed_time[key], label=key)
    plt.legend(title="Algorithm", loc="lower right")
    plt.grid(True)
    plt.savefig(f"graphs/time/time-hybrid-vs-cf.png")
    plt.close()


if __name__ == "__main__":
    active_users_vs_all_users()
    positive_ratings_analysis()
    item_vs_user_based()
    hybrid_vs_cf()
