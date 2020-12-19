---
title: "Advent of Code: Day 19"
categories:
  - Blog
tags:
  - Advent of Code
  - Raku
---

After  I was singing Raku's praises yesterday, it had to come back to bite me.

Today's solution is written in Python because I just couldn't get it to work in Raku. It's iterable handling is, in my opinion, a joke. Between `List`s, `Array`s, and `Seq`s (among others) and no discernible way to differentiate between them at object creation time, and the fact that everything _in_ a list gets cast to a `Scalar` (thus adding an extra container around it), it made it too hard, and I wasn't going to waste my Saturday fighting it.

## The Problem

### Part 1

After we land the elves contact us for help in decoding a transcript they got from a satellite. Some messages are corrupted, but we also have a set of rules the messages have to follow. They send us a file containing both the rules, and the messages that looks like this:

```
0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb
```

Each rule has an **ID** and its **definition**. The definition can either be a single letter ("a" or "b") _or_ a pointer to another rule. Additionally, a rule may have multiple definitions separated by a pipe character (`|`). Luckily, the elves tell us there are **no loops** in the logic.

In the case of rule 0 above, it matches "a" (rule 4), then any of the eight options from rule 1, then "b" (rule 5): `aaaabb`, `aaabab`, `abbabb`, `abbbab`, `aabaab`, `aabbbb`, `abaaab`, or `ababbb`.

Comparing this to the list of messages, we can see that only `ababbb` and `abbbab` match entirely (meaning no extra characters left over). In our real input, how many messages match rule 0?

#### Solution

[GitHub Link](https://github.com/aaronreidsmith/advent-of-code/blob/main/2020/19/python/main.py)

See below for explanation and any implementation-specific comments.

```python
import sys


def is_match(rules, message, stack):
    if len(stack) > len(message):
        return False
    elif len(stack) == 0 or len(message) == 0:
        return len(stack) == 0 and len(message) == 0

    entry = stack.pop(0)
    if isinstance(entry, str):
        if message[0] == entry:
            return is_match(rules, message[1:], stack.copy()) # [1]
    else:
        for rule in rules[entry]:
            if is_match(rules, message, list(rule) + stack):
                return True

    return False


if __name__ == '__main__':
    with open(sys.argv[1]) as file:
        raw_rules, messages = [x.splitlines() for x in file.read().split('\n\n')]

    rules = {}
    for rule in raw_rules:
        rule_id, contents = rule.split(': ')
        if contents.startswith('"'):
            rules[int(rule_id)] = contents[1]
        else:
            sub_rules = []
            for entry in contents.split(' | '):
                sub_rules.append([int(sub_rule) for sub_rule in entry.split(' ')])

            rules[int(rule_id)] = sub_rules

    count = 0
    for message in messages:
        if is_match(rules, message, rules[0][0].copy()):
            count += 1

    print(count)
```

This runs as such:

```
$ python main.py input.txt
120
```

#### Explanation

I started this as a recursive regex problem in Raku. Seeing as Raku is supposedly good for regexes, it seemed like a good idea. Halfway through implementation I realized it would work better as just an iterative problem; trying to implement it in Raku proved difficult as well, so I went back to Python.

The logic here is actually much simpler than it may seem from the problem.

1. We parse our input into 2 pieces:
  - A dictionary of rules that looks like this (using the example data): `{0: [[4, 1, 5]], 1: [[2, 3], [3, 2]], 2: [[4, 4], [5, 5]], 3: [[4, 5], [5, 4]], 4: 'a', 5: 'b'}`
  - A list of messages
2. We iterate through each message and apply the following logic:
  - If the length of the rule is longer than the length of the message, return `False`
  - If _either_ the rule list, or the message is empty, check if they both are. If they both are, return `True`, otherwise `False`
  - Get the next item from the rules list.
    - If it is `a` or `b`, check if that is the next letter in the message. If yes, keep looking for a match, otherwise return `False`
    - If it is another set of rules, add them _in front_ of any remaining rules we have and check if it is suddenly a match

##### Specific Comments

1. We have to pass a copy of the list in or else it will get out of sync as we prepend items to it.

### Part 2

After all that work, we find two rules in the input are actually wrong! Rules 8 and 11 change as follows.

Old:

```
8: 42
11: 42 31
```

New:

```
8: 42 | 42 8
11: 42 31 | 42 11 31
```

So now the rules _can_ contain loops. How will this affect us? Our job is still to find how many messages match rule 0.

#### Solution

[GitHub Link](https://github.com/aaronreidsmith/advent-of-code/blob/main/2020/19/python/main.py)

See below for explanation and any implementation-specific comments.

```python
import sys


def is_match(rules, message, stack):
    if len(stack) > len(message):
        return False
    elif len(stack) == 0 or len(message) == 0:
        return len(stack) == 0 and len(message) == 0

    entry = stack.pop(0)
    if isinstance(entry, str):
        if message[0] == entry:
            return is_match(rules, message[1:], stack.copy())
    else:
        for rule in rules[entry]:
            if is_match(rules, message, list(rule) + stack):
                return True

    return False


def count_matches(rules, messages, initial_stack):
    count = 0
    for message in messages:
        if is_match(rules, message, initial_stack.copy()):
            count += 1

    return count


if __name__ == '__main__':
    with open(sys.argv[1]) as file:
        raw_rules, messages = [x.splitlines() for x in file.read().split('\n\n')]

    rules = {}
    for rule in raw_rules:
        rule_id, contents = rule.split(': ')
        if contents.startswith('"'):
            rules[int(rule_id)] = contents[1]
        else:
            sub_rules = []
            for entry in contents.split(' | '):
                sub_rules.append([int(sub_rule) for sub_rule in entry.split(' ')])

            rules[int(rule_id)] = sub_rules

    initial_stack = rules[0][0]
    print(f'Part 1: {count_matches(rules, messages, initial_stack)}')

    rules[8] = [[42], [42, 8]]
    rules[11] = [[42, 31], [42, 11, 31]]
    print(f'Part 2: {count_matches(rules, messages, initial_stack)}')
```

This runs as such:

```
$ python main.py input.txt
Part 1: 120
Part 2: 350
```

#### Explanation

We're lucky we didn't go with the recursive regex solution, because that would have likely caused a rewrite. You can see only a few things changed:

1. We added the `count_matches` helper function
2. We call the helper function twice, once before changing rules 8 and 11 and once after

That's it! The reason this works is because as soon as the `stack` variable starts to get infinitely long, it will get caught by the `len(stack) > len(message)` check and immediately return `False`.

## Final Thoughts

This whole process is wearing on me, especially given the choice to do it using functional Raku (which obviously hasn't worked out), but we are almost done! Less than a week to go!
