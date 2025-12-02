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
	}

	max, _ := strconv.Atoi(strings.Repeat(fmt.Sprintf("%d", 9), maxNumberLen/2))
	candidateIDs := pregenerateIDs(max)

	solve(ranges, candidateIDs)
}

type Range struct {
	From, To int
}

func pregenerateIDs(max int) []int {
	res := make([]int, 0, 10)

	for i := 1; i <= max; i++ {
		n, _ := strconv.Atoi(fmt.Sprintf("%d%d", i, i))
		res = append(res, n)
	}

	return res
}

func solve(ranges []Range, candidateIDs []int) {

	var (
		resultA = 0
	)

	for _, r := range ranges {
		fmt.Println(r.To, "-", r.From)
		for _, id := range candidateIDs {
			if id > r.To {
				break
			}
			if id >= r.From {
				fmt.Println(id)
				resultA += id
			}
		}
	}

	fmt.Println(resultA)
}
