package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
)

// Wrong answers (B):
// 5393

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
		lines   = make([]string, 0)
	)
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	assert(calcB(0, 100), 1)
	assert(calcB(0, 101), 1)
	assert(calcB(0, 200), 2)
	assert(calcB(1, 100), 1)
	assert(calcB(1, 101), 1)
	assert(calcB(1, 200), 2)
	assert(calcB(1, 1), 0)
	assert(calcB(99, 1), 1)

	assert(calcB(0, -100), 1)
	assert(calcB(0, -101), 1)
	assert(calcB(1, -101), 2)
	assert(calcB(0, -200), 2)
	assert(calcB(0, -1), 0)

	assert(calcB(1, -1), 1)
	assert(calcB(0, 0), 0)

	assert(calcB(1, -2), 1)
	assert(calcB(1, -200), 2)
	assert(calcB(1, -201), 3)
	assert(calcB(1, -202), 3)

	assert(calcB(50, -50), 1)
	assert(calcB(50, 150), 2)
	assert(calcB(50, -150), 2)

	solve(lines)
}

func assert(got, want int) {
	if got != want {
		failure := fmt.Sprintf("got(%d) != want(%d)", got, want)
		panic(failure)
	}
}

func calcB(pos, turn int) int {
	var (
		res    int
		newPos = pos + turn
	)

	res += newPos / 100
	if res == 0 {

		if pos == newPos {
			return 0
		}

		if newPos == 0 {
			return 1
		}

		if pos > 0 && newPos < 0 {
			res += 1
		}
	}

	if res < 0 {
		res *= -1
	}

	if newPos/100 != 0 && pos > 0 && newPos < 0 {
		res += 1
	}

	return res
}

func solve(lines []string) {
	var (
		pos    = 50
		countA = 0
		countB = 0
	)

	for _, line := range lines {
		add, err := strconv.Atoi(line[1:])
		if err != nil {
			panic(err)
		}
		if string(line[0]) == "L" {
			add = add * -1
		}

		countB += calcB(pos, add)
		pos = (pos + add) % 100
		if pos < 0 {
			pos = 100 + pos
		}

		if pos == 0 {
			countA += 1
		}

	}
	fmt.Println(countA, countB)
}
