
This is a JavaScript challenge. Your input is injected three ways:

- `YOUR_INPUT`
- `"YOUR_INPUT"`
- `'YOUR_INPUT'`

Your task is to access the `target.exploit` attribute in all three cases, using a single payload.

You can use at most 3 `*` characters, and 28 characters total.

# Solution to Flip the Script
Solvers, please let me know if you find a shorter or easier solution!

This works:

    /*"+/*'*/i/+target.exploit//

I don't want you to be able to do this, so I say it has too many stars:

    /*"+/*'+/**/target.exploit//

First, note that `i` is used as a loop variable
(and thus is accessible through `eval()`).

The trick in my solution is to overload `*/i/`:

- In the single-quoted case, multiply a string by a regular expression
  literal of `i`, then add `target.exploit`.
- In the double-quoted case, add a string to `i / ((unary plus) target.exploit)`
- In the unquoted case, divide `i` by ((unary plus) target.exploit)

# Notes
- This challenge uses JavaScript getters to remove the need
  for parentheses (and their associated mischief).

