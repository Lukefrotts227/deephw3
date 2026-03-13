#! /bin/bash
# Scores for different sections of the homework
#

test1=25
test2=25
test3=25
author_block=25

# Warn the caller if the Author or Netid fields are missing.
grep -P "Author:" hw03.py
if [[ $? -ne 0 ]]; then
    echo "Warning: Author field missing."
    echo "Your code must have a comment with the following:"
    echo -e "\tAuthor: your name"
    author_block=0
fi

grep -P "Netid:" hw03.py
if [[ $? -ne 0 ]]; then
    echo "Warning: Netid field missing."
    echo "Your code must have a comment with the following:"
    echo -e "\tNetid: your netid"
    author_block=0
fi

out=$(python3 hw03.py example_test_digit_4.png)
if [[ "$out" != "Prediction is 4 with confidence 0.999797" ]]; then
    echo "Failed with test digit 4"
    test1=0
fi

out=$(python3 hw03.py validate_test_digit_8.png)
if [[ "$out" != "Prediction is 1 with confidence 0.999607" ]]; then
    echo "Failed with validation digit 8"
    test2=0
fi

out=$(python3 hw03.py validate_test_digit_9.png)
if [[ "$out" != "Prediction is 9 with confidence 0.988948" ]]; then
    echo "Failed with validation digit 9"
    test3=0
fi

echo "Score is $(( test1 + test2 + test3 +  author_block))"



