# Extract recursively
Module to extract tar/gzip files recursively

#### Using

Extract tar, tgz, tbz, tb2 file
```python
filepath = "/home/test.tar"
Extract.tar(filepath)
```

Extract gz
```python
filepath = "/home/test.gz"
Extract.gz(filepath)
```

Extract recursively or unkown file (read code ducmentation for special setup) 
```python
filepath = "/home/test.tgz"
Extract.extract(filepath)
```

Make unique directory path
Dictories in home directory
```
/home/test
/home/test 1
/home/test 2
```
Python code
```python
>>>directory_path = "/home/test"
>>>var = Extract.make_unique_directory_name(directory_path)
>>>print(var)
>>> '/home/test 3'
```
