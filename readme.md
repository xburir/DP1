# Map match

## How to use:

First, you need to prepare files for the script

### Directory structure

You should have one directory, which contains two directories "Walk" and "Drive".

In each directory put the csv files, which contain your path data. For example:

```
root
|-- Drive
|   |-- 33718.csv
|   |-- 31783.csv
|-- Walk
|   |-- 93293.csv
|   |-- 44352.csv
|   |-- 764555.csv
|   |-- 354852.csv
```

### CSV structure

Your csv file should be two columns, first longitude, second lattitude, for example:

```
lon,lat
17.07299,48.151611
17.073095,48.151878
17.073084,48.15184
17.073084,48.151733
17.073048,48.151672
17.073011,48.151714
```

### Running script

```
python3 path_to_root debug[optional]
ex: python3 "C:/Users/richard.buri/search_web/python/test/" debug
ex: python3 "C:/Users/richard.buri/search_web/python/test/"
```

Running the script with debug parameter will generate 2 geojsons for each csv file for easy visualization. First file is the original points, the second one is mapmatched points.
