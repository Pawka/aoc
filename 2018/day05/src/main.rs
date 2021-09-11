use std::collections::VecDeque;
use std::fs;

// DIFF defines the difference between uppercase and lowercase chars such as 'A' - 'a'.
const DIFF: isize = 32;

fn main() {
    let filename = "input.txt";
    let input = fs::read_to_string(&filename).expect("Can't read file");
    solve_a(&input);
}

fn solve_a(input: &String) {
    let mut stack: VecDeque<isize> = VecDeque::new();
    for c in input.trim().chars() {
        let val = c as isize;
        match stack.is_empty() {
            true => stack.push_back(val),
            false => {
                if DIFF == isize::abs(val - stack.back().unwrap()) {
                    stack.pop_back();
                } else {
                    stack.push_back(val);
                };
            }
        };
    }
    println!("Day05(a): {}", stack.len());
}
