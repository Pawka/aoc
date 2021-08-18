use std::collections::HashSet;
use std::fs;

fn main() {
    let filename = "input.txt";
    part_a(&filename);
    part_b(&filename);
}

fn part_a(filename: &str) {
    let contents = fs::read_to_string(filename).expect("Can't read the file.");
    let res = contents
        .lines()
        .map(|l| l.parse::<i32>().unwrap())
        .fold(0, |a, b| a + b);

    println!("Day01(A): {}", res);
}

fn part_b(filename: &str) {
    let contents = fs::read_to_string(filename).expect("Can't read the file.");
    let numbers = contents.lines().map(|l| l.parse::<i32>().unwrap()).cycle();

    let mut hm = HashSet::new();
    let mut freq = 0;

    for n in numbers {
        freq = freq + n;
        if hm.contains(&freq) {
            break;
        }
        hm.insert(freq);
    }
    println!("Day01(B): {}", freq);
}
