use std::collections::{HashMap, HashSet};
use std::fs;

fn main() {
    let filename = "input.txt";
    part_a(&filename);
    part_b(&filename);
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

fn part_b(filename: &str) {
    let contents = fs::read_to_string(filename).expect("Can't read the file");
    let lines: Vec<String> = contents.lines().map(|x| x.to_string()).collect();
    let id = find_id(lines).expect("id not found");
    println!("Day02(B): {}", id);
}

fn find_id(lines: Vec<String>) -> Option<String> {
    let mut result = String::new();
    let mut i = 0;
    for line1 in &lines {
        for line2 in lines.iter().skip(i) {
            if compare(&line1, &line2) {
                let mut j = 0;
                let ch2 = line2.chars();
                for ch in line1.chars() {
                    if ch == ch2.clone().nth(j).unwrap() {
                        result.push(ch);
                    }
                    j += 1;
                }
                return Some(result);
            }
        }
        i += 1;
    }

    None
}

fn compare(str1: &String, str2: &String) -> bool {
    let mut diff = 0;
    let mut i = 0;
    let ch2 = str2.chars();

    for ch in str1.chars() {
        if ch != ch2.clone().nth(i).unwrap() {
            diff += 1;
        }
        if diff > 1 {
            break;
        }
        i += 1;
    }

    match diff {
        1 => true,
        _ => false,
    }
}

#[test]
fn compare_test() {
    assert!(!compare(&String::from("asdf"), &String::from("asdf")));
    assert!(!compare(&String::from("ab"), &String::from("ab")));
    assert!(compare(&String::from("aaa"), &String::from("aba")));
}
