package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"regexp"
	"strconv"
	"strings"
)

const input = "input.txt"

var (
	first = regexp.MustCompile(`^[^\d]*([\d])`)
	last  = regexp.MustCompile(`([\d])[^\d]*$`)
)

func main() {
	file, err := os.Open(input)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	var (
		scanner = bufio.NewScanner(file)
		sumA    = 0
		sumB    = 0
	)
	// optionally, resize scanner's capacity for lines over 64K, see next example
	for scanner.Scan() {
		line := scanner.Text()
		sumA += partA(line)
		sumB += partB(line)
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
	fmt.Println(sumA)
	fmt.Println(sumB)
}

func partA(line string) int {
	f := first.FindStringSubmatch(line)
	l := last.FindStringSubmatch(line)
	fmt.Println(line, f)
	var (
		decimal = 0
		unit    = 0
	)
	if len(f) == 2 {
		decimal, _ = strconv.Atoi(f[1])
	}
	if len(l) == 2 {
		unit, _ = strconv.Atoi(l[1])
	}
	return decimal*10 + unit
}

func partB(line string) int {
	rpl1 := strings.NewReplacer(
		"eightwo", "eighttwo",
		"eightree", "eighttree",
		"fiveight", "fiveeithg",
		"nineight", "nineeight",
		"oneight", "oneeight",
		"sevenine", "sevennine",
		"threeight", "threeeight",
		"twone", "twoone",
	)
	rpl := strings.NewReplacer(
		"eight", "8",
		"five", "5",
		"four", "4",
		"nine", "9",
		"one", "1",
		"seven", "7",
		"six", "6",
		"three", "3",
		"two", "2",
	)
	rline := rpl1.Replace(line)
	rline = rpl.Replace(rline)
	f := first.FindStringSubmatch(rline)
	l := last.FindStringSubmatch(rline)
	decimal, _ := strconv.Atoi(f[1])
	unit, _ := strconv.Atoi(l[1])
	fmt.Println(line, rline, decimal, unit)
	return decimal*10 + unit
}
