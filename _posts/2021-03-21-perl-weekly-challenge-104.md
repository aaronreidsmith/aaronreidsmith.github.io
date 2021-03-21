---
title: "Perl Weekly Challenge 104"
categories:
  - Blog
tags:
  - Perl Weekly Challenge
  - Raku
---

This week had some fun topics like [recursion](https://en.wikipedia.org/wiki/Recursion_(computer_science)), [memoization](https://en.wikipedia.org/wiki/Memoization), and IO/data validation!

## Task 1: FUSC Sequence

Write a script to generate first 50 members of `FUSC` Sequence. Please refer to [OEIS](http://oeis.org/A002487) for more information.

The sequence defined as below:

```
fusc(0) = 0
fusc(1) = 1
for n > 1:
when n is even: fusc(n) = fusc(n / 2),
when n is odd: fusc(n) = fusc((n-1)/2) + fusc((n+1)/2)
```

### Solution

[GitHub Link](https://github.com/manwar/perlweeklychallenge-club/blob/master/challenge-104/aaronreidsmith/raku/ch-1.raku)

See below for explanation and any implementation-specific comments.

```
use experimental :cached; # [1]

sub fusc(Int(Rat) $n) is cached returns Int { # [2]
    given $n {
        when 0      { 0 }
        when 1      { 1 }
        when * %% 2 { fusc($n / 2) }                            # [3]
        default     { fusc(($n - 1) / 2) + fusc(($n + 1) / 2) } # [4]
    }
}

sub MAIN(Int $terms = 50) {
    say (^$terms).map(&fusc); # [4]
}
```

This program runs as such:

```
$ raku ch-1.raku
(0 1 1 2 1 3 2 3 1 4 3 5 2 5 3 4 1 5 4 7 3 8 5 7 2 7 5 8 3 7 4 5 1 6 5 9 4 11 7 10 3 11 8 13 5 12 7 9 2 9)
```

### Explanation

I feel like this is pretty straight forward, and aligns well to the definition of the FUSC sequence. When we look at `$n`, we run through the following logic:

1. Is it 0? Return 0.
2. Is it 1? Return 1.
3. Is it even? Return `fusc($n / 2)`.
4. Otherwise, return `fusc(($n - 1) / 2) + fusc(($n + 1) / 2)`

The function recurses until it ends up in one of the two stopping conditions (0 or 1). So obviously `fusc(50)` is going to go through `fusc(49)`, `fusc(48)`, etc. See below for how we make this efficient.

#### Specific comments

1. Caching in Raku is an experimental feature, so we have to import it (and add the `is cached` trait to our subroutine). The basic idea is that `fusc($n)` is _always_ the same value, so once we calculate it once, we can just look it up later. Adding this trait essentially adds a hash behind the scenes that checks if `fusc($n)` already exists. If it does, it just returns that value, otherwise, it will actually calculate the value and store it in the hash before returning.
2. Notice the function signature takes `Int(Rat)`. This means that this function will accept either `Int` _or_ `Rat` ([Rational number](https://docs.raku.org/type/Rat)) types, but it will coerce the input to an `Int`. The reason for this is that division in Raku will generate a `Rat` type, even for something like `2 / 1`. So we need to convert it to an `Int` on the recursive calls. This saves use from having to write `fusc(($n / 2).Int)`.
3. Raku has a special "is divisible by" operator. So instead of saying `$n % 2 == 0`, we can say `$n %% 2`. Also notice that in the `given` block, we have to use the "whatever star" (`*`) to do this operation; this is because we can't [smartmatch](https://docs.raku.org/language/operators#index-entry-smartmatch_operator) against `%% 2`, so we need to be more explicit.
4. Remember when passing a function as an argument (in this case to `map`), it has a special [sigil](https://docs.raku.org/language/variables#index-entry-sigil_&) -- `&`.
  
## Task 2: NIM Game

Write a script to simulate the NIM Game.

It is played between 2 players. For the purpose of this task, let assume you play against the machine.

There are 3 simple rules to follow:

```
a) You have 12 tokens
b) Each player can pick 1, 2 or 3 tokens at a time
c) The player who picks the last token wins the game
```

### Solution

[GitHub Link](https://github.com/manwar/perlweeklychallenge-club/blob/master/challenge-104/aaronreidsmith/raku/ch-2.raku)

See below for explanation and any implementation-specific comments.

```
# Formats a message defined as plural to be singular if $n == 1
sub format(Str $message, Int $n) returns Str {
    $n == 1 ?? $message.trans(['are', 'tokens'] => ['is', 'token']) !! $message; # [1]
}

sub challenge(Int $n) {
    my $remaining = $n;

    # Defined within the challenge sub because it references $remaining
    sub default-prompt returns Any {
        prompt(format("There are $remaining tokens. How many would you like to pick up? (1, 2, 3) ", $remaining)); # [2]
    }

    my $input = default-prompt;
    my $most-recent-move;
    while $remaining > 0 {
        given $input {
            when 1|2|3 {
                if $input > $remaining {
                    $input = prompt("There are only $remaining tokens left. Please enter a valid number ")
                } else {
                    say format("You take $input tokens", $input);
                    $remaining -= $input;
                    $most-recent-move = 'You';

                    last if $remaining == 0;

                    # If there are only 3 or less tokens, take all of them. Otherwise, take a random number between 1 and 3
                    my $bot-move = $remaining ~~ 1|2|3 ?? $remaining !! (1..3).pick;
                    say format("The computer takes $bot-move tokens", $bot-move);
                    $remaining -= $bot-move;
                    $most-recent-move = 'Computer';

                    last if $remaining == 0;

                    $input = default-prompt;
                }
            }
            default { $input = prompt('Please enter 1, 2, or 3 ') }
        }
    }
    say $most-recent-move eq 'Computer' ?? 'The computer wins!' !! 'You win!'; # [3]
}

sub MAIN(Int $n where $n > 0 = 12) { # [4]
    challenge($n);
}
```

This program runs as such:

```
$ raku ch-2.raku
There are 12 tokens. How many would you like to pick up? (1, 2, 3) 3
You take 3 tokens
The computer takes 3 tokens
There are 6 tokens. How many would you like to pick up? (1, 2, 3) 2
You take 2 tokens
The computer takes 3 tokens
There is 1 token. How many would you like to pick up? (1, 2, 3) 1
You take 1 token
You win!
```

### Explanation

This task is basically an exercise in IO (`prompt`) and data validation (did I get what I expect?). We follow the following steps:

1. Ask the user to give us a number (1, 2, or 3).
    - Did they give it to us? Move on to step 2.
    - Otherwise, keep asking for a valid input (doesn't matter if they gave us an invalid number, a string, etc.).
2. Do a special check to see if their number is higher than the remaining tokens (only happens when there are 3 or fewer tokens). If so, keep prompting them for a valid input.
3. Now that we know we have valid input, decrement `$remaining` to reflect the number of token the user took.
4. If there are 0 tokens left, exit the loop and print that the user won.
5. Otherwise, there are tokens left, and it is the computer's turn. Our bot is semi-smart, so if there are 3 or fewer tokens take all of them (and win). Otherwise, take a random valid number of tokens.
6. If there are 0 tokens left, exit the loop and print that th computer won.
7. Finally, if there are still tokens left, repeat steps 1-6 until there are 0 tokens left.

#### Specific Comments

1. This is simply a helper function, so we can write all of our prompts like `"There are $n tokens remaining"` and they will get properly formatted if `$n` is 1. This is very specific to this question, obviously, but it is useful. `trans` basically just translates all `are` instances to `is` and all `tokens` instances to `token`.
2. You'll notice a few things about this subroutine. First, we don't have to define it with parentheses if it doesn't take any arguments. Second, it returns `Any` because we don't know what we are going to get from the user. Third, it is defined _inside_ `challenge` because it is acting as a [closure](https://simple.wikipedia.org/wiki/Closure_(computer_science)), meaning it references variables defined outside itself (in this case, `$remaining`).
3. Raku is kind of strange in that if you want to do string equality you have to use `eq` instead of `==`.
4. This function signature specifies that it takes an `Int` that is greater than 0, and if it is not provided, it defaults to 12.

## Final Thoughts

Raku gives us some cool tools to make these challenges easier. The `given` syntax was especially helpful in both of these challenges (and in others)! 
