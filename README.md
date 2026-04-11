# Why did I chose this project

* ### To learn how to organise a large codebase, by using seperate files etc
* ### I created it in the form of a python libary to experement with how real codebases would be writen

---
# Usage

* run `pip install -e .` in `.\font-file-parser` to create local package later it will be available as a public python package

* Run any file in `usage\`

---
# TODO:
* Fix naming convention
* Probaly have a seperate TTF parser (and OTF etc.)
* Read complex glyphs
* Read cmap table

# ...
# Optimisation
* Make version without reader class, just using list comprehension e.g. data[head: head+1]
* Make version in C++