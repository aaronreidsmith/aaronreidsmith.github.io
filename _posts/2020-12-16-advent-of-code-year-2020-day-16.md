---
title: "Advent of Code: Year 2020, Day 16"
categories:
  - Blog
tags:
  - Advent of Code
  - Raku
---

We got to explore some cool features of Raku today, even if it wasn't 100% functional. 🙂 Read on to see what I am talking about! 

## The Problem

### Part 1

Going through our itinerary for our re-routed leg, we realize we are going to end up on a train in a country where we don't speak the language! Luckily, we were able to scan all the train tickets around us to give us input that looks something like the following:

```
class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12
```

Where each ticket column corresponds to _a_ field in the first section, but we don't know which one. Our first job is simply to find the _error rate_ in the tickets. That is, find each ticket that is invalid (where one field is not in _any_ of the valid ranges), and then find the sum of the invalid fields.

#### Solution

[GitHub Link](https://github.com/aaronreidsmith/advent-of-code/blob/103fedb13cd88b0e852caed8a1ff951d84bffdac/src/main/raku/2020/day-16.raku)

See below for explanation and any implementation-specific comments.

```
sub parse-input($file) {
    my ($train-text, $my-ticket, $other-tickets) = $file.IO.lines(:nl-in("\n\n"));

    # Turn train ranges into Junctions of Range objects
    my @train-info = $train-text.lines.map(-> $line {
        my $range-text = $line.split(': ')[1];
        my @ranges = $range-text.split(' or ').map(-> $range { $range.split('-').map(*.Int).minmax }); # [1]
        Junction.new(@ranges, type => 'any');                                                          # [2]
    });

    # Map the tickets into lists of integers
    my @my-info = $my-ticket.lines[1].split(',').map(*.Int);
    my @other-info = $other-tickets.lines[1..*].map(-> $line { $line.split(',').map(*.Int) });

    (@train-info, @my-info, @other-info)
}

sub find-invalid-rate(@train-info, @tickets) {
    my @invalid = gather {
        for @tickets -> @ticket {
            for @ticket -> $field {
                if $field ∈ any(@train-info) {
                    next;                      # [3]
                } else {
                    take $field;
                    last;                      # [4]
                }
            }
        }
    }
    @invalid.sum;
}

sub MAIN($file) {
    my (@train-info, @my-ticket, @other-tickets) := parse-input($file);
    my @all-tickets = (@my-ticket, |@other-tickets);
    say find-invalid-rate(@train-info, @all-tickets);
}
```

This runs as such:

```
$ raku day-16.raku input.txt
20091
```

#### Explanation

I felt the parse step in and of itself was complex enough to warrant its own subroutine today, so you'll see our first step is `parse-input`. This will return a list of valid ranges, a list representing our ticket, and a list of the scanned tickets nearby. We then take that data and pass it to `find-invalid-rate`, which will iterate through each ticket and checks if each field is in _any_ valid range. Finally, it sums the invalid fields it finds.

That's it!

##### Specific Comments

1. Once we've parsed the input for train information we end up with a string like `100-150`, which we then turn into a list like `(100, 150)`. Raku has a special `minmax` method which will make a range based on the min and max values of a list. So `(100, 150).minmax` becomes `(100..150)`.
2. Each ticket field has 2 valid ranges, so we turn them into a [`Junction`](https://docs.raku.org/type/Junction) that will basically return true if a value is in _either_ range.
3. `next` is similar to `continue` in other languages.
4. `last` is similar to `break` in other languages.

### Part 2

Now that we have found our invalid tickets, we need to disregard them entirely. Our next step is to take _only_ the other tickets we scanned and determine which column corresponds to which ticket field (it will be the same column for each ticket). Once we have done that, we need to find the 6 fields starting with the word `departure` and find the product of their fields on _our_ ticket.

#### Solution

[GitHub Link](https://github.com/aaronreidsmith/advent-of-code/blob/103fedb13cd88b0e852caed8a1ff951d84bffdac/src/main/raku/2020/day-16.raku)

See below for explanation and any implementation-specific comments.

```
sub parse-input($file) {
    my ($train-text, $my-ticket, $other-tickets) = $file.IO.lines(:nl-in("\n\n"));

    # Turn train ranges into Junctions of Range objects
    my %train-info = $train-text.lines.map(-> $line {
        my ($range-name, $range-text) = $line.split(': ');
        my @ranges = $range-text.split(' or ').map(-> $range { $range.split('-').map(*.Int).minmax });
        $range-name => Junction.new(@ranges, type => 'any');
    }).Hash;

    # Map the tickets into lists of integers
    my @my-info = $my-ticket.lines[1].split(',').map(*.Int);
    my @other-info = $other-tickets.lines[1..*].map(-> $line { $line.split(',').map(*.Int) });

    (%train-info, @my-info, @other-info)
}

sub is-valid(@train-info, @ticket) {
    so all(@ticket) ∈ any(@train-info); # [1]
}

sub find-invalid-field(@train-info, @ticket) {
    for @ticket -> $field {
        if $field ∈ any(@train-info) {
            next;
        } else {
            return $field;
        }
    }
}

sub find-invalid-rate(@train-info, @tickets) {
    my @invalid = gather {
        for @tickets -> @ticket {
            if !is-valid(@train-info, @ticket) {
                take find-invalid-field(@train-info, @ticket);
            }
        }
    }
    @invalid.sum;
}

sub find-field-indices(%train-info, @fields) {
    # Given the size of our input ranges, some of our fields may fit into more than one category,
    # so we have to find all possible categories
    my %possible-fields;
    for @fields.kv -> $index, @field {
        for %train-info.kv -> $name, $range {
            if ?(all(@field) ∈ $range) {            # [2]
                if %possible-fields{$name}:exists {
                    %possible-fields{$name} = (|%possible-fields{$name}, $index);
                } else {
                    %possible-fields{$name} = ($index,);
                }
            }
        }
    }

    my $number-of-fields = %possible-fields.elems;

    # We assume at least one of the above fields fits into exactly one category, so we look for
    # that item and then remove that index from the rest of the fields' categories and keep keep
    # looping until we have $number-of-fields defined
    my %final-fields;
    while %final-fields.elems != $number-of-fields {
        for %possible-fields.kv -> $name, @possible-indices {
            if @possible-indices.elems == 1 {
                my $index = @possible-indices.head;
                %final-fields{$name} = $index;
                %possible-fields{$name}:delete;
                for %possible-fields.kv -> $name-to-update, @indices-to-update {
                    %possible-fields{$name-to-update} = @indices-to-update.grep(* != $index);
                }
            }
        }
    }
    %final-fields;
}

sub MAIN($file, Bool :$p2 = False) {
    my (%train-info, @my-ticket, @other-tickets) := parse-input($file);
    my @all-tickets = (@my-ticket, |@other-tickets);
    if $p2 {
        my @valid-tickets = @other-tickets.grep(&is-valid.assuming(%train-info.values, *));
        my @fields = [Z] @valid-tickets;
        my %field-indices = find-field-indices(%train-info, @fields);
        my @departure-fields = gather {
            for %field-indices.kv -> $name, $index {
                if $name.starts-with('departure') {
                    take @my-ticket[$index];
                }
            }
        }
        say [*] @departure-fields;
    } else {
        say find-invalid-rate(%train-info.values, @all-tickets);
    }
}
```

This runs as such:

```
# Part 1
$ raku day-16.raku input.txt
20091

# Part 2
$ raku day-16.raku --p2 input.txt
2325343130651
```

#### Explanation

I tried to make `MAIN` as clear as possible here. You'll notice `train-info` is now `Hash` so that we can access each range's name as well. If it is part two we first filter down valid tickets using the logic above, then we pivot that into rows of _fields_ instead of rows of _tickets_, and we calculate the indices that correspond to each train ticket field. Finally, we take the six fields that start with `departure` and multiple them together!

As far as implementation, we split out the logic from part one into `is-valid` and `find-invalid-field`, the former of which is used in part two. `find-field-indices` first finds all possible columns that correspond to a given range, then filters them down one-by-one until we have determined definitively which column corresponds to which ticket field. 

##### Specific Comments

1. This line is just a bunch of junctions, but I feel it reads very well. We are checking if _all_ of the fields in this ticket match _any_ of the pairs of ranges that we have parsed out. As an aside, `so` is the way to cast the junction of booleans to a single boolean.
2. This line is similar -- we are checking if _all_ of the values in this field are in the supplied range pair. `?` _also_ casts the line to a boolean value.

## Final Thoughts

Not super happy with the overall complexity of this solution -- most subroutines use some form of a nested loop yielding O(n²) complexity. It works for our small data, but it certainly does not scale well. Regardless, we made it through and are almost ⅔ of the way done!
