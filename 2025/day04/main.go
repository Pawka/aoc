package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
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

	solve(data)
}

const (
	Empty = 0
	Paper = 1
)

func matrix(input []string) [][]int {
	data := make([][]int, len(input))

	for i, l := range input {
		data[i] = make([]int, 0, len(l))

		for _, chr := range strings.Split(l, "") {
			var cell = Empty
			if chr == "@" {
				cell = Paper
			}
			data[i] = append(data[i], cell)
		}
	}

	return data
}

func solve(data [][]int) {
	var (
		width  = len(data[0])
		height = len(data)

		result int
	)

	for y, line := range data {
		for x, _ := range line {
			if data[y][x] == Empty {
				continue
			}

			// Check
			pappersArround := 0
			for x1 := x - 1; x1 <= x+1; x1++ {
				for y1 := y - 1; y1 <= y+1; y1++ {
					if x1 < 0 || x1 >= width {
						continue
					}
					if y1 < 0 || y1 >= height {
						continue
					}
					if x1 == x && y1 == y {
						continue
					}
					if data[y1][x1] == Paper {
						pappersArround += 1
					}
				}
			}
			if pappersArround < 4 {
				result += 1
			}
		}
	}

	fmt.Println(result)
}
