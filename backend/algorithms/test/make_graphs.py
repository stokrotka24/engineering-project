from collections import defaultdict
import matplotlib.pyplot as plt

from algorithms.test.predicted_ratings_test import positive_threshold_values, algorithm_types, bool_values, \
    binary_similarities_types
from algorithms.test.similarity_type import SimilarityType

title = {
    SimilarityType.jaccard: "Jaccard",
    SimilarityType.cosine_binary: "Cosine for binary matrix",
    SimilarityType.cosine: "Cosine",
    SimilarityType.cosine_normalized: "Cosine for normalized data"
}


def compare_positive_threshold():
    for similarity_type in binary_similarities_types:
        for algorithm_type in algorithm_types:
            for weighted_average in bool_values:
                n = defaultdict(list)
                elapsed_time = defaultdict(list)
                prediction_ability = defaultdict(list)
                mae = defaultdict(list)
                rmse = defaultdict(list)

                for positive_threshold in positive_threshold_values:
                    with open(
                            f"results/{algorithm_type}/{similarity_type}_{weighted_average}_{positive_threshold}") as f:
                        lines = f.readlines()
                        for line in lines:
                            line = line.strip().split(" ")
                            n[positive_threshold].append(int(line[0]))
                            elapsed_time[positive_threshold].append(float(line[1]))
                            prediction_ability[positive_threshold].append(float(line[2]) * 100)
                            mae[positive_threshold].append(float(line[3]))
                            rmse[positive_threshold].append(float(line[4]))

                plt.figure()
                plt.title(title[similarity_type])
                plt.xlabel("n")
                plt.ylabel("time [s]")
                for positive_threshold in positive_threshold_values:
                    plt.plot(n[positive_threshold], elapsed_time[positive_threshold], label=positive_threshold)
                plt.legend(title="Positive threshold", loc="lower right")
                plt.grid(True)
                plt.savefig(f"graphs/{algorithm_type}/time/positive_threshold/{similarity_type}_{weighted_average}.png")
                plt.close()

                plt.figure()
                plt.title(title[similarity_type])
                plt.xlabel("n")
                plt.ylabel("prediction ability [%]")
                for positive_threshold in positive_threshold_values:
                    plt.plot(n[positive_threshold], prediction_ability[positive_threshold], label=positive_threshold)
                plt.legend(title="Positive threshold", loc="lower right")
                plt.grid(True)
                plt.savefig(
                    f"graphs/{algorithm_type}/prediction_ability/positive_threshold/{similarity_type}_{weighted_average}.png")
                plt.close()

                plt.figure()
                plt.title(title[similarity_type])
                plt.xlabel("n")
                plt.ylabel("mean absolute error")
                for positive_threshold in positive_threshold_values:
                    plt.plot(n[positive_threshold], mae[positive_threshold], label=positive_threshold)
                plt.legend(title="Positive threshold", loc="lower right")
                plt.grid(True)
                plt.savefig(f"graphs/{algorithm_type}/mae/positive_threshold/{similarity_type}_{weighted_average}.png")
                plt.close()

                plt.figure()
                plt.title(title[similarity_type])
                plt.xlabel("n")
                plt.ylabel("root mean square error")
                for positive_threshold in positive_threshold_values:
                    plt.plot(n[positive_threshold], rmse[positive_threshold], label=positive_threshold)
                plt.legend(title="Positive threshold", loc="lower right")
                plt.grid(True)
                plt.savefig(f"graphs/{algorithm_type}/rmse/positive_threshold/{similarity_type}_{weighted_average}.png")
                plt.close()


# def compare_
compare_positive_threshold()
