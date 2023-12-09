package main

import (
	"fmt"
	"regexp"

	"github.com/Pawka/aoc/2023/pkg"
)

const (
	input = "input.txt"
	Left  = 0
	Right = 1
)

var Direction = map[rune]int{
	'L': Left,
	'R': Right,
}

func main() {
	var (
		lines = pkg.ReadLines(input)
		re    = regexp.MustCompile("[A-Z0-9]+")
		sides string
		graph = make(map[string][]string)
	)

	for i, l := range lines {
		if i == 0 {
			sides = l
			continue
		}
		if l == "" {
			continue
		}
		nodes := re.FindAllString(l, 3)
		graph[nodes[0]] = nodes[1:]
	}

	solveA(sides, graph)
	solveB(sides, graph)
}

func solveA(sides string, graph map[string][]string) {
	var (
		steps   = 0
		current = "AAA"
	)
	for {
		i := steps % len(sides)
		steps++
		current = graph[current][Direction[rune(sides[i])]]
		if current == "ZZZ" {
			break
		}
	}
	fmt.Println(steps)
}

func solveB(sides string, graph map[string][]string) {
	var (
		current   string
		starts    = []string{}
		direction = map[rune]int{
			'L': Left,
			'R': Right,
		}
	)

	for k := range graph {
		if k[2] == 'A' {
			starts = append(starts, k)
		}
	}

	allSteps := make([]int, 0, len(current))
	for _, current := range starts {
		var steps = 0
		for {
			i := steps % len(sides)
			steps++
			current = graph[current][direction[rune(sides[i])]]
			if current[2] == 'Z' {
				allSteps = append(allSteps, steps)
				break
			}
		}
	}

	fmt.Println(pkg.LCM(allSteps...))
}
