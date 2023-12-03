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
	for _, d := range digits {
		n, _ := strconv.Atoi(d.Str)
		for _, p := range digitPositions(d) {
			sums[p] += n
		}
	}
	for k, d := range sums {
		fmt.Printf("%s:\t%d\n", k, d)
	}
	result := 0
	for _, d := range chars {
		fmt.Printf("%#v\n", d)
		fmt.Println(sums[d.Pos()])
		result += sums[d.Pos()]
	}

	fmt.Println(result)
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
