import string

"""
This script reads in a file, parses the lines and creates a list of words from the lines
Calculates the word frequency
Gets the word with the maximum frequency
Gets the minimum frequency and a list of words with that frequency
Calculates the percentage of words that are unique in the file and prints it
"""

# open file and stores its content as a list
with open("./Odyssey.txt") as file:
    file_contents = file.readlines()

# create translator to remove punctuation
translator = str.maketrans('', '', string.punctuation)

# put the words in the file into a list split on spaces and no trailing whitespace
words_in_file = []
for line in file_contents:
    striped_line = line.strip()
    # lower case all words and remove punctuation
    words_in_file.extend(striped_line.translate(translator).lower().split(" "))


# remove empty strings
words_in_file = list(filter(None, words_in_file))
# get number of words in file
num_words_in_file = len(words_in_file)

# store the unique words and their occurrences in a dict
words_dict = {}
# loop through word list
for word in words_in_file:
    # if word is already in the words_dict, increment
    if word in words_dict:
        words_dict[word] += 1
    # if word is not in the words_dict, add it and set its value to 1
    else:
        words_dict[word] = 1

# store the occurrence rate of each word in a dict
occurrence_rate = {}

for word in words_dict:
    word_occurrence_rate = words_dict[word] / num_words_in_file
    occurrence_rate[word] = word_occurrence_rate

num_unique_words = len(words_dict)

# get most and least frequent word
most_frequent = max(words_dict, key=words_dict.get)
least_frequent = min(words_dict, key=words_dict.get)

print("The most frequently used word is: {}".format(most_frequent))

# get the rate of occurrence for the least frequent word
min_occurrence_rate = words_dict[least_frequent]/num_words_in_file

# get all of the words that have the min occurrence rate
min_occurrence_list = []

for word in words_dict:
    if words_dict[word] == 1:
        min_occurrence_list.append(word)

# get a count for the number of words with the min occurrence rate
num_min_occurrence_words = len(min_occurrence_list)

# print frequency results
print("The minimum frequency is {:.5f}%, {} words have this frequency.".format(min_occurrence_rate, num_min_occurrence_words))

# print the total words and number of unique words
print("There are {} words and {}({:.2f}%) unique words".format(num_words_in_file, num_unique_words, num_min_occurrence_words/num_words_in_file))