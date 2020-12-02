---
title: "Advent of Code: Day 2"
categories:
  - Blog
tags:
  - Advent of Code
  - Raku
---

We're back again with another functional Raku solution! This problem requires some text parsing as well, which is where Raku (and its older brother Perl) really shine, so that was quite a bit of fun to utilize. Let's dive right in!

## The Problem

### Part 1

Given a file full of lines that look like this:

```
1-3 a: ababa
10-14 q: qqqqqqqqq
```

Which can be interpretted as a password policy that reads as such:

```
The password "ababa" must contain between 1 and 3 (inclusive) "a" characters
The password "qqqqqqqqqq" must contain between 10 and 14 (inclusive) "q" characters
```

Our job is to find how many passwords are **valid**.

#### Solution

[GitHub Link](https://github.com/aaronreidsmith/advent-of-code/blob/main/2020/02/raku/main.raku)

See below for explanation and any implemenation specific comments

```
grammar PasswordEntry {
    token TOP { ^(<digit>+)'-'(<digit>+) <.ws> (<[a..z]>)':' <.ws> (<[a..z]>+)$ } # [1]
}

grammar PasswordEntryActions {
    method TOP($/) {                                                          # [2]
        my $range-start  = $/[0].Int;
        my $range-end    = $/[1].Int;
        my $target       = $/[2].Str;
        my $password     = $/[3].Str;
        my $target-count = $password.comb($target).elems;                     # [3]
        make so $range-start <= $target-count && $target-count <= $range-end;
    }
}

sub MAIN($file) {
    my $actions = PasswordEntryActions.new;
    say $file.IO.lines
          .map(-> $row { PasswordEntry.parse($row, :$actions).made }) # [4]
          .grep(* == True)                                            # [5]
          .elems;
}
```

This runs as such:

```
$ raku main.raku input.txt
393
```

#### Explanation

We do a couple things here:

First we pull in all the lines in the file, then parse them using our `PasswordEntry` grammar. See below for the explanation on the grammar.

When we parse each line, we specify what actions should take place with the parsed text (in this case, we pass it to `PasswordEntryActions` to do post-processing). `PasswordEntryActions` takes the input (a [`Match`](https://docs.raku.org/type/Match) object), and determines if the parsed password contains the right number of target characters.

These are then filtered down to only those that _do_ contain the right number of characters (valid passwords) and counted.

##### Specific Comments

1. We could just define a regex like `my $regex = /pattern/`, but I wanted to combine the parse step _and_ the business logic of determining if it is a valid password; we will get into that second part below.
  - When definining a grammar, you always have to define a `TOP` token the encompasses everything. If I had a more complex grammar, I could define subtokens that could be used in the `TOP` token (or any other defined tokens).
  - For the non-regex folks, the way this reads is:
        - Start of line
        - An integer (captured group, see below)
        - Followed by a dash
        - Followed by an integer (captured group, see below)
        - Followed by a space
        - Followed by a single lowercase letter (captured group, see below)
        - Followed by a colon
        - Followed by a space
        - Followed by one or more lowercase letters (captured group, see below)
        - End of line
  - Additionally, you'll notice the four sets of parenthese that define _capture groups_, meaning when this grammar parses a line successfully, it will return the four groups in an array.
  
2. When we use the parser (`PasswordEntry.parse`), we are able to supply this `actions` class that has methods corresponding to the tokens in the parser. This is where any business logic should take place. For example, any type casting or object creation to be used in the outer scope. In this case, like I said above, we want to parse and reduce to `True` or `False` in one pass. So what our `TOP` method does is take the match `$/` (this is a special variable, I would never name something like this), extract the four groups defined in the grammar, and cast them to the correct types. We then count the number of times the target appears in the password and see if it is in range.
3. `comb` takes a string and turns it into a list of characters. When supplied with a string argument (in this case, `$target`), it turns the string into a list _and_ filters it down to elements that equal the supplied character.
4. There is some special syntax going on on this line. I could have written `PasswordEntry.parse($row, actions => $actions)`, and used `$actions` as a named keyword. But, since my variable has the same name as the target argument, I am able to pass it in as `:$actions`. It reminds me of `**kwargs` in Python.
5. I _hate_ that I have to say `* == True`, but `grep` would not work otherwise, so I guess that is just an edge case.

### Part 2

Given the same file as before, the interpretation of the lines has changed. Given the same lines as above, the intperpretation should now be:

```
The password "ababa" must contain an "a" character in position 1 or 3 (but not both)
The password "qqqqqqqqqq" must contain a "q" character in position 10 or 14 (but not both)
```

**Note:** These strings are 1-indexed instead of 0-indexed, so we have to account for that.

#### Solution

[GitHub Link](https://github.com/aaronreidsmith/advent-of-code/blob/main/2020/02/raku/main.raku)

See below for explanation and any implemenation specific comments

```
grammar PasswordEntry {
    token TOP { ^(<digit>+)'-'(<digit>+) <.ws> (<[a..z]>)':' <.ws> (<[a..z]>+)$ }
}

class PartOneActions {
    method TOP($/) {
        my $range-start  = $/[0].Int;
        my $range-end    = $/[1].Int;
        my $target       = $/[2].Str;
        my $password     = $/[3].Str;
        my $target-count = $password.comb($target).elems;
        make so $range-start <= $target-count && $target-count <= $range-end;
    }
}

class PartTwoActions {
    method TOP($/) {
        my $position-one = $/[0].Int - 1;
        my $position-two = $/[1].Int - 1;
        my $target       = $/[2].Str;
        my @password     = $/[3].Str.comb;
        make so (
            (@password[$position-one] cmp $target) == Same # [1][2]
            xor                                            # [3]
            (@password[$position-two] cmp $target) == Same
        );
    }
}

sub MAIN($file, Bool :$p2 = False) {
    my $actions = $p2 ?? PartTwoActions.new !! PartOneActions.new;
    say $file.IO.lines
          .map(-> $row { PasswordEntry.parse($row, :$actions).made })
          .grep(* == True)
          .elems;
}
```

This runs as such:

```
# Part 1
$ raku main.raku input.txt
393

# Part 2
$ raku main.raku --p2 input.txt
690
```

#### Explanation

Similarly to [day 1](https://aaronreidsmith.github.io/blog/advent-of-code-day-01/), we can utilize the code already written and tweak it a little bit. In this case, the grammar stays the same, but the actions taken on each line need to change.

Again, we provide the `--p2` flag, and then add the `PartTwoActions` class to handle the business logic for the new interpretation of the password policy.

##### Specific Comments

1. I had to use `cmp` instead of `==` here to get proper string comparison (otherwise, Raku tries to cast strings to hexadecimal).
2. `cmp` returns `Less`, `More` or `Same` instead of a boolean. I couldn't find a way to cast `Same` to a boolean, because it casts it as such `Same -> 0 -> False`, when what we really want is `True`, so I had to add the ugly `== Same`.
3. `|` is a junction operator in Raku, so it has the handy dandy `xor` operator utilized here.


## Final Thoughts

Another functional and (in my opinion) beautiful solution! In my day job, I actually maintain a grammar defined using [ANTLR](https://www.antlr.org/), so it is fun to see tools with the same concepts in other languages. Looking forward to getting to use grammars more in Raku. See y'all tomorrow!