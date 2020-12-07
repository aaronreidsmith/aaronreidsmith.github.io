---
title: "Advent of Code: Day 7"
categories:
  - Blog
tags:
  - Advent of Code
  - Python
---

Well, today was our streak breaker. For the life of me, I could not get Raku to run in a timely manner. I ended up reverting to Python and using a more imperative approach. Nevertheless, I am sharing it here for anyone who cares!

## The Problem

### Part 1

For the past few days, we have been traveling. First we had troubles at [the airport](https://aaronreidsmith.github.io/blog/advent-of-code-day-04/), then we had trouble [finding our seat](https://aaronreidsmith.github.io/blog/advent-of-code-day-05/), and then we had issues filling out the [customs form](https://aaronreidsmith.github.io/blog/advent-of-code-day-06/). But, we have landed safely and are ready to enjoy our vacation!

However, our luggage is taking a long time getting to the carousel due to recent luggage rules that have been put into effect. We are given a list of the rules that looks like the following:

```
light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
```

We have a **shiny gold** bag, and we want to know how many color combinations there are for the outermost bag. With the above example, we have:

- A bright white bag, which can hold our shiny gold bag directly
- A muted yellow bag, which can hold our shiny gold bag directly, plus some other bags
- A dark orange bag, which can hold bright white and muted yellow bags, either of which could then hold our shiny gold bag
- A light red bag, which can hold bright white and muted yellow bags, either of which could then hold our shiny gold bag

So the question is, given a much larger input file, how many outermost bags can eventually hold our shiny gold bag?

#### Solution

[GitHub Link](https://github.com/aaronreidsmith/advent-of-code/blob/main/2020/07/python/main.py)

See below for explanation and any implementation-specific comments.

```python
from dataclasses import dataclass
from typing import List, Tuple
import sys


@dataclass(unsafe_hash=True) # [1][2]
class Bag:
    adjective: str
    color: str

    def contains_target(self, target, rules):
        rule = rules[self]
        held_bags = [item[0] for item in rule.contents]
        return any(bag == target or bag.contains_target(target, rules) for bag in held_bags)
        

@dataclass
class Rule:
    bag: Bag
    contents: List[Tuple[Bag, int]]


def parse_line(line):
    bag_desc, contents = line.split(' contain ')

    # Create Bag
    adjective, color, _ = bag_desc.split(' ')
    bag = Bag(adjective, color)

    # Fill in contents
    _contents = []
    if contents != 'no other bags.':
        inner_bags = contents.split(', ')
        for _bag in inner_bags:
            quantity, adjective, color, _ = _bag.split(' ')
            inner_bag = (Bag(adjective, color), int(quantity))
            _contents.append(inner_bag)

    # Turn the contents into a rule and return
    rule = Rule(bag, _contents)
    return (bag, rule)


if __name__ == '__main__':
    input_file = sys.argv[1]

    rules = {}
    with open(input_file) as file:
        for line in file:
            stripped = line.strip()
            bag, rule = parse_line(stripped)
            rules[bag] = rule

    target = Bag('shiny', 'gold')

    can_hold_target = 0
    for bag in rules.keys():
        if bag.contains_target(target, rules):
            can_hold_target += 1
            
    print(can_hold_target)

```

This runs as such:

```
$ python main.py input.txt
151
```

#### Explanation

The logic of this one is fairly straightforward:

1. For each line in the file, we turn it into a key-value pair of `Bag` and `Rule`, where the `Bag` contains the color of the outer bag and the `Rule` contains a list of inner bags, as well as how many of them we hold.
2. For each outer bag we call `.contains_target` which will recursively check if this bag will ever hold our shiny gold bag.
3. We tally up the outer bags that returned `True` above.

I tried to apply this logic in Raku, but I just kept finding myself fighting the type system. 

First, rather than the inelegant parsing I did here, I tried to use one of Raku's [grammars](https://docs.raku.org/type/Grammar), which ended up being clunky, and it took me several hours just to get the data to parse.

Once it was parsed to my liking, I ran into an issue that `Hash`es only use strings as keys. There _is_ a way to circumvent it, but there is a [known bug](https://docs.raku.org/language/hashmap#index-entry-non-string_keys) in the compiler that casts them to strings anyway.

Finally, after rewriting my parser and using parameterized hashes as the above documentation suggested, I began fighting their type system. Here is what a `Hash`'s declaration looks like:

```
class Hash is Map { }
class Map does Associative does Iterable { }
role Associative[::TValue = Mu, ::TKey = Str(Any)] { }
role Iterable { }
```

So some functions expect a `Hash`, others expect an `Iterable` others an `Associative`. With non-parameterized types, they all work great and it just converts it to what it needs at runtime. However, with the parameterized types needed to circumvent the `Hash` issue, I would get errors like this:

```
Error: Expected Associative[Bag] but found Hash[Bag]
```

Rather than waste my whole day on the issue, I decided to fall back to ol' reliable: Python.

##### Specific Comments

1. Dataclasses are a fairly recent addition to Python, and are similar to Scala [case classes](https://docs.scala-lang.org/tour/case-classes.html). The idea is they generate the `__init__` and other helper functions for you, and are meant to be used to store data with keys (similar to a [`namedtuple`](https://docs.python.org/3/library/collections.html)).
2. To use an object as a key in a dictionary, it has to implement `__hash__` and `__eq__`. By default, the `dataclass` does not generate a `__hash__` function for us, but it will with `unsafe_hash=True`. Normally you would want to implement your own `__hash__` function, but it is safe in this case

### Part 2

Now the question flips: if our _outermost_ bag is our shiny gold bag, how many bags are we required to store inside of it?

#### Solution

[GitHub Link](https://github.com/aaronreidsmith/advent-of-code/blob/main/2020/07/python/main.py)

See below for explanation and any implementation-specific comments.

```python
from dataclasses import dataclass
from typing import List, Tuple
import sys


@dataclass(unsafe_hash=True)
class Bag:
    adjective: str
    color: str

    def contains_target(self, target, rules):
        rule = rules[self]
        held_bags = [item[0] for item in rule.contents]
        return any(bag == target or bag.contains_target(target, rules) for bag in held_bags)

    def get_contents(self, rules):
        contents = rules[self].contents
        total_bags = 0
        for bag, quantity in contents:
            total_bags += quantity + (quantity * bag.get_contents(rules))

        return total_bags


@dataclass
class Rule:
    bag: Bag
    contents: List[Tuple[Bag, int]]


def parse_line(line):
    bag_desc, contents = line.split(' contain ')

    # Create Bag
    adjective, color, _ = bag_desc.split(' ')
    bag = Bag(adjective, color)

    # Fill in contents
    _contents = []
    if contents != 'no other bags.':
        inner_bags = contents.split(', ')
        for _bag in inner_bags:
            quantity, adjective, color, _ = _bag.split(' ')
            inner_bag = (Bag(adjective, color), int(quantity))
            _contents.append(inner_bag)

    # Turn the contents into a rule and return
    rule = Rule(bag, _contents)
    return (bag, rule)


if __name__ == '__main__':
    input_file = sys.argv[1]

    rules = {}
    with open(input_file) as file:
        for line in file:
            stripped = line.strip()
            bag, rule = parse_line(stripped)
            rules[bag] = rule

    target = Bag('shiny', 'gold')

    # Part 1
    can_hold_target = 0
    for bag in rules.keys():
        if bag.contains_target(target, rules):
            can_hold_target += 1

    # Part 2
    total_contents = target.get_contents(rules)

    print(f'Part 1: {can_hold_target}')
    print(f'Part 2: {total_contents}')

```

This runs as such:

```
$ python main.py input.txt
Part 1: 151
Part 2: 41559
```

#### Explanation

As you can see, all we had to add was our `get_contents` function to the `Bag` class. For each bag in the shiny gold bag, it counts not only the bag itself, but all the bags within it as well.

I don't have any implementation-specific comments on this one, as it is pretty straightforward, especially with such a small change from part 1. The only thing I will say is I did not add the CLI that I have added to my Raku solutions because it is much more cumbersome in Python. Every language has its strong suits!

## Final Thoughts

While I am bummed that I failed in my goal to write functional Raku for all 25 days of this thing, I think it is important to note that it is best to use the right tool for the job. I think I could have struggled through it in Raku, but I don't have the time, patience, or know-how to do that; especially when we've got another challenge coming tomorrow! I will continue to try to do the rest of the problems in functional Raku, but if I can't do it, at least we've already bridged that gap!