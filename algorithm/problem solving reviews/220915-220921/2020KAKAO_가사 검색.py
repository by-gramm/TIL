"""
정확성 테스트 통과, 효율성 테스트 5개중 2개 통과
"""

def solution(words, queries):
    words_length = [[] for _ in range(10001)]
    counts = []
    
    for word in words:
        words_length[len(word)].append(word)
    
    for query in queries:
        Q_LEN = len(query)
        is_not_wildcard = []
        
        for idx in range(Q_LEN):
            if query[idx] != '?':
                is_not_wildcard.append(idx)
        
        count = 0
        
        for word in words_length[Q_LEN]:
            for idx in is_not_wildcard:
                if query[idx] != word[idx]:
                    break
            else:
                count += 1
        
        counts.append(count)
    
    return counts
