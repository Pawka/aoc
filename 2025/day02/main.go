package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"slices"
	"strconv"
	"strings"
)

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
		line    string
	)
	for scanner.Scan() {
		line = scanner.Text()
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	parts := strings.Split(line, ",")
	ranges := make([]Range, len(parts))
	maxNumberLen := 0
	maxNumber := 0
	for i, p := range parts {
		r := strings.Split(p, "-")
		from, _ := strconv.Atoi(r[0])
		to, _ := strconv.Atoi(r[1])
		ranges[i].From = from
		ranges[i].To = to

		if len(r[0]) > maxNumberLen {
			maxNumberLen = len(r[0])
		}
		if len(r[1]) > maxNumberLen {
			maxNumberLen = len(r[1])
		}
		if from > maxNumber {
			maxNumber = from
		}
		if to > maxNumber {
			maxNumber = to
		}
	}

	max, _ := strconv.Atoi(strings.Repeat(fmt.Sprintf("%d", 9), maxNumberLen/2))
	candidateIDs := pregenerateIDs(max, 2, maxNumber)
	solve(ranges, candidateIDs)

	candidateIDsB := pregenerateIDs(max, 10, maxNumber)
	solve(ranges, candidateIDsB)
}

type Range struct {
	From, To int
}

func pregenerateIDs(max, count int, maxVal int) []int {
	rMap := make(map[int]bool)

	for i := 1; i <= max; i++ {
		for j := 2; j <= count; j++ {
			n, _ := strconv.Atoi(strings.Repeat(fmt.Sprintf("%d", i), j))
			if n > maxVal {
				break
			}
			rMap[n] = true
		}
	}

	res := make([]int, 0, len(rMap))
	for k, _ := range rMap {
		res = append(res, k)
	}
	slices.Sort(res)

	return res
}

func solve(ranges []Range, candidateIDs []int) {
	var result int

	for _, r := range ranges {
		for _, id := range candidateIDs {
			if id > r.To {
				break
			}
			if id >= r.From {
				result += id
			}
		}
	}

	fmt.Println(result)
}
