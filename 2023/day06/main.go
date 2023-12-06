package main

import (
	"fmt"
	"strconv"
	"strings"

	"github.com/Pawka/aoc/2023/pkg"
)

const input = "input.txt"

func main() {
	var (
		resultA   = 0
		lines     = pkg.ReadLines(input)
		times     = strings.Fields(lines[0])[1:]
		distances = strings.Fields(lines[1])[1:]
	)

	for i := 0; i < len(times); i++ {
		var (
			time, _     = strconv.Atoi(times[i])
			distance, _ = strconv.Atoi(distances[i])
			res         = solve(time, distance)
		)

		if i == 0 {
			resultA = res
		} else {
			resultA *= res
		}
	}

	var (
		theTime = strings.Join(times, "")
		theDist = strings.Join(distances, "")
		tt, _   = strconv.Atoi(theTime)
		dd, _   = strconv.Atoi(theDist)
	)

	fmt.Println(resultA)
	fmt.Println(solve(tt, dd))
}

func solve(time, distance int) int {
	var (
		current = 0
		i       = 0
	)
	for {
		current = i * (time - i)
		if current > distance {
			break
		}
		i++
	}
	res := time - i*2 + 1
	return res
}
