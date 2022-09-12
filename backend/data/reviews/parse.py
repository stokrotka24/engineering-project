from datetime import datetime


def parse_date(review_date):
    return datetime.strptime(review_date, "%Y-%m-%d %H:%M:%S").date()


def parse_content(content: str):
    sequences_map = {':\\': r':\ ',  # sad emoticon
                     }
    char_map = {'\n': r'\n',
                '\r': r'\r',
                '\t': r'\t',
                '\'': r'\'',
                '\"': r'\"',
                '\\': ''}

    for (sequence, replacement) in sequences_map.items():
        content = content.replace(sequence, replacement)

    parsed_content = ''
    for char in content:
        parsed_content += char_map.get(char, char)
    return parsed_content


def parse_reviews(reviews):
    parsed_reviews = []

    for review in reviews:
        parsed_review = {}

        for review_property in review:
            match review_property:
                case "review_id":
                    parsed_review["id"] = review["review_id"]
                case "business_id":
                    parsed_review["hotel_id"] = review["business_id"]
                case "date":
                    parsed_review["date"] = parse_date(review["date"])
                case "text":
                    parsed_review["content"] = parse_content(review["text"])
                case "useful" | "funny" | "cool":
                    pass
                case other:
                    parsed_review[other] = review[other]

        parsed_reviews.append(parsed_review)

    return parsed_reviews
