---
title: "Advent of Code: Day 13"
last_modified_at: 2020-12-14T19:46:00-05:00
categories:
  - Blog
tags:
  - Advent of Code
  - Raku
---

Today's challenge was... interesting, to say the least. It may look short and sweet, but it is fairly complex and requires a fair bit of [number theory](https://en.wikipedia.org/wiki/Number_theory) for part two.

## The Problem

### Part 1

After [yesterday's fiasco](https://aaronreidsmith.github.io/blog/advent-of-code-day-12/), our ferry is being forced to make an emergency stop on a different island. Unfortunately, there are no ferries from this island to our destination island; once again, we will have to take a plane. To get to the airport, our only option is a bus. Bus IDs also correspond to how often they come. I.e., a bus with ID 7 will come at timestamps 0, 7, 14, etc.

We took a few notes (our input) on the bus schedule. Example:

```
939
7,13,x,x,59,x,31,19
```

The first line is the earliest timestamp we will be able to make it to the bus station, and the second line is a list of bus IDs; buses that are out of service are denoted with an X. Given this information, our goal is to find the earliest bus that will get us to the airport. With the above example, we can see how this breaks down (in the below table a `D` means "departure"):

```
time   bus 7   bus 13  bus 59  bus 31  bus 19
929      .       .       .       .       .
930      .       .       .       D       .
931      D       .       .       .       D
932      .       .       .       .       .
933      .       .       .       .       .
934      .       .       .       .       .
935      .       .       .       .       .
936      .       D       .       .       .
937      .       .       .       .       .
938      D       .       .       .       .
939      .       .       .       .       .  <--- Time we make it to the bus station
940      .       .       .       .       .
941      .       .       .       .       .
942      .       .       .       .       .
943      .       .       .       .       .
944      .       .       D       .       .  <--- First bus that can take us to the airport
945      D       .       .       .       .
946      .       .       .       .       .
947      .       .       .       .       .
948      .       .       .       .       .
949      .       D       .       .       .
```

Once we have found the bus that can take us to the airport, we need to calculate the product of the bus ID and our wait time. In the example above it would be `59 * (944 - 939) = 295`.

#### Solution

[GitHub Link](https://github.com/aaronreidsmith/advent-of-code/blob/main/2020/13/raku/main.raku)

See below for explanation and any implementation-specific comments.

```
sub MAIN($file) {
    my @input = $file.IO.lines;
    my $arrival-time = @input[0].Int;
    my @buses = @input[1].split(',').grep(* ne 'x').map(*.Int);
    say [*] @buses
            .map(-> $id { ($id, $id - $arrival-time % $id) })
            .min(*[1])
            .flat;
}
```

This runs as such:

```
$ raku main.raku input.txt
261
```

#### Explanation

Since our bus timestamps will always just be multiples of the bus ID, we can look at just the bus IDs themselves to find how long we will be waiting. When we calculate the remainder between `$arrival-time` and `$id`, it will show us how many minutes have passed **since the last bus**. Let's look at this in context:

```
939 % 7  = 1  (means there was a bus 1 minute ago)
939 % 13 = 3  (means there was a bus 3 minutes ago)
939 % 59 = 54 (means there was a bus 54 minutes ago)
939 % 31 = 9  (means there was a bus 9 minutes ago)
939 % 19 = 8  (means there was a bus 8 minutes ago)
```

So, looking at the above, it is not immediately obvious what we need to do. Basically, since we know how often a bus comes, we want to minimize the value of `$id - <output of above>`. To do that, we simply subtract the amount of time that has passed for each bus from its scheduled departure time:

```
 7 - (939 %  7) =  7 - 1  = 6
13 - (939 % 13) = 13 - 3  = 10
59 - (939 % 59) = 59 - 54 = 5
31 - (939 % 31) = 31 - 9  = 22
19 - (939 % 19) = 19 - 8  = 11
```

So from this, it is obvious that bus 59 has the shortest time to next departure, so that is the best choice. At this point, we multiply 59 * 5 and get 295.

I feel the code reflects this pretty well. The first three lines are just pulling the data in, removing the `x` buses, and converting things to integers. After that, for each bus ID, we do the calculations above, then filter it down to the minimum wait time. Finally, we flatten it into one list and multiply the values (via the `[*]` metaoperator). That's it!

##### Specific Comments

No specific comments today; I feel it is pretty straightforward.

### Part 2

So after all the time we just spent to find the bus that will get us to the airport the fastest, we throw it all out the window.

The shuttle company is running a contest to find the earliest timestamp such that each bus will depart one minute after the next. In the case of an `x`, there no constraints on bus IDs in that slot. So, given the same input as above:

```
7,13,x,x,59,x,31,19
```

We are looking for a timestamp (`t`) that satisfies these conditions:

- Bus ID `7` departs at timestamp `t`.
- Bus ID `13` departs one minute after timestamp `t`.
- There are no requirements or restrictions on departures at two or three minutes after timestamp `t`.
- Bus ID `59` departs four minutes after timestamp `t`.
- There are no requirements or restrictions on departures at five minutes after timestamp `t`.
- Bus ID `31` departs six minutes after timestamp `t`.
- Bus ID `19` departs seven minutes after timestamp `t`.

In this example, the answer is `1068781`, as shown here:

```
time     bus 7   bus 13  bus 59  bus 31  bus 19
1068773    .       .       .       .       .
1068774    D       .       .       .       .
1068775    .       .       .       .       .
1068776    .       .       .       .       .
1068777    .       .       .       .       .
1068778    .       .       .       .       .
1068779    .       .       .       .       .
1068780    .       .       .       .       .
1068781    D       .       .       .       .  <--- Bus 7 departs at timestamp `t`
1068782    .       D       .       .       .  <--- Bus 13 departs 1 minutes after `t`
1068783    .       .       .       .       .
1068784    .       .       .       .       .
1068785    .       .       D       .       .  <--- Bus 59 departs 4 minutes after `t`
1068786    .       .       .       .       .
1068787    .       .       .       D       .  <--- Bus 31 departs 6 minutes after `t`
1068788    D       .       .       .       D  <--- Bus 19 departs 7 minutes after `t`
1068789    .       .       .       .       .
1068790    .       .       .       .       .
1068791    .       .       .       .       .
1068792    .       .       .       .       .
1068793    .       .       .       .       .
1068794    .       .       .       .       .
1068795    D       D       .       .       .
1068796    .       .       .       .       .
1068797    .       .       .       .       .
```

Looking at our notes (our input), we realize that timestamp `t` will _surely_ be larger thn **100 _trillion_**, so we need to be smart about how we calculate it.

#### Solution

[GitHub Link](https://github.com/aaronreidsmith/advent-of-code/blob/main/2020/13/raku/main.raku)

See below for explanation and any implementation-specific comments.

```
sub MAIN($file, Bool :$p2 = False) {
    my @input = $file.IO.lines;
    if $p2 {
        # https://brilliant.org/wiki/chinese-remainder-theorem
        my @buses = @input[1].split(',').antipairs.grep(*.key ne 'x');

        my @times = @buses.map(*.key.Int);
        my @offsets = @buses.map(-> $pair { $pair.key - $pair.value });

        my $N = [*] @times;
        my @x = do for @offsets Z @times -> ($offset, $depart-time) {
            $offset * ($N div $depart-time) * expmod($N div $depart-time, -1, $depart-time);
        }

        say @x.sum % $N;
    } else {
        my @buses = @input[1].split(',').grep(* ne 'x').map(*.Int);
        my $arrival-time = @input[0].Int;
        say [*] @buses
                .map(-> $id { ($id, $id - $arrival-time % $id) })
                .min(*[1])
                .flat;
    }
}
```

This runs as such:

```
# Part 1
$ raku main.raku input.txt
261

# Part 2
$ raku main.raku --p2 input.txt
807435693182510
```

#### Explanation

So obviously, given the hint about 100 trillion in the problem, we can't just brute force this. The brute force method (using the example data) would be to start at 100 trillion and basically just go one-by-one until each subsequent bus passes our tests. Given that our actual output is closer to 1 quadrillion, that would take _forever_.

That's where number theory comes in. As I commented in the code, there is something called [Chinese remainder theorem](https://en.wikipedia.org/wiki/Chinese_remainder_theorem) that basically states the following:

Given the following items:

- A sequence `n` of [pairwise coprime](https://en.wikipedia.org/wiki/Coprime_integers#Coprimality_in_sets) integers
- A sequence `a`, such that `0 <= ai < ni` for every `i`
- An integer `N` defined as the product of all integers in the sequence `n`

There is exactly one number, `x`, in the range `0 <= x < N` such that `x % ai == ni`.

I won't go too deep into the math here, but basically (again, using example data) we have the following terms:

- Our sequence `n`: `7, 13, 59, 31, 19`
- Our sequence `a`: `0, 1, 4, 6, 7`
- Our number `N`: `7 * 13 * 59 * 31 * 19 = 3162341`

And we basically solve for `x`. That's pretty much as far as I can go with this explanation, as Chinese remainder theorem is pretty advanced for me as well. I just converted the proof in the commented link to Raku to make this work 🙂

When we do this with our real data, rather than running forever, it finishes in about 0.27 seconds (using a fairly slow language). 

##### Specific Comments

I don't fully understand the implementation here, so I have nothing to add 😂

## Final Thoughts

We are officially past the halfway point! I wouldn't say this was the toughest one, it felt like more of a trick question. Regardless, I expect the difficulty to start ramping quite a bit; hopefully I can keep up.

