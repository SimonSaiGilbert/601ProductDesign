import sys

def add(x: float, y:float):
	return x + y

if __name__ == '__main__':
	x = sys.argv[1]
	y = sys.argv[2]
	S = add(float(x), float(y))
	print(S)