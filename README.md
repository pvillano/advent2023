# Advent 2023

My solutions for [Advent of Code 2023](https://adventofcode.com/2023).

Feel free to copy `template.py` or anything in `utils`

Feel free to study any of `day01.py`, `day02.py` etc.

     ||::|:||   .--------,
     |:||:|:|   |_______ /        .-.
     ||::|:|| ."`  ___  `".    {\('v')/}
     \\\/\///:  .'`   `'.  ;____`(   )'____
      \====/ './  o   o  \|~     ^" "^   //
       \\//   |   ())) .  |   Season's    \
        ||     \ `.__.'  /|   Greetings  //
        ||   _{``-.___.-'\|  from Peter   \
        || _." `-.____.-'`|    ___       //
        ||`        __ \   |___/   \_______\
      ."||        (__) \    \|     /
     /   `\/       __   vvvvv'\___/
     |     |      (__)        |
      \___/\                 /
        ||  |     .___.     |
        ||  |       |       |
        ||.-'       |       '-.
    jgs ||          |          )
        ||----------'---------'
from [ascii.co.uk](https://ascii.co.uk/art/snowman)


# Library Functions

### benchmark
```python
def benchmark(func: Callable, *args, **kwargs) -> None:
```
In the following order:
- prints the start time
- Calls a function with the given arguments and prints the return value
- prints the execution time

-----

### get_day
```python
def get_day(day: int, practice: str = "", *, year: int = 2023, override=False) -> str:
```
This function automatically retrieves a specific day's input text, returning it as a str

-----

### debug_print
```python
def debug_print(*args, override=False, **kwargs) -> None:
```
Passes arguments to `print`,
if currently executing program
is being debugged or override is True

-----

### debug_print_recursive
```python
def debug_print_recursive(*args, override=False, **kwargs) -> None:
```
Prints with an indent proportional to the current call stack depth

-----

### debug_print_sparse_grid
```python
def debug_print_sparse_grid(grid_map: dict[(int, int), Any] or set, *, transpose=False, override=False) -> None:
```
Prints a sparse grid densely

-----

### otqdm
```python
def otqdm(
    iterator: Sized and Iterable,
    min_interval=1,
    min_iters=1,
    unit="it/s",
    n_bars=10,
    percent_is_time=False,
    bars_is_time=False,
    len_iterator=None,
):
```
Operates similarly to tqdm, but also gives an estimate of the fuction's algorithmic complexity
