package main

import (
	"bufio"
	"fmt"
	"log"
	"math"
	"os"
	"slices"
	"strconv"
	"strings"
	"sync"
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

	solve(lines)
}

type Range struct {
	DestinationFrom, SourceFrom, Lenght int
}

func solve(lines []string) {
	var (
		seeds   []string
		ranges  = make(map[string][]Range)
		current string
	)
	lines = append(lines, "")
	for i, line := range lines {
		if i == 0 {
			seeds = strings.Fields(strings.TrimPrefix(line, "seeds: "))
			continue
		}
		if line == "" {
			current = ""
			continue
		}
		if current == "" {
			current = strings.Split(line, " ")[0]
			ranges[current] = make([]Range, 0, 10)
			continue
		}

		var (
			f       = strings.Fields(line)
			from, _ = strconv.Atoi(f[0])
			to, _   = strconv.Atoi(f[1])
			l, _    = strconv.Atoi(f[2])
		)
		ranges[current] = append(ranges[current], Range{from, to, l})
	}

	partASeeds := make([]int, 0, len(seeds))
	for _, seed := range seeds {
		s, _ := strconv.Atoi(seed)
		partASeeds = append(partASeeds, s)
	}

	fmt.Println(findMin(partASeeds, ranges))

	resB := make([]int, 0, len(seeds)/2)
	mux := sync.Mutex{}
	wg := sync.WaitGroup{}
	fmt.Printf("Total threads: %d\n", len(seeds)/2)
	for i := 0; i < len(seeds); i += 2 {
		wg.Add(1)
		go func(i int) {
			defer wg.Done()
			from, _ := strconv.Atoi(seeds[i])
			l, _ := strconv.Atoi(seeds[i+1])
			to := from + l
			m := findMinRange(from, to, ranges)
			mux.Lock()
			defer mux.Unlock()
			resB = append(resB, m)
			fmt.Printf("Thread %d:\t%d\t%d\t%d\n", i/2, from, to, m)
		}(i)
	}
	wg.Wait()
	fmt.Println(slices.Min(resB))
}

func findMin(seeds []int, ranges map[string][]Range) int {
	m := math.MaxInt
	for _, seed := range seeds {
		p := findLoc(seed, "seed-to-soil", ranges)
		if p < m {
			m = p
		}
	}

	return m
}

func findMinRange(from, to int, ranges map[string][]Range) int {
	m := math.MaxInt
	for i := from; i < to; i++ {
		p := findLoc(i, "seed-to-soil", ranges)
		if p < m {
			m = p
		}
	}

	return m
}

var links = map[string]string{
	"seed-to-soil":            "soil-to-fertilizer",
	"soil-to-fertilizer":      "fertilizer-to-water",
	"fertilizer-to-water":     "water-to-light",
	"water-to-light":          "light-to-temperature",
	"light-to-temperature":    "temperature-to-humidity",
	"temperature-to-humidity": "humidity-to-location",
}

func findLoc(in int, current string, ranges map[string][]Range) int {
	p := findPos(in, ranges[current])
	if current == "humidity-to-location" {
		return p
	}

	return findLoc(p, links[current], ranges)
}

func findPos(seed int, ranges []Range) int {
	for _, r := range ranges {
		if seed >= r.SourceFrom && seed < r.SourceFrom+r.Lenght {
			return seed - r.SourceFrom + r.DestinationFrom
		}
	}
	return seed
}
