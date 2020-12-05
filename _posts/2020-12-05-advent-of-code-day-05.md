---
title: "Advent of Code: Day 5"
categories:
  - Blog
tags:
  - Advent of Code
  - Raku
---

[Binary search](https://en.wikipedia.org/wiki/Binary_search_algorithm) is a well-known algorithm for searching already sorted lists. I liken it to searching for a book at a book store. If the author's last name starts with "S," you will start somewhere on the right-hand side of the shelf, then narrow down your search from there. This is obviously more efficient than searching from the left-hand side of the bookshelf.

That was our task with today's problem. Yet again, we get to bust out our old friend recursion to solve this problem fairly easily in a functional manner. 


## The Problem

### Part 1

After [yesterday's fiasco](https://aaronreidsmith.github.io/blog/advent-of-code-day-04/) of just getting through the airport, we find ourselves on the plane. Lo and behold, we dropped our boarding pass, but they still let us on the plane with the holiday rush.

Luckily, we use our phone to scan _all_ the boarding passes nearby into a file full of lines that look like this:

```
FBFBBFFRLR
```

The first seven characters define what row (0 through 127, inclusive) everyone's seat is in, and the last three characters refer to that seat's column (0 through 7, inclusive). For example, given the above input:

- Start by considering the whole range, rows 0 through 127
- F means to take the lower half, keeping rows 0 through 63
- B means to take the upper half, keeping rows 32 through 63
- F means to take the lower half, keeping rows 32 through 47
- B means to take the upper half, keeping rows 40 through 47
- B keeps rows 44 through 47
- F keeps rows 44 through 45
- The final F keeps the lower of the two, row 44

Similarly, for the columns:

- Start by considering the whole range, columns 0 through 7
- R means to take the upper half, keeping columns 4 through 7
- L means to take the lower half, keeping columns 4 through 5
- The final R keeps the upper of the two, column 5

And finally, to find someone's seat number, we have the following calculation:

```
(row_number * seats_in_row) + column_number = seat_number
```

Which yields:

```
(44 * 8) + 5 = 357
```

Our task is to find the maximum seat number in the list of scanned boarding passes.


#### Solution

[GitHub Link](https://github.com/aaronreidsmith/advent-of-code/blob/main/2020/05/raku/main.raku)

See below for explanation and any implementation-specific comments.

```
sub binary-search(@list, @possible-rows, $lower-symbol) {
    if @possible-rows.elems == 1 {
        @possible-rows.head;
    } else {
        my ($first-item, @rest-of-list) := @list[0,1..*];                                  # [1][2]
        my $half-way-point = @possible-rows.elems div 2;                                   # [3]
        if $first-item eq $lower-symbol {                                                  # [4]
            binary-search(@rest-of-list, @possible-rows[^$half-way-point], $lower-symbol); # [5]
        } else {
            binary-search(@rest-of-list, @possible-rows[$half-way-point..*], $lower-symbol);
        }
    }
}

sub find-seat($boarding-pass) {
    my (@row-definition, @column-definition) := $boarding-pass.comb.rotor(7, :partial); # [6]
    my $row = binary-search(@row-definition, (^128), 'F');
    my $column = binary-search(@column-definition, (^8), 'L');
    ($row * 8) + $column;
}

sub MAIN($file) {
    say $file.IO.lines.map(&find-seat).max;
}
```

This runs as such:

```
$ raku main.raku input.txt
828
```

#### Explanation

The `binary-search` subroutine itself is fairly straight forward. It takes the list of characters (something like `(F, B, F, B, B, F, F)`), the list of possible rows/columns (something like `(0..127)`), and what character means "lower half" (`F` for front or `L` for left).

If there is only one item in the list of remaining rows/columns, that's our answer, and we return. Otherwise, we check if we are keeping the left half or right half and call the function again with the smaller input.

We wrap this function in a helper function called `find-seat` which includes the multiplication logic, then map it over our input lines. Finally, we call `max` to find the max seat number.

##### Specific Comments

1. When unpacking a list in this manner, the left-hand side is normally one or more scalars (denoted by the `$` sigil). When unpacking using a list on the left-hand side, we have to use the special [binding](https://docs.raku.org/language/operators#index-entry-Binding_operator) operator (`:=`) or everything will get "slurped" (Raku's terminology, not mine) into the list instead of being split between the list and scalar.
2. I used some special Hash syntax yesterday to extract multiple keys at the same time. This is the equivalent List syntax (comma-separated instead of space-separated).
3. `div` is Raku's integer division operator. Even though we know our input will always be a multiple of two, it never hurts to use best practices!
4. In the past few posts for string comparison I was using `$x cmp $y == Same`. I finally stumbled upon the `eq` operator and no longer have that code smell!
5. This line (and others) contain special range syntax. Basically `^$half-way-point` is the same as `(0..^$half-way-point)`, meaning everything from zero to the half-way point, exclusive.
6. This line splits the input into a list of characters and then uses the `rotor` function to split it into groups of 7. Since our second group (the column definition) is of size 3, we need to pass the `:partial` parameter in, or else it will get dropped for being too small. `:partial` is special syntax to pass in a boolean flag named `partial` as true. This is the equivalent of passing in `partial => True`

### Part 2

Now that we've found the maximum seat, the flight attendants are asking us to take our seat! Our seat is the only seat number not in the list of boarding passes we scanned. And of course instead of just looking around the plane and finding the empty seat, we sit in the aisle and tweak our program to tell us where to go.

As a caveat, the seat numbers do _not_ start at 1, so we have to take that into consideration.

#### Solution

[GitHub Link](https://github.com/aaronreidsmith/advent-of-code/blob/main/2020/05/raku/main.raku)

See below for explanation and any implementation-specific comments.

```
sub binary-search(@list, @possible-rows, $lower-symbol) {
    if @possible-rows.elems == 1 {
        @possible-rows.head;
    } else {
        my ($first-item, @rest-of-list) := @list[0,1..*];
        my $half-way-point = @possible-rows.elems div 2;
        if $first-item eq $lower-symbol {
            binary-search(@rest-of-list, @possible-rows[^$half-way-point], $lower-symbol);
        } else {
            binary-search(@rest-of-list, @possible-rows[$half-way-point..*], $lower-symbol);
        }
    }
}

sub find-seat($boarding-pass) {
    my (@row-definition, @column-definition) := $boarding-pass.comb.rotor(7, :partial);
    my $row = binary-search(@row-definition, (^128), 'F');
    my $column = binary-search(@column-definition, (^8), 'L');
    ($row * 8) + $column;
}

sub MAIN($file, Bool :$p2 = False) {
    my @seats =  $file.IO.lines.map(&find-seat);
    my $max-seat = @seats.max;
    if $p2 {
        my $min-seat = @seats.min;
        my $all-seats = set ($min-seat..$max-seat);
        my @missing-seats = ($all-seats ⊖ set @seats).keys; # [1]
        say @missing-seats.head;
    } else {
        say $max-seat;
    }
}
```

This runs as such:

```
# Part 1
$ raku main.raku input.txt
828

# Part 2
$ raku main.raku --p2 input.txt
565
```

#### Explanation

You'll notice all we did was tweak our `MAIN` method a bit. We still find all the seat numbers, and if the user doesn't specify `p2`, we print the maximum.

If the user _does_ specify `p2`, we also calculate our minimum seat number (since the seats don't start at 1). We then find the set of _all_ seats (being the range from `$min-seat` to `$max-seat`). We then use our handy dandy [symmetric difference](https://en.wikipedia.org/wiki/Symmetric_difference) operator to find the difference between all possible seats, and the list of seats we scanned. The difference, of course, being our seat. We find it just in time before the flight attendants drag us out. Phew!

##### Specific Comments

1. A set is a scalar instead of a collection in Raku (note the `$` sigil instead of the `@` sigil), so we have to convert it to a list using the `.keys` method. Of course, there is only one thing in it, so we then call `.head` to get that item.


## Final Thoughts

This exercise has me diving more and more into [set theory](https://en.wikipedia.org/wiki/Set_theory). It's awesome that Raku allows (and encourages) use of the Unicode operators found in math textbooks. Their reasoning for this is that it is easier to take an algorithm from paper to code when you are allowed to use the same notation in each place. Now to find a keyboard to be able to type these symbols!

So far we are 5 for 5 with pure functional solutions. 20% of the way there!