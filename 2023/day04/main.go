package main

import (
	"fmt"
	"strings"

	"github.com/Pawka/aoc/2023/pkg"
)

const input = "input.txt"

func main() {
	lines := pkg.ReadLines(input)
	partA(lines)
	partB(lines)
}

func partA(lines []string) {
	var sum = 0
	for _, line := range lines {
		var (
			card    = strings.Split(line, ": ")
			parts   = strings.Split(card[1], " | ")
			lucky   = strings.Fields(parts[0])
			current = strings.Fields(parts[1])
			mlucky  = make(map[string]bool)
		)

		for _, l := range lucky {
			mlucky[l] = true
		}

		var val = 0
		for _, n := range current {
			if _, ok := mlucky[n]; ok {
				if val == 0 {
					val = 1
				} else {
					val *= 2
				}
			}
		}
		sum += val
	}

	fmt.Println(sum)
}

func partB(lines []string) {
	var (
		points = make([]int, len(lines))
		sum    = 0
	)

	for i := 0; i < len(lines); i++ {
		var (
			line    = lines[i]
			card    = strings.Split(line, ": ")
			parts   = strings.Split(card[1], " | ")
			lucky   = strings.Fields(parts[0])
			current = strings.Fields(parts[1])
			mlucky  = make(map[string]bool)
		)

		for _, l := range lucky {
			mlucky[l] = true
		}

		var val = 0
		for _, n := range current {
			if _, ok := mlucky[n]; ok {
				val++
			}
		}

		points[i] = val
	}

	var sums = make([]int, len(lines))
	for i := len(lines) - 1; i >= 0; i-- {
		sums[i] = 1
		for j := 1; j <= points[i]; j++ {
			sums[i] += sums[i+j]
		}
	}
	for _, v := range sums {
		sum += v
	}

	fmt.Println(sum)
}
