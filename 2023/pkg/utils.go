package pkg

import (
	"bufio"
	"os"
)

func ReadLines(input string) []string {
	file, err := os.Open(input)
	if err != nil {
		panic(err)
	}
	defer file.Close()

	var (
		scanner = bufio.NewScanner(file)
		lines   = make([]string, 0)
	)
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}

	if err := scanner.Err(); err != nil {
		panic(err)
	}

	return lines
}

// Greatest common denominator
func GCD(a, b int) int {
	for b != 0 {
		t := b
		b = a % b
		a = t
	}
	return a
}

// Lowest common multiplier
func LCM(in ...int) int {
	if len(in) < 2 {
		panic("At least two integers required forl LCM!")
	}
	result := in[0] * in[1] / GCD(in[0], in[1])
	for _, i := range in[2:] {
		result = LCM(result, i)
	}

	return result
}
