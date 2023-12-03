package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
	"unicode"
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

	partA(lines)
}

type Token struct {
	Row, Col int
	Str      string
}

func (d Token) String() string {
	return d.Str
}

func (d Token) Pos() string {
	return fmt.Sprintf("%d;%d", d.Row, d.Col)
}

func partA(lines []string) {
	digits := []*Token{}
	chars := []*Token{}

	for row, line := range lines {
		var (
			digit = &Token{}
		)

		for col, symbol := range line {
			if unicode.IsDigit(symbol) {
				if digit.Str == "" {
					digit.Row = row
					digit.Col = col

				}
				digit.Str += string(symbol)
			} else {
				if len(digit.Str) > 0 {
					digits = append(digits, digit)
					digit = &Token{}
				}
				// If some char found.
				if symbol != '.' {
					chars = append(chars, &Token{
						Row: row,
						Col: col,
						Str: string(symbol),
					})
				}
			}
		}
		if len(digit.Str) > 0 {
			digits = append(digits, digit)
			digit = &Token{}
		}
	}

	sums := make(map[string]int)
	gears := make(map[string][]int)
	for _, d := range digits {
		n, _ := strconv.Atoi(d.Str)
		for _, p := range digitPositions(d) {
			sums[p] += n
			if len(gears[p]) == 0 {
				gears[p] = make([]int, 0)
			}
			gears[p] = append(gears[p], n)
		}
	}
	resultA := 0
	resultB := 0
	for _, d := range chars {
		p := d.Pos()
		resultA += sums[p]
		if d.Str == "*" && len(gears[p]) == 2 {
			resultB += (gears[p][0] * gears[p][1])
		}
	}

	fmt.Println(resultA)
	fmt.Println(resultB)
}

func digitPositions(digit *Token) []string {
	result := []string{
		fmt.Sprintf("%d;%d", digit.Row, digit.Col-1),
		fmt.Sprintf("%d;%d", digit.Row, digit.Col+len(digit.Str)),
	}

	for i := digit.Col - 1; i <= digit.Col+len(digit.Str); i++ {
		result = append(result,
			fmt.Sprintf("%d;%d", digit.Row-1, i),
			fmt.Sprintf("%d;%d", digit.Row+1, i),
		)
	}

	return result
}
