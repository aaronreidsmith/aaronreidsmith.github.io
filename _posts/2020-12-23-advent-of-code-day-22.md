---
title: "Advent of Code: Day 22"
categories:
  - Blog
tags:
  - Advent of Code
  - Raku
  - Python
---

I am posting day 22's blog a day late due to an outage at work that took precedence. However, you can see from my [git history](https://github.com/aaronreidsmith/advent-of-code/commit/0f0559fb30044848b0985e732497dc6674798158) that the code itself was written on the 22nd.

I solved the first half of the problem in Raku and then _tried_ to write the second half in Raku but got stuck, so this is the first problem where each half was solved. in a different language.

## The Problem

### Part 1

Our last mode of transportation is a raft and are bored out of our minds. There is a little crab on our raft, and we decide to play a class game of [War](https://bicyclecards.com/how-to-play/war/).

The rules are simple:

- Each player has a deck of cards (the decks do not have any duplicate values).
- Each turn each player reveals the top card in their deck. Whomever's is bigger wins the round and puts both cards on the bottom of their deck, with the bigger card on top.
- When one player gets _all_ the cards in their deck, that player wins

Here is an example:

```
-- Round 1 --
Player 1's deck: 9, 2, 6, 3, 1
Player 2's deck: 5, 8, 4, 7, 10
Player 1 plays: 9
Player 2 plays: 5
Player 1 wins the round!

-- Round 2 --
Player 1's deck: 2, 6, 3, 1, 9, 5
Player 2's deck: 8, 4, 7, 10
Player 1 plays: 2
Player 2 plays: 8
Player 2 wins the round!

-- Round 3 --
Player 1's deck: 6, 3, 1, 9, 5
Player 2's deck: 4, 7, 10, 8, 2
Player 1 plays: 6
Player 2 plays: 4
Player 1 wins the round!

-- Round 4 --
Player 1's deck: 3, 1, 9, 5, 6, 4
Player 2's deck: 7, 10, 8, 2
Player 1 plays: 3
Player 2 plays: 7
Player 2 wins the round!

-- Round 5 --
Player 1's deck: 1, 9, 5, 6, 4
Player 2's deck: 10, 8, 2, 7, 3
Player 1 plays: 1
Player 2 plays: 10
Player 2 wins the round!

...several more rounds pass...

-- Round 27 --
Player 1's deck: 5, 4, 1
Player 2's deck: 8, 9, 7, 3, 2, 10, 6
Player 1 plays: 5
Player 2 plays: 8
Player 2 wins the round!

-- Round 28 --
Player 1's deck: 4, 1
Player 2's deck: 9, 7, 3, 2, 10, 6, 8, 5
Player 1 plays: 4
Player 2 plays: 9
Player 2 wins the round!

-- Round 29 --
Player 1's deck: 1
Player 2's deck: 7, 3, 2, 10, 6, 8, 5, 9, 4
Player 1 plays: 1
Player 2 plays: 7
Player 2 wins the round!


== Post-game results ==
Player 1's deck: 
Player 2's deck: 3, 2, 10, 6, 8, 5, 9, 4, 7, 1
```

When we get to the end, we can calculate the winning player's score like this, here each position's value is its card value multiplied by its position from the bottom of the deck:

```
   3 * 10
+  2 *  9
+ 10 *  8
+  6 *  7
+  8 *  6
+  5 *  5
+  9 *  4
+  4 *  3
+  7 *  2
+  1 *  1
= 306
```

What is the winning player's score with the actual input?

#### Solution

[GitHub Link](https://github.com/aaronreidsmith/advent-of-code/blob/main/2020/22/raku/main.raku)

See below for explanation and any implementation-specific comments.

```
sub calculate-score(@deck) {
    @deck.reverse.kv.map(-> $index, $value { ($index + 1) * $value }).sum;
}

sub play-game(@player1, @player2) {
    if @player1.elems == 0 {
        calculate-score(@player2);
    } elsif @player2.elems == 0 {
        calculate-score(@player1);
    } else {
        my $player1-card = @player1.head;
        my $player2-card = @player2.head;
        if $player1-card > $player2-card {
            play-game(
                (|@player1[1..*], $player1-card, $player2-card),
                @player2[1..*]
            );
        } else {
            play-game(
                @player1[1..*],
                (|@player2[1..*], $player2-card, $player1-card)
            );
        }
    }
}

sub MAIN($file) {
    my ($player1-str, $player2-str) = $file.IO.lines(:nl-in("\n\n"));
    my @player1 = $player1-str.lines[1..*].map(*.Int);
    my @player2 = $player2-str.lines[1..*].map(*.Int);
    say play-game(@player1, @player2);
}
```

This runs as such:

```
$ raku main.raku input.txt
33400
```

#### Explanation

I guess it is worth saying that our input looks like this:

```
Player 1:
45
10
43
46
25
36
16
38
30
15
26
34
9
2
44
1
4
40
5
24
49
3
41
19
13

Player 2:
28
50
37
20
6
42
32
47
39
22
14
7
21
17
27
8
48
11
23
12
18
35
29
33
31
```

Most of the stuff that happens in `MAIN` is just parsing that into two lists of integers. We then pass those lists to `play-game`, which has very simple logic:

1. If one player has zero cards, return the score of the other player
2. Otherwise, pull their top cards and compare them. The player with the higher card put their card on the bottom of the deck _and then_ the loser's card on the bottom of their deck.
3. Play the game recursively until our end condition is met

Other than the main logic, our `calculate-score` does it's job by reversing the list then multiplying each item by `$index + 1` (since we measure distance from the bottom), then summing.

That's it!

### Part 2

Now we challenge the crab to a game of **Recursive War**. Recursive War is similar to regular War, with the following changes:

- Before either player deals a card, if there was a previous round in this game that had exactly the same cards in the same order in the same players' decks, the game instantly ends in a win for player 1. Previous rounds from other games are not considered. (This prevents infinite games of Recursive Combat, which everyone agrees is a bad idea.)
- Otherwise, this round's cards must be in a new configuration; the players begin the round by each drawing the top card of their deck as normal.
- If both players have at least as many cards remaining in their deck as the value of the card they just drew, the winner of the round is determined by playing a new game of Recursive Combat (see below).
- Otherwise, at least one player must not have enough cards left in their deck to recurse; the winner of the round is the player with the higher-value card.

To play a sub-game of Recursive Combat, each player creates a new deck by making a copy of the next cards in their deck (the quantity of cards copied is equal to the number on the card they drew to trigger the sub-game). During this sub-game, the game that triggered it is on hold and completely unaffected; no cards are removed from players' decks to form the sub-game. (For example, if player 1 drew the 3 card, their deck in the sub-game would be copies of the next three cards in their deck.)

Here is an example of a recursive combat game (sorry it's so long...):

```
=== Game 1 ===

-- Round 1 (Game 1) --
Player 1's deck: 9, 2, 6, 3, 1
Player 2's deck: 5, 8, 4, 7, 10
Player 1 plays: 9
Player 2 plays: 5
Player 1 wins round 1 of game 1!

-- Round 2 (Game 1) --
Player 1's deck: 2, 6, 3, 1, 9, 5
Player 2's deck: 8, 4, 7, 10
Player 1 plays: 2
Player 2 plays: 8
Player 2 wins round 2 of game 1!

-- Round 3 (Game 1) --
Player 1's deck: 6, 3, 1, 9, 5
Player 2's deck: 4, 7, 10, 8, 2
Player 1 plays: 6
Player 2 plays: 4
Player 1 wins round 3 of game 1!

-- Round 4 (Game 1) --
Player 1's deck: 3, 1, 9, 5, 6, 4
Player 2's deck: 7, 10, 8, 2
Player 1 plays: 3
Player 2 plays: 7
Player 2 wins round 4 of game 1!

-- Round 5 (Game 1) --
Player 1's deck: 1, 9, 5, 6, 4
Player 2's deck: 10, 8, 2, 7, 3
Player 1 plays: 1
Player 2 plays: 10
Player 2 wins round 5 of game 1!

-- Round 6 (Game 1) --
Player 1's deck: 9, 5, 6, 4
Player 2's deck: 8, 2, 7, 3, 10, 1
Player 1 plays: 9
Player 2 plays: 8
Player 1 wins round 6 of game 1!

-- Round 7 (Game 1) --
Player 1's deck: 5, 6, 4, 9, 8
Player 2's deck: 2, 7, 3, 10, 1
Player 1 plays: 5
Player 2 plays: 2
Player 1 wins round 7 of game 1!

-- Round 8 (Game 1) --
Player 1's deck: 6, 4, 9, 8, 5, 2
Player 2's deck: 7, 3, 10, 1
Player 1 plays: 6
Player 2 plays: 7
Player 2 wins round 8 of game 1!

-- Round 9 (Game 1) --
Player 1's deck: 4, 9, 8, 5, 2
Player 2's deck: 3, 10, 1, 7, 6
Player 1 plays: 4
Player 2 plays: 3
Playing a sub-game to determine the winner...

=== Game 2 ===

-- Round 1 (Game 2) --
Player 1's deck: 9, 8, 5, 2
Player 2's deck: 10, 1, 7
Player 1 plays: 9
Player 2 plays: 10
Player 2 wins round 1 of game 2!

-- Round 2 (Game 2) --
Player 1's deck: 8, 5, 2
Player 2's deck: 1, 7, 10, 9
Player 1 plays: 8
Player 2 plays: 1
Player 1 wins round 2 of game 2!

-- Round 3 (Game 2) --
Player 1's deck: 5, 2, 8, 1
Player 2's deck: 7, 10, 9
Player 1 plays: 5
Player 2 plays: 7
Player 2 wins round 3 of game 2!

-- Round 4 (Game 2) --
Player 1's deck: 2, 8, 1
Player 2's deck: 10, 9, 7, 5
Player 1 plays: 2
Player 2 plays: 10
Player 2 wins round 4 of game 2!

-- Round 5 (Game 2) --
Player 1's deck: 8, 1
Player 2's deck: 9, 7, 5, 10, 2
Player 1 plays: 8
Player 2 plays: 9
Player 2 wins round 5 of game 2!

-- Round 6 (Game 2) --
Player 1's deck: 1
Player 2's deck: 7, 5, 10, 2, 9, 8
Player 1 plays: 1
Player 2 plays: 7
Player 2 wins round 6 of game 2!
The winner of game 2 is player 2!

...anyway, back to game 1.
Player 2 wins round 9 of game 1!

-- Round 10 (Game 1) --
Player 1's deck: 9, 8, 5, 2
Player 2's deck: 10, 1, 7, 6, 3, 4
Player 1 plays: 9
Player 2 plays: 10
Player 2 wins round 10 of game 1!

-- Round 11 (Game 1) --
Player 1's deck: 8, 5, 2
Player 2's deck: 1, 7, 6, 3, 4, 10, 9
Player 1 plays: 8
Player 2 plays: 1
Player 1 wins round 11 of game 1!

-- Round 12 (Game 1) --
Player 1's deck: 5, 2, 8, 1
Player 2's deck: 7, 6, 3, 4, 10, 9
Player 1 plays: 5
Player 2 plays: 7
Player 2 wins round 12 of game 1!

-- Round 13 (Game 1) --
Player 1's deck: 2, 8, 1
Player 2's deck: 6, 3, 4, 10, 9, 7, 5
Player 1 plays: 2
Player 2 plays: 6
Playing a sub-game to determine the winner...

=== Game 3 ===

-- Round 1 (Game 3) --
Player 1's deck: 8, 1
Player 2's deck: 3, 4, 10, 9, 7, 5
Player 1 plays: 8
Player 2 plays: 3
Player 1 wins round 1 of game 3!

-- Round 2 (Game 3) --
Player 1's deck: 1, 8, 3
Player 2's deck: 4, 10, 9, 7, 5
Player 1 plays: 1
Player 2 plays: 4
Playing a sub-game to determine the winner...

=== Game 4 ===

-- Round 1 (Game 4) --
Player 1's deck: 8
Player 2's deck: 10, 9, 7, 5
Player 1 plays: 8
Player 2 plays: 10
Player 2 wins round 1 of game 4!
The winner of game 4 is player 2!

...anyway, back to game 3.
Player 2 wins round 2 of game 3!

-- Round 3 (Game 3) --
Player 1's deck: 8, 3
Player 2's deck: 10, 9, 7, 5, 4, 1
Player 1 plays: 8
Player 2 plays: 10
Player 2 wins round 3 of game 3!

-- Round 4 (Game 3) --
Player 1's deck: 3
Player 2's deck: 9, 7, 5, 4, 1, 10, 8
Player 1 plays: 3
Player 2 plays: 9
Player 2 wins round 4 of game 3!
The winner of game 3 is player 2!

...anyway, back to game 1.
Player 2 wins round 13 of game 1!

-- Round 14 (Game 1) --
Player 1's deck: 8, 1
Player 2's deck: 3, 4, 10, 9, 7, 5, 6, 2
Player 1 plays: 8
Player 2 plays: 3
Player 1 wins round 14 of game 1!

-- Round 15 (Game 1) --
Player 1's deck: 1, 8, 3
Player 2's deck: 4, 10, 9, 7, 5, 6, 2
Player 1 plays: 1
Player 2 plays: 4
Playing a sub-game to determine the winner...

=== Game 5 ===

-- Round 1 (Game 5) --
Player 1's deck: 8
Player 2's deck: 10, 9, 7, 5
Player 1 plays: 8
Player 2 plays: 10
Player 2 wins round 1 of game 5!
The winner of game 5 is player 2!

...anyway, back to game 1.
Player 2 wins round 15 of game 1!

-- Round 16 (Game 1) --
Player 1's deck: 8, 3
Player 2's deck: 10, 9, 7, 5, 6, 2, 4, 1
Player 1 plays: 8
Player 2 plays: 10
Player 2 wins round 16 of game 1!

-- Round 17 (Game 1) --
Player 1's deck: 3
Player 2's deck: 9, 7, 5, 6, 2, 4, 1, 10, 8
Player 1 plays: 3
Player 2 plays: 9
Player 2 wins round 17 of game 1!
The winner of game 1 is player 2!


== Post-game results ==
Player 1's deck: 
Player 2's deck: 7, 5, 6, 2, 4, 1, 10, 8, 9, 3
```

_Now_, what is the score of the winner?

#### Solution

[GitHub Link](https://github.com/aaronreidsmith/advent-of-code/blob/main/2020/22/python/main.py)

See below for explanation and any implementation-specific comments.

```python
import sys


def calculate_score(deck):
    return sum([(idx + 1) * value for idx, value in enumerate(deck[::-1])])


def play_game(player1, player2):
    seen = set()

    while player1 and player2:
        key = (tuple(player1), tuple(player2))
        if key in seen:
            return player1, []
        else:
            seen.add(key)

        p1_card, player1 = player1[0], player1[1:]
        p2_card, player2 = player2[0], player2[1:]
        if p1_card <= len(player1) and p2_card <= len(player2):
            player1_prime = player1[:p1_card]
            player2_prime = player2[:p2_card]
            player1_prime, player2_prime = play_game(player1_prime, player2_prime)
            if len(player1_prime) > len(player2_prime):
                player1.extend([p1_card, p2_card])
            else:
                player2.extend([p2_card, p1_card])
        elif p1_card > p2_card:
            player1.extend([p1_card, p2_card])
        else:
            player2.extend([p2_card, p1_card])

    return player1, player2


if __name__ == '__main__':
    with open(sys.argv[1]) as file:
        p1_string, p2_string = file.read().split('\n\n')
        player1 = [int(line) for line in p1_string.split('\n')[1:]]
        player2 = [int(line) for line in p2_string.split('\n')[1:]]

    p1, p2 = play_game(player1, player2)
    print(calculate_score(p1 + p2))
```

This runs as such:

```
$ python main.py input.txt
33745
```

#### Explanation

The `__main__` and `calculate_score` functions are the same as their Raku counterparts; what changed here was `play_game`. We basically follow the following logic:

- If we have seen this orientation (in this game or sub-game), player 1 wins immediately
- Otherwise, we draw our cards
- If we have both enough cards for a sub game ("enough" is an amount greater than the card we drew), then play a sub-game to determine the winner
- Once the winner is determined (either through a sub game or just comparing cards), add the cards to the bottom of the winner's deck as normal.
- Repeat until one player has all the cards!

## Final Thoughts

I wrote part one at 6am and wrote part two around 10pm yesterday. I probably could have gotten it working in Raku, but I was hoping to do a puzzle a day for the duration of AoC, so I had to do what I had to do. Hopefully I will get back on track today and finish out the week (and the month) strong!
