---
title: "Advent of Code: Day 4"
categories:
  - Blog
tags:
  - Advent of Code
  - Raku
---

Today's challenge was a rough one for me. Not because of the challenge itself, but because I fell into a trap in the Raku language that was giving me an off-by-one error. See Part 2 for details!


## The Problem

### Part 1

This problem may require a little more back-story than my previous posts.

We're traveling for the holidays, but realized we forgot our passport! Luckily, we have our North Pole Credentials that have all the same information except Country ID (you know, the thing that makes a passport useful). A passport contains the following fields:

```
byr (Birth Year)
iyr (Issue Year)
eyr (Expiration Year)
hgt (Height)
hcl (Hair Color)
ecl (Eye Color)
pid (Passport ID)
cid (Country ID
```

Unfortunately we are stuck in a long line because the passport scanner is down. Apparently it is having trouble detecting which passports have all the required fields. We're nice folks though, so we're going to offer our skills up to the border agents to fix their passport scanner (and maybe we can slip in a "bug" to ignore the fact that we don't have a passport?).

We are given a batch file of passport information as our input. Each passport is separated by a blank line, and each item in the passport is separated by either a newline or a space. Example:

```
ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in
```

- Passport 1 is valid because it has all required fields
- Passport 2 is invalid because it is missing the `hgt` field
- Passport 3 is "valid" because it contains everything but `cid`
- Passport 4 is invalid because it is missing both the `cid` and `byr` fields

Our job is to find how many passports are either valid or "valid"


#### Solution

[GitHub Link](https://github.com/aaronreidsmith/advent-of-code/blob/main/2020/04/raku/main.raku)

See below for explanation and any implementation specific comments.

```
sub is-valid(%credentials) {
    my $passport-keys = set <byr iyr eyr hgt hcl ecl pid cid>;   # [1]
    my $north-pole-credentials = $passport-keys ⊖ 'cid';         # [2]

    my $keys = set %credentials.keys;

    $keys ~~ $passport-keys || $keys ~~ $north-pole-credentials; # [3]
}

sub MAIN($file) {
    say $file.IO
          .slurp
          .split(/\n\n/)
          .map(-> $entry {
              $entry
                .split(/<space>/)
                .map(*.split(':'))
                .map(-> ($key, $value) { $key.trim => $value.trim })
                .Hash
          })
          .map(&is-valid)
          .grep(* == True)
          .elems;
}
```

This runs as such:

```
$ raku main.raku input.txt
237
```

#### Explanation

The hardest part to step one was getting our data out of the batch file and into a data structure (in this case, a list of hashes). You'll notice this time we use `IO.slurp` instead of `IO.lines` to pull all the data into one string to manipulate it ourselves. Once we have the file as a string, we apply the following steps:

1. Split the data on 2 newlines (aka, a blank line between entries)
2. Then for each passport entry split on the the [`<space>`](https://docs.raku.org/language/regexes#Predefined_character_classes) character (which is an alias for `\s`), giving us an inner list containing colon-separated key-value pairs
3. For each key-value pair, we split on the comma
4. We then take all our pairs and turn them into actual [Pair](https://docs.raku.org/type/Pair) objects
5. We use the Pair objects as an interim to convert each entry to a [Hash](https://docs.raku.org/type/Hash)

At this point, our sample input above would look something like this:

```
(
  {byr => 1937, cid => 147, ecl => gry, eyr => 2020, hcl => #fffffd, hgt => 183cm, iyr => 2017, pid => 860033327},
  {byr => 1929, cid => 350, ecl => amb, eyr => 2023, hcl => #cfa07d, iyr => 2013, pid => 028048884},
  {byr => 1931, ecl => brn, eyr => 2024, hcl => #ae17e1, hgt => 179cm, iyr => 2013, pid => 760753108},
  {ecl => brn, eyr => 2025, hcl => #cfa07d, hgt => 59in, iyr => 2011, pid => 166559648}
)
```

We then map our `is-valid` function over this list of hashes and count how many `True`s we get

##### Specific Comments

1. The `<...>` syntax is a special way of making a list of strings. It implicitly quotes each space-separated entry. We then cast this list to a set.
2. Raku is big on Unicode operators, and I try to use them where I can. In this case, we are using the [set difference](https://en.wikipedia.org/wiki/Symmetric_difference) operator commonly seen in mathematics classes. It gives us a new set containing everything except `cid`.
3. Now we have our valid and "valid" (entries that contain everything except Country ID) sets, so we just check if our current passport entry matches either one using the [smartmatch](https://docs.raku.org/language/operators#index-entry-smartmatch_operator) operator.

### Part 2

So, after helping security out with their passport issue, now they're starting to get suspicious that _too_ many people are getting through, so we need to tighten up our script.

Now it needs to check both keys and values with the following stipulations:

- Birth Year - Must be a 4-digit number between 1920 and 2002 (inclusive)
- Issue Year - Must be a 4-digit number between 2010 and 2020 (inclusive)
- Expiration Year - Must be a 4-digit number between 2020 and 2030 (inclusive)
- Height - A number followed by either `in` or `cm`
  - If `in`, height must be between 59 and 76 (inclusive)
  - If `cm`, height must be between 150 and 193 (inclusive)
- Hair Color - Must be a `#` character followed by exactly 6 characters `0-9` or `a-f`
- Eye Color - Must be one of `amb, blu, brn, grn, gry, hzl, oth`
- Passport ID - 9-digit number including leading zeroes
- Country ID - We still want to ignore this, or we won't get through

#### Solution

[GitHub Link](https://github.com/aaronreidsmith/advent-of-code/blob/main/2020/04/raku/main.raku)

See below for explanation and any implementation specific comments.

```
sub is-valid(%credentials, $check-values) {
    my $passport-keys = set <byr iyr eyr hgt hcl ecl pid cid>;
    my $north-pole-credentials = $passport-keys ⊖ 'cid';

    my $keys = set %credentials.keys;
    my $valid-keys = $keys ~~ $passport-keys || $keys ~~ $north-pole-credentials;

    if $valid-keys && $check-values {
        my ($byr, $iyr, $eyr, $hgt, $hcl, $ecl, $pid) = %credentials<byr iyr eyr hgt hcl ecl pid>.map(*.Str); # [1]

        my $valid-byr = so $byr ~~ /^<digit> ** 4$/ && $byr.Int ∈ set (1920..2002); # [2][3]
        my $valid-iyr = so $iyr ~~ /^<digit> ** 4$/ && $iyr.Int ∈ set (2010..2020);
        my $valid-eyr = so $eyr ~~ /^<digit> ** 4$/ && $eyr.Int ∈ set (2020..2030);
        my $valid-hgt = gather {
            given $hgt {
                when /^(<digit>+)'in'$/ { take $/[0].Int ∈ set (59..76) }
                when /^(<digit>+)'cm'$/ { take $/[0].Int ∈ set (150..193) }
                default                 { take False }
            }
        }.head;
        my $valid-hcl = so $hcl ~~ /^'#'<xdigit> ** 6$/;                             # [4]
        my $valid-ecl = $ecl ∈ set <amb blu brn gry grn hzl oth>;
        my $valid-pid = so $pid ~~ /^<digit> ** 9$/;
        $valid-byr && $valid-iyr && $valid-eyr && $valid-hgt && $valid-hcl && $valid-ecl && $valid-pid;
    } else {
        $valid-keys;
    }
}

sub MAIN($file, Bool :$p2 = False) {
    say $file.IO
          .slurp
          .split(/\n\n/)
          .map(-> $entry {
              $entry
                .split(/<space>/)
                .map(*.split(':'))
                .map(-> ($key, $value) { $key.trim => $value.trim })
                .Hash
          })
          .map(&is-valid.assuming(*, $p2)) # [5]
          .grep(* == True)
          .elems;
}
```

This runs as such:

```
# Part 1
$ raku main.raku input.txt
237

# Part 2
$ raku main.raku --p2 input.txt
172
```

#### Explanation

This solution could be faster by [short-circuiting](https://en.wikipedia.org/wiki/Short-circuit_evaluation) after each check, but I was going for readability here, so it works.

All that really changed from part 1 is our `is-valid` check, and I feel the logic is fairly straight forward. We basically just unpack the items from our passport (assuming it has all the keys), then test the for validity using a combination of regexes and set containment operators. If all conditions are met, we return `True`, else `False`.

Because it is so straight forward, it was even more maddening when I was off by one. See #2 below for the trap I was falling into!

##### Specific Comments

1. Hashes have a special syntax where you can provide multiple space-separated keys, and it will return all the values as a list. We then map these entries to strings and unpack them. Again, the `<...>` automatically quotes our keys, so we don't have to.
2. Originally this line (along with the rest) looked like `(59..76).contains($byr.Int)`. The logic is exactly the same, but this is apparently a [well-documented trap](https://docs.raku.org/language/traps#Lists_become_strings,_so_beware_.contains()). Basically `.contains` does not test for presence of an element. It converts the list to a string and checks if the given substring exists within it. I don't fully know which item was erroneously getting matched here, but it caused the outcome to be 173 instead of 172.
3. The solution to the above trap is to use set containment operators as shown here. Once again, we are using the Unicode operator, this time we use the ["is an element of"](https://en.wikipedia.org/wiki/Element_(mathematics)#Notation_and_terminology) set operator.
4. `<xdigit>` is a built-in metacharacter for the characters `0-9`, `a-f`, and `A-F`.
5. The way Raku handles [partial functions](https://en.wikipedia.org/wiki/Partial_function) is the [`assuming`](https://docs.raku.org/routine/assuming) method, which allows you to fix one or more parameters when calling a subroutine.


## Final Thoughts

I had a hard time tracking down that bug! I eventually got help from someone on the [Raku subreddit](http://reddit.com/r/rakulang) who was able to point me in the right direction.

With that being said, I am really learning a lot through this exercise. In fact, I am noticing mistakes (or rather, code smells) in my previous solutions! I am not planning on editing them out though; it's always good to see where you came from to remember how far you've come!

See y'all for day 5!