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

type Range struct {
	from, to int
}

func main() {
	file, err := os.Open(input)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	var (
		scanner          = bufio.NewScanner(file)
		ranges           = make([]Range, 0, 10)
		ingredients      = make([]int, 0, 10)
		parseIngredients = false
	)

	for scanner.Scan() {
		line := scanner.Text()
		if line == "" {
			parseIngredients = true
			continue
		}

		if parseIngredients {
			num, _ := strconv.Atoi(line)
			ingredients = append(ingredients, num)
		} else {
			nums := strings.Split(line, "-")
			from, _ := strconv.Atoi(nums[0])
			to, _ := strconv.Atoi(nums[1])
			ranges = append(ranges, Range{from, to})
		}

	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	solve(ranges, ingredients)
}

func solve(ranges []Range, ingredients []int) {

	var total int
	for _, i := range ingredients {
		for _, r := range ranges {
			if i >= r.from && i <= r.to {
				total += 1
				break
			}
		}
	}

	fmt.Println(total)
}
