import pandas as pd

def keywords():
    diff_language = {
        "Cross language",
        "Crosslanguage",
        "Cross lingual",
        "Crosslingual",
        "Cross linguistic",
        "Crosslinguistic",
        "Multi language",
        "Multilanguage",
        "Multi lingual",
        "Multilingual",
        "Multi linguistic",
        "Multilinguistic",
        "Machine translation"
    }

    copy = {
        "Copy",
        "Duplicate",
        "Plagiarism"
    }

    detection = {
        "Detection",
        "Discovery"
    }
    terms = []
    for dl in diff_language:
        for cp in copy:
            for de in detection:
                # terms.append('"' + dl + '"' + ' +' + cp + ' +' + de)
                terms.append((dl, cp, de))
                # print(terms[0])

    print ("Keywords created!!")
    df = pd.DataFrame(terms, columns=['dl', 'cp', 'de'])
    df.to_csv('keywords.csv', sep="\t", encoding="utf-8", index=None)
    return terms
    # else:
    #     return "Keywords already created!!"
