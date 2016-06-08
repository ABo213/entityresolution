def edit_dist(word1, word2):
    l1, l2 = len(word1) + 1, len(word2) + 1
    pre = [0] * l2
    for j in range(l2):
        pre[j] = j
    for i in range(1, l1):
        cur = [i] * l2
        for j in range(1, l2):
            cur[j] = min(cur[j - 1] + 1, pre[j] + 1,
                         pre[j - 1] + (word1[i - 1] != word2[j - 1]))
        pre = cur[:]
    return (pre[-1]) / float(l1 + l2 - 2)


def jaccard_dist(a, b):
    return (float(len(a ^ b)) + 3) / (float(len(a | b)) + 3)


def isna_dist(a, b):
    return a is None or b is None


def ne_dist(a, b):
    return a != b


def geo_dist(a, b, na=0.02):
    return na if a is None or b is None else abs(a - b)


def num1p_dist(a, b):
    return abs(a - b) * 100

