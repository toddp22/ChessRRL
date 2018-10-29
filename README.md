# ChessRRL

install python-chess with `pip install python-chess` (or `pip3 install python-chess`)
install binarytree with `pip install binarytree` (or `pip3 install binarytree`)

run with `python main.py` (or `python3 main.py`)

## storing python structures in a file
* `import pickle`
* `file = open('filename.bin', 'wb')`
* `pickle.dump(your_data, file)`

## loading python structures in a file
* `import pickle`
* `file = open('filename.bin', 'rb')`
* `your_data = pickle.load(file)`
