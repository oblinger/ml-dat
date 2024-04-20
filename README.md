# dat
Data and code encapsulation for ML experimentation and productization


## Installation

```bash
pip install -e .
```

## Usage

```bash
cd tests; ./do hello_world
```

## Testing

```bash
python -m pytest
```

## Development

```bash
python -m black src
```


do = DoManager(dat_dict['do_folder'])
method1 = do.method1
method2 = do.method2


## Ask
- How to: from ml_dat import Inst, do
- Accept the list into a constructor.  must I do a shallow copy?
- Should .add_insts accept a list of insts or a star list of insts?
- I plan to split ml-cube from ml-dat
- Right now Inst has ALL property functions.  maybe it is more confusing than helpful.

inst.path().

Cube(insts=, point_fns=, data_folder=)
Cube()
Cube.add_point_fns(...)
lambda x: {"my": 333}
""

c3 = c1 + c2
c4 = Cube(points=funky_function(c3.points))

c1 = []
c2 = []
c3 = c1 + c2


df = df_utils.build_from_insts(insts, point_fns, data_folder)
df = DataFrames.build_from_insts(insts, point_fns, data_folder)


## Todo
- [ ] convert inst names to use '.' instead of '/' (still needs testing)

## Later
- [ ] Split ml-cube into a separate package
- [ ] Add a `requirements.txt` file
- [ ] Add a `setup.py` file
- [ ] make inst use the datconfig defined folder 
- Support cube of cubes with cached points in sub cubes
TODO for cube.py
- Implement the 'merge_keys' method
- Implement the 'get_csv' method
- Support inst 'Cube' section that build data cube and cube reports
l