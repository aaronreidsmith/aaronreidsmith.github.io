---
title: "Advent of Code: Day 21"
categories:
  - Blog
tags:
  - Advent of Code
  - Raku
---

I had much more fun with today's puzzle than yesterday's! We are back in Raku, after a few days of detouring through Python.

## The Problem

### Part 1

We are trying to buy some snacks for the last leg of our journey, but we don't speak the local language. Luckily, the allergen information is in English. We have a list of foods that looks like the following, where each line contains a list of ingredients in the foreign language followed by the allergens in English:

```
mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)
```

This list has a caveat to it -- allergens are not always listed for each food. So we first have to figure out which ingredient _can't_ contain an allergen. In the above example it would be `kfcds`, `nhms`, `sbzzf`, and `trh`. We then want to count how many times those ingredients occur (in the above example it would be `5`). What is the count of non-allergen ingredients in the real input?

#### Solution

[GitHub Link](https://github.com/aaronreidsmith/advent-of-code/blob/main/2020/21/raku/main.raku)

See below for explanation and any implementation-specific comments.

```
sub MAIN($file) {
    my @rules = $file.IO.lines.map(-> $line {
        my ($ingredients-str, $allergens-str) = $line.split(' (contains ');
        my @ingredients = $ingredients-str.split(' ');
        my @allergens = $allergens-str.substr(0, *-1).split(', ');
        { :@ingredients, :@allergens };
    });
    my $all-allergens = @rules.map(-> %rule { |%rule<allergens> }).Set;

    my %candidates = $all-allergens.keys.map(-> $allergen {
        $allergen => [∩] @rules.grep(*<allergens> ∋ $allergen).map(*<ingredients>); # [1]
    });

    my (%mapping, @mapped);
    while %mapping.elems < $all-allergens.elems {
        for %candidates.kv -> $allergen, $ingredients {
            if $ingredients.keys.elems == 1 {
                %mapping{$allergen} = $ingredients.keys.head;
                @mapped.push(%mapping{$allergen});
                %candidates{$allergen}:delete;
            }
            %candidates{$allergen} ∖= @mapped; # [2]
        }
    }

    say @rules.map((*<ingredients> ∖ @mapped).elems).sum;
}
```

This runs as such:

```
$ raku main.raku input.txt
2061
```

#### Explanation

We spend the first few lines getting our data into this structure (using the example data):

```
[
  {allergens => [dairy fish], ingredients => [mxmxvkd kfcds sqjhc nhms]},
  {allergens => [dairy], ingredients => [trh fvjkl sbzzf mxmxvkd]},
  {allergens => [soy], ingredients => [sqjhc fvjkl]},
  {allergens => [fish], ingredients => [sqjhc mxmxvkd sbzzf]}
]
```

Which is, of course, a list of `Hash` objects containing the ingredient and allergen information. We then create a `Set` of all possible allergens (in this case `Set(dairy fish soy)`).

Next, looking at the ingredients in comparison to the allergens set, we construct an object containing the allergens with their possible ingredients that looks like this:

```
{dairy => Set(mxmxvkd), fish => Set(mxmxvkd sqjhc), soy => Set(fvjkl sqjhc)}
```

After we have that, we loop through each candidate pair and see if the `Set` is exactly 1 item. If it is, we moved that pair to the `%mapping` `Hash` and the value to the `@mapped` list and remove the candidate from the other sets. Here is how it would look for each loop:

```
# Start
%mapping    = {}
@mapped     = ()
%candidates = {dairy => Set(mxmxvkd), fish => Set(mxmxvkd sqjhc), soy => Set(fvjkl sqjhc)}

# Loop 1
%mapping    = {dairy => mxmxvkd}
@mapped     = (mxmxvkd)
%candidates = {fish => Set(sqjhc), soy => Set(fvjkl sqjhc)}

# Loop 2
%mapping    = {dairy => mxmxvkd, fish => sqjhc}
@mapped     = (mxmxvkd, sqjhc)
%candidates = {soy => Set(fvjkl)}

# Loop 3
%mapping    = {dairy => mxmxvkd, fish => sqjhc, soy => fvjkl}
@mapped     = (mxmxvkd, sqjhc, fvjkl)
%candidates = {}
```

Finally, for each food we take the set disjunction `∖` of the ingredients list and the known allergens (leaving the non-allergens), then sum the counts!

##### Specific Comments

1. A few set operators in this line: `∋` is the reverse of the other operator I use of (`∈`). The latter reads `x is an element of y`, while the former reads `set y contains element x`. When I use the `Whatever` star, I like it to be on the left, so that is the reason for using it here. Additionally, we use the set intersection reduction operator (`[∩]`) which finds the overlapping regions of the input allergen lists and converts them to a single set.
2. This is also a new one, it is the set difference operator, aka the [relative complement](https://en.wikipedia.org/wiki/Complement_(set_theory)#Relative_complement) operator. It's used to remove the already-mapped elements from the candidate sets.

### Part 2

Now that we have isolated the safe ingredients, we should have enough information to generate a list of dangerous ingredients. We need to generate a comma-separated list order alphabetically _by allergen_ name. For the above example it would look like this:

```
mxmxvkd,sqjhc,fvjkl
```

What is the allergen list for our real input?

#### Solution

[GitHub Link](https://github.com/aaronreidsmith/advent-of-code/blob/main/2020/21/raku/main.raku)

See below for explanation and any implementation-specific comments.

```
sub MAIN($file, Bool :$p2 = False) {
    my @rules = $file.IO.lines.map(-> $line {
        my ($ingredients-str, $allergens-str) = $line.split(' (contains ');
        my @ingredients = $ingredients-str.split(' ');
        my @allergens = $allergens-str.substr(0, *-1).split(', ');
        { :@ingredients, :@allergens };
    });
    my $all-allergens = @rules.map(-> %rule { |%rule<allergens> }).Set;

    my %candidates = $all-allergens.keys.map(-> $allergen {
        $allergen => [∩] @rules.grep(*<allergens> ∋ $allergen).map(*<ingredients>);
    });

    my (%mapping, @mapped);
    while %mapping.elems < $all-allergens.elems {
        for %candidates.kv -> $allergen, $ingredients {
            if $ingredients.keys.elems == 1 {
                %mapping{$allergen} = $ingredients.keys.head;
                @mapped.push(%mapping{$allergen});
                %candidates{$allergen}:delete;
            }
            %candidates{$allergen} ∖= @mapped;
        }
    }

    if $p2 {
        say %mapping.sort.map(*.value).join(',');
    } else {
        say @rules.map((*<ingredients> ∖ @mapped).elems).sum;
    }
}
```

This runs as such:

```
$ raku main.raku input.txt
2061

$ raku main.raku --p2 input.txt
cdqvp,dglm,zhqjs,rbpg,xvtrfz,tgmzqjz,mfqgx,rffqhl
```

#### Explanation

We basically already did this for part one, so all that changes is the last section.

We have our `%mapping` hash which we then sort (by default it uses the key, which is our allergen), then we extract just the values, and finally join them into a comma-separated list.

## Final Thoughts

Well, at least the creator of AoC is true to his word that weekday puzzles are easier. 🙂 This was a fun little one and puts us at 84% of the way there! 
