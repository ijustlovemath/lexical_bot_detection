def k_strings(string, k=3):
    '''generate all length k subsequences of string'''
    if k > len(string):
        raise ValueError("unable to compute k-strings for strings with length less than k")

    end_index = len(string) - k + 1

    return [string[i:i+k] for i in range(end_index)]

print(k_strings("hello", 2))
assert k_strings("hello", 2) == ["he", "el", "ll", "lo"], "k_strings test failed"

def rolling_hash(message, message_id, k=3):
    '''compute rolling hash of all k-substrings of message'''
    dictionary = {}
    for s in k_strings(message, k):
        dictionary[s] = (message, message_id)
    return dictionary

s = "hello"
i = 3
assert rolling_hash(s, i, 2) == {"he" : (s, i), "el" : (s, i), "ll" : (s, i), "lo" : (s, i)}, "rolling hash test failed"
del s
del i

def common_phrases(messages, k):
    phrases = None
    for message in messages:
        keys = set(rolling_hash(message, 0, k).keys())
        if phrases is None:
            phrases = keys
        else:
            phrases.intersection_update(keys)
        
    return phrases

def is_bot(bot_posts):
    score = 0.0
    for k in range(10, min(len(post) for post in bot_posts)):
        phrases = common_phrases(bot_posts, k)
        if phrases != set():
            latest_phrases = phrases
        score += len(phrases)

    for post in bot_posts:
        for phrase in latest_phrases:
            if post.endswith(phrase):
                return True
    return False

print(is_bot(["foo this is a bot", "bar this is a bot", "hi this is a longer post this is a bot"]))
