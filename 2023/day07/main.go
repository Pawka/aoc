package main

import (
	"fmt"
	"sort"
	"strconv"
	"strings"

	"github.com/Pawka/aoc/2023/pkg"
)

const input = "input.txt"

func main() {
	var (
		lines  = pkg.ReadLines(input)
		handsA = make([]Hand, 0, len(lines))
		handsB = make([]Hand, 0, len(lines))
	)
	for _, l := range lines {
		handsA = append(handsA, NewHand(l))
		handsB = append(handsB, NewHand(l))
	}

	sort.Slice(handsA, func(i, j int) bool {
		var (
			hv1 = HandValue(handsA[i].counts)
			hv2 = HandValue(handsA[j].counts)
		)
		if hv1 != hv2 {
			return hv1 < hv2
		}

		for k := 0; k < 5; k++ {
			var (
				cv1 = cardValue(rune(handsA[i].cards[k]), false)
				cv2 = cardValue(rune(handsA[j].cards[k]), false)
			)
			if cv1 == cv2 {
				continue
			}
			return cv1 < cv2
		}

		return false
	})

	sort.Slice(handsB, func(i, j int) bool {
		var (
			hv1 = JokerHandValue(handsB[i].distinct)
			hv2 = JokerHandValue(handsB[j].distinct)
		)
		if hv1 != hv2 {
			return hv1 < hv2
		}

		for k := 0; k < 5; k++ {
			var (
				cv1 = cardValue(rune(handsB[i].cards[k]), true)
				cv2 = cardValue(rune(handsB[j].cards[k]), true)
			)
			if cv1 == cv2 {
				continue
			}
			return cv1 < cv2
		}

		return false
	})

	fmt.Println(result(handsA))
	fmt.Println(result(handsB))
}

func result(hands []Hand) int {
	res := 0
	for i, h := range hands {
		res += (i + 1) * h.bid
	}
	return res
}

func cardValue(in rune, joker bool) int {
	switch in {
	case 'A':
		return 20
	case 'K':
		return 19
	case 'Q':
		return 18
	case 'J':
		if joker {
			return 0
		}
		return 17
	case 'T':
		return 16
	default:
		val, _ := strconv.Atoi(string(in))
		return val
	}
}

type Hand struct {
	cards    string
	bid      int
	distinct map[rune]int
	counts   map[int]int
}

func NewHand(line string) Hand {
	var (
		fields = strings.Split(line, " ")
		bid, _ = strconv.Atoi(fields[1])
		hand   = Hand{
			cards:    fields[0],
			bid:      bid,
			distinct: map[rune]int{},
			counts:   map[int]int{},
		}
	)

	for _, r := range hand.cards {
		hand.distinct[r]++
	}
	for _, c := range hand.distinct {
		hand.counts[c]++
	}

	return hand
}

const (
	FiveOfKind  = 7
	FourOfKind  = 6
	FullHouse   = 5
	ThreeOfKind = 4
	TwoPair     = 3
	OnePair     = 2
	HighCard    = 1
)

func HandValue(counts map[int]int) int {
	if counts[5] == 1 {
		return FiveOfKind
	}
	if counts[4] == 1 {
		return FourOfKind
	}
	if counts[3] == 1 && counts[2] == 1 {
		return FullHouse
	}
	if counts[3] == 1 && counts[1] == 2 {
		return ThreeOfKind
	}
	if counts[2] == 2 {
		return TwoPair
	}
	if counts[2] == 1 && counts[1] == 3 {
		return OnePair
	}
	return HighCard
}

func JokerHandValue(distinct map[rune]int) int {
	var (
		maxK   rune
		maxV   = 0
		cp     = make(map[rune]int)
		counts = make(map[int]int)
	)
	for k, v := range distinct {
		if k == 'J' {
			continue
		}
		cp[k] = v
		if v > maxV {
			maxK = k
			maxV = v
		}
	}
	cp[maxK] += distinct['J']
	for _, c := range cp {
		counts[c]++
	}
	return HandValue(counts)
}
