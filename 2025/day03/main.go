package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

const (
	input = "input.txt"
	// input = "input-demo.txt"
)

func main() {
	file, err := os.Open(input)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	var (
		scanner = bufio.NewScanner(file)
		lines   = make([]string, 0, 10)
	)
	for scanner.Scan() {
		line := scanner.Text()
		lines = append(lines, line)
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	data := matrix(lines)
	solve(data, 2)
	solve(data, 12)
}

func matrix(input []string) [][]int {
	data := make([][]int, len(input))

	for i, l := range input {
		data[i] = make([]int, 0, len(l))

		for _, chr := range strings.Split(l, "") {
			num, _ := strconv.Atoi(chr)
			data[i] = append(data[i], num)
		}
	}

	return data
}

func solve(input [][]int, size int) {
	var (
		sum    int
		length = len(input[0])
	)

	for _, line := range input {

		var (
			code   = make([]int, 0, size)
			maxPos = -1
			max    = 0
		)
		for s := size; s > 0; s-- {
			max = 0
			_maxPos := maxPos
			for i := length - s; i > maxPos; i-- {
				if line[i] >= max {
					max = line[i]
					_maxPos = i
				}
			}
			maxPos = _maxPos
			code = append(code, max)
		}

		var str string
		for _, n := range code {
			str += fmt.Sprintf("%d", n)
		}
		_code, _ := strconv.Atoi(str)
		sum += _code
	}

	fmt.Println(sum)
}
