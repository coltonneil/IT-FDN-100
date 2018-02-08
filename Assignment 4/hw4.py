"""
takes two lists of words, one in english and one in french, joins them into a dictionary and allows the user to type
in a word in english to receive its french translation
"""

print("--- English to French translator ---")

# create lists of words and joins them into the translations dict
english = ["hello", "goodbye", "tomorrow", "today", "yesterday", "dog", "cat", "me", "you", "they", "day",
           "night", "food", "water", "bathroom"]
french = ["bonjour", "au revoir", "demain", "aujourd'hui", "hier", "chien", "chat", "moi", "toi", "ils", "journée",
          "nuit", "aliments", "eau", "salle de bains"]

translations = dict(zip(english, french))

print("Translation options: {}".format(", ".join(english)))

# set parameters for while loops
allowed = 5
attempts = 0
found = False

# get user_key and check if it is a key in the dict, if it is break while loop, else increment attempts and try again
while attempts < allowed:
    print("{} attempts remaining".format(allowed - attempts))
    user_key = input("Enter a word to translate: ")
    if user_key in translations.keys():
        found = True
        break
    else:
        print("Does not exist")
        attempts += 1

# if the user_key was in the dict, display its translation, if not exit
if found:
    print("{} in French is {}".format(user_key.capitalize(), translations[user_key].capitalize()))
else:
    print("No more attempts remaining, exiting")
