def k_strings(string, k=3):
    '''generate all length k subsequences of string'''
    if k > len(string):
        raise ValueError("unable to compute k-strings for strings with length less than k")

    n = len(string) - k + 1

    return [string[i:i+k] for i in range(n)]

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

def all_equal(iterator):
    iterator = iter(iterator)

    try:
        first = next(iterator)
    except StopIteration:
        return True
    return all(first == rest for rest in iterator)

def is_bot(bot_posts, minimum_phrase_length=10, maximum_post_length=50):
    ''' generate all common phrases from 10 to the length of the minimum post
    Looks like this essentially gets the longest phrases possible'''
    score = 0.0
    minimum_phrase_length = 10

    # trivial check for silly bots
    if all_equal(bot_posts):
        return True

    latest_phrases = set()
    bot_posts = [post for post in bot_posts if len(post) > minimum_phrase_length]
    minimum_post_length = min(len(post) for post in bot_posts)
    minimum_post_length = min(minimum_post_length, maximum_post_length)
    if minimum_post_length < minimum_phrase_length + 1:
        raise ValueError
    for k in range(minimum_post_length, minimum_phrase_length, -1):
        phrases = common_phrases(bot_posts, k)
        if phrases != set():
            latest_phrases = phrases
        score += len(phrases)
        for post in bot_posts:
            for phrase in latest_phrases:
                if post.endswith(phrase) or post.startswith(phrase):
                    return True

    return False

if __name__ == '__main__':
    print(is_bot(["foo this is a bot", "bar this is a bot", "hi this is a longer post this is a bot"]))
