# Brainfrick to Go Transpiler

Converts Brainf*** (here called Brainfrick) code into Go code. This Go code could then be compiled to a binary.

This project was inspired by [Walnut](https://kabir.computer/p/walnut), which accomplishes more-or-less the same thing. That being said, any similarities between this code and their's is entirely accidental.

## Installation

Note: dependencies are `git` for installation, `python3` for transpiling, and `go` for using the generated Go code.  
Download source code with:
```
git clone https://github.com/asmith-dev/brainfrick_to_go.git
```

## Usage

I have included two examples in the `test` directory:
- Simple Hello World program - `helloWorld.bf`
- Complicated Mandelbrot terminal art - `mandelbrot.bf`

Note: the Mandelbrot source code was borrowed - credit is due elsewhere.
<br><br>
Within the parent directory of `brainfrick_to_go`, generate Go code using:
```
python3 brainfrick_to_go <SOURCE_CODE_PATH>
```

To demonstrate using the given example codes:
```
python3 brainfrick_to_go brainfrick_to_go/test/helloWorld.bf

# OR

python3 brainfrick_to_go brainfrick_to_go/test/mandelbrot.bf
```

This will generate a Go file in the current directory.  
To use this Go code:
```
# Execute/run with
go run <GO_FILE>

# Compile to a binary with
go build <GO_FILE>
```

## Notes

While the conversion from Brainfrick to Go is <em>decently efficient</em>, running the resulting Go code can be <em>incredibly inefficient</em> (try the `mandelbrot` example to see this). This does not seem to be an issue with the method of conversion; rather, it is a limitation of converting Brainfrick to Go in general. Therefore, this project serves as more of a proof of concept. For a more efficient compilation of Brainfrick code, see my other project - [Brainf*** compiler written in Go](https://github.com/asmith-dev/brainfrick).