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
		lines   = make([][]string, 0, 10)
	)
	for scanner.Scan() {
		line := scanner.Text()
		tokens := strings.Fields(line)
		lines = append(lines, tokens)
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	solveA(lines)

}

func solveA(lines [][]string) {
	var res int

	for x := 0; x < len(lines[0]); x++ {
		var val int = 0
		if lines[len(lines)-1][x] == "*" {
			val = 1
		}

		for y := 0; y < len(lines)-1; y++ {
			num, _ := strconv.Atoi(lines[y][x])
			if lines[len(lines)-1][x] == "*" {
				val = val * num
			} else {
				val += num
			}
		}

		res += val
	}

	fmt.Println(res)
}
