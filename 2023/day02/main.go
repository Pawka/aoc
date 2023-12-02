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
	//Game 1: 3 blue, 2 green, 6 red; 17 green, 4 red, 8 blue; 2 red, 1 green, 10 blue; 1 blue, 5 green

	limits := map[string]int{
		"red":   12,
		"green": 13,
		"blue":  14,
	}

	var (
		parts = strings.Split(line, ": ")
		game  = parts[0]
		sets  = strings.Split(parts[1], "; ")
	)

	for _, set := range sets {
		pairs := strings.Split(set, ", ")
		for _, pair := range pairs {
			var (
				t      = strings.Split(pair, " ")
				val, _ = strconv.Atoi(t[0])
				colour = t[1]
			)
			if val > limits[colour] {
				return 0
			}
		}
	}

	game_no, _ := strconv.Atoi(strings.Split(game, " ")[1])
	return game_no
}

func partB(line string) int {
	//Game 1: 3 blue, 2 green, 6 red; 17 green, 4 red, 8 blue; 2 red, 1 green, 10 blue; 1 blue, 5 green

	limits := map[string]int{
		"red":   0,
		"green": 0,
		"blue":  0,
	}

	var (
		parts = strings.Split(line, ": ")
		sets  = strings.Split(parts[1], "; ")
	)

	for _, set := range sets {
		pairs := strings.Split(set, ", ")
		fmt.Printf("%#v\n", pairs)
		for _, pair := range pairs {
			var (
				t      = strings.Split(pair, " ")
				val, _ = strconv.Atoi(t[0])
				colour = t[1]
			)
			if val > limits[colour] {
				limits[colour] = val
			}
		}
	}

	return limits["red"] * limits["green"] * limits["blue"]
}
