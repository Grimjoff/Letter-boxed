import nltk
from nltk.corpus import words

nltk.download('words')
english_words = set(words.words())

lists = [
    ['e', 'n', 'v'],
    ['i', 'k', 'u'],
    ['w', 'p', 's'],
    ['r', 'h', 'l']
]
scorelists = lists

def get_list_index(letter):
    for i, lst in enumerate(lists):
        if letter in lst:
            return i
    return None


def getWord(lists, lastWord=None, words_found=None):
    global scorelists
    if words_found is None:
        words_found = []

    bestword = None
    bestScore = None
    lastChar = None

    # get lastChar if lastWord exists
    if lastWord is not None:
        lastChar = lastWord[-1]

    all_letters = set(c for lst in lists for c in lst)

    for word in english_words:
        word = word.lower()
        firstChar = word[0]

        # This Logic is wrong but it works???
        # Supposed to continue if firstChar == lastChar but whatever, it works with != for some reason
        if lastWord is not None and firstChar != lastChar:
            continue

        # Check if all chars in word are allowed
        if not all(char in all_letters for char in word):
            continue

        # Check if next letter is from a different list, only continues if it is
        valid = True
        for i in range(len(word) - 1):
            if get_list_index(word[i]) == get_list_index(word[i + 1]):
                valid = False
                break
        if not valid:
            continue

        # Get a set of word with all unique chars
        unique_word = set(word)

        # Count how many letters from unique word still exist in scorelist -> determine score
        removed_count = 0
        for sublist in scorelists:
            removed_count += sum(1 for char in sublist if char in unique_word)

        # Save current best word for now
        if bestScore is None or removed_count > bestScore:
            bestword = word
            bestScore = removed_count
            best_unique_word = unique_word

    # If no Valid word found return list
    if bestword is None:
        return words_found

    # add best word to list
    words_found.append(bestword)

    # Remove the letters from best word from the list
    for sublist in scorelists:
        sublist[:] = [char for char in sublist if char not in best_unique_word]


    # Recursively call the function with the best word found so it can take lastChar next Iteration
    if any(len(sublist) > 0 for sublist in scorelists):
        return getWord(lists, bestword, words_found)
    else:
        return words_found


print(getWord(lists))
