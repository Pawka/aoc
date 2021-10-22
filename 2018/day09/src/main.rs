fn main() {
    assert_eq!(32, solve(9, 25));
    assert_eq!(8317, solve(10, 1618));
    assert_eq!(146373, solve(13, 7999));

    println!("Day09(a): {}", solve(476, 71657));
    println!("Day09(b): {}", solve(476, 71657 * 100));
}

fn solve(players: usize, max: usize) -> usize {
    let mut left = vec![0 as usize; max + 1];
    let mut right = vec![0 as usize; max + 1];
    let mut scores = vec![0 as usize; players];

    let mut marble = 1;
    let mut current = 0;
    let mut player = 0;
    while marble <= max {
        if marble % 23 == 0 {
            scores[player] += marble;
            for _ in 0..7 {
                current = left[current];
            }
            scores[player] += current;
            let r = right[current];
            let l = left[current];
            right[l] = r;
            left[r] = l;
            current = r;
        } else {
            // insert
            current = right[current];
            right[marble] = right[current];
            left[marble] = current;
            right[current] = marble;
            left[right[marble]] = marble;
            current = marble;
        }

        marble += 1;
        player = (player + 1) % players;
    }

    *scores.iter().max().unwrap()
}
