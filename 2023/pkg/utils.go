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
