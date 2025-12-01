package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
)

const input = "input.txt"

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

	solve(lines)
}

func solve(lines []string) {
	pos := 50
	count := 0

	fmt.Println(pos)
	for _, line := range lines {
		add, err := strconv.Atoi(line[1:])
		if err != nil {
			panic(err)
		}
		if string(line[0]) == "L" {
			add = add * -1
		}

		pos = (pos + add) % 100
		fmt.Println(line, pos)
		if pos < 0 {
			pos = 100 + pos
		}
		fmt.Println(line, add, pos)

		if pos == 0 {
			count += 1
		}

	}
	fmt.Println(pos, count)
}
