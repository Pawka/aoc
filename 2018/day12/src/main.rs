use std::collections::HashMap;
use std::fs;

const TARGET_A: i32 = 20;
const TARGET_B: i64 = 5_0000_000_000;

fn main() {
    let filename = "input.txt";
    let content = fs::read_to_string(filename).expect("can't read file");

    let mut lines = content.lines();
    let initial = lines
        .next()
        .unwrap()
        .strip_prefix("initial state: ")
        .unwrap();

    lines.next();

    let rules: HashMap<&str, char> = lines
        .map(|line| {
            let parts: Vec<&str> = line.split(" => ").collect();
            (parts[0], parts[1].chars().next().unwrap())
        })
        .collect();

    solve(initial, &rules, TARGET_A, TARGET_B);
}

fn solve(input: &str, rules: &HashMap<&str, char>, target_iter_a: i32, target_iter_b: i64) {
    let mut shift = 0;
    let mut current = input.to_string();
    shift += grow(&mut current);

    let mut avg = Vec::with_capacity(1000);
    let mut last_sum = 0;
    let mut delta = 0.0;
    let target_it = 1000;
    for it in 1..=100000 {
        let len = current.len();
        let mut s = String::with_capacity(len);
        s.push_str("..");
        for i in 2..len - 2 {
            let part = &current[i - 2..=i + 2];
            if let Some(v) = rules.get(part) {
                s.push(*v);
            } else {
                s.push('.');
            }
        }
        current = s;
        shift += grow(&mut current);
        let sum = sum(&current, shift);
        if it == target_iter_a {
            println!("Day12(a): {}", sum);
        }
        if last_sum != 0 {
            avg.push(sum - last_sum);
        }
        last_sum = sum;
        if it % 500 == 0 {
            let s: i32 = avg.iter().sum();
            delta = f64::from(s) / avg.len() as f64;
            if it == target_it {
                break;
            }
            avg.clear();
        }
    }

    println!(
        "Day12(b): {}",
        (delta as i64 * (target_iter_b - target_it as i64)) + last_sum as i64
    );
}

fn sum(input: &String, shift: i32) -> i32 {
    let mut sum = 0;
    for (k, c) in input.chars().enumerate() {
        if c == '#' {
            sum += k as i32 - shift;
        }
    }
    sum
}

fn grow(input: &mut String) -> i32 {
    let mut shift = 0;
    if &input[0..3] != "..." {
        input.insert_str(0, "...");
        shift = 3;
    }
    if !input.ends_with("...") {
        input.push_str("...");
    }
    shift
}
