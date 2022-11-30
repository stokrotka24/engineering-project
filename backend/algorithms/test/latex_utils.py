import ast


def convert_tuples_list_to_dict(l: list):
    d: dict = dict()
    for (elem1, elem2) in l:
        d[elem1] = elem2
    return d


def add_single_result(results_line, result):
    if result is None:
        results_line += " - &"
    else:
        results_line += f" {round(result, 3)} &"
    return results_line


def add_endline(results_line):
    return results_line[:-1] + "\\\\ \\hline\n"


def latex_table_body(list_1, title_1, list_2, title_2):
    dict_1 = convert_tuples_list_to_dict(list_1)
    dict_2 = convert_tuples_list_to_dict(list_2)

    ranking_sizes = list(filter(lambda t: t > 2, dict_1.keys()))
    ranking_sizes.sort()

    size_line = "$k$ &"
    line_1 = f"{title_1} &"
    line_2 = f"{title_2} &"
    for ranking_size in ranking_sizes:
        size_line += f" {ranking_size} &"
        line_1 = add_single_result(line_1, dict_1.get(ranking_size))
        line_2 = add_single_result(line_2, dict_2.get(ranking_size))

    size_line = add_endline(size_line)
    line_1 = add_endline(line_1)
    line_2 = add_endline(line_2)
    return size_line + line_1 + line_2


if __name__ == "__main__":
    with open("results/content_based.txt") as f:
        lines = f.readlines()
        dcg = ast.literal_eval(lines[3])
        ndcg = ast.literal_eval(lines[4])
        print(latex_table_body(dcg, "$DCG_k$",
                               ndcg, "$nDCG_k$"))

    with open("results/jaccard.txt") as f:
        lines = f.readlines()
        jaccard_dcg = ast.literal_eval(lines[3])
    with open("results/content_based_vs_jaccard.txt") as f:
        lines = f.readlines()
        content_based_dcg = ast.literal_eval(lines[3])
    print(latex_table_body(jaccard_dcg, "$DCG_k$ (\\textit{jaccard})",
                           content_based_dcg, "$DCG_k$ (\\textit{content based})"))

    with open("results/jaccard.txt") as f:
        lines = f.readlines()
        jaccard_dcg = ast.literal_eval(lines[4])
    with open("results/content_based_vs_jaccard.txt") as f:
        lines = f.readlines()
        content_based_dcg = ast.literal_eval(lines[4])
    print(latex_table_body(jaccard_dcg, "$nDCG_k$ (\\textit{jaccard})",
                           content_based_dcg, "$nDCG_k$ (\\textit{content based})"))

    with open("results/cosine.txt") as f:
        lines = f.readlines()
        cosine_dcg = ast.literal_eval(lines[3])
    with open("results/content_based_vs_cosine.txt") as f:
        lines = f.readlines()
        content_based_dcg = ast.literal_eval(lines[3])
    print(latex_table_body(cosine_dcg, "$DCG_k$ (\\textit{cosinus})",
                           content_based_dcg, "$DCG_k$ (\\textit{content based})"))

    with open("results/cosine.txt") as f:
        lines = f.readlines()
        cosine_dcg = ast.literal_eval(lines[4])
    with open("results/content_based_vs_cosine.txt") as f:
        lines = f.readlines()
        content_based_dcg = ast.literal_eval(lines[4])
    print(latex_table_body(cosine_dcg, "$nDCG_k$ (\\textit{cosinus})",
                           content_based_dcg, "$nDCG_k$ (\\textit{content based})"))
