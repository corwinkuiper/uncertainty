# Uncertainty

Takes a function of some values and returns a value and uncertainty in it's value.
For example, `python uncertainty.py "A(20, 3)**2` is a function of A.
Then the value A = 20 ± 3 is propagated through the function.
The expected answer, through symbolic calculation is: 400 ± 120.
This script outputs: 400.0 ± 120.0 representing the floating point nature of the operation.

I have written about what I understand about uncertainties [over here](https://blog.kuiper.dev/uncertainties).
The [Wikipedia Article](https://en.wikipedia.org/wiki/Propagation_of_uncertainty) on the subject is also good.

On it's own this is not all too useful, however it should be useful enough to maybe check calculations?

## Example

* `python uncertainty.py "A(20, 3) + B(10, 4)"`
* This is a function, f, of A and B where f = A + B.
* The value of A is 20 ± 3.
* The value of B is 10 ± 4.
* The value of the function, f, is then 30 ± 5.