use std::collections::{HashMap, HashSet};
use std::fs;

fn main() {
    let filename = "input.txt";
    part_a(&filename)
}

fn part_a(filename: &str) {
    let contents = fs::read_to_string(filename).expect("Can't read the file");
    let counts: Vec<i32> = contents
        .lines()
        .map(|l| {
            let mut hm = HashMap::new();
            for c in l.chars() {
                let value = match hm.get(&c) {
                    Some(value) => *value + 1,
                    None => 1,
                };
                hm.insert(c, value);
            }
            let mut res = HashSet::new();
            for v in hm.values() {
                if res.len() == 2 {
                    break;
                }
                if *v == 2 || *v == 3 {
                    res.insert(v.clone());
                }
            }
            res
        })
        .flatten()
        .collect();

    let twos = counts.iter().filter(|x| **x == 2).count();
    let threes = counts.len() - twos;
    println!("Day02(A): {}", twos * threes);
}
