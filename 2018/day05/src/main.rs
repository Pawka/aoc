use std::collections::VecDeque;
use std::fs;

// DIFF defines the difference between uppercase and lowercase chars such as 'A' - 'a'.
const DIFF: isize = 32;

fn main() {
    let filename = "input.txt";
    let input = fs::read_to_string(&filename).expect("Can't read file");
    println!("Day05(a): {}", solve_a(&input));
    println!("Day05(b): {}", solve_b(&input));
}

fn solve_a(input: &String) -> usize {
    let mut stack: VecDeque<isize> = VecDeque::new();
    for c in input.trim().chars() {
        let val = c as isize;
        match stack.is_empty() {
            true => stack.push_back(val),
            false => {
                match DIFF == isize::abs(val - stack.back().unwrap()) {
                    true => {
                        stack.pop_back();
                    }
                    false => stack.push_back(val),
                };
            }
        };
    }
    stack.len()
}

fn solve_b(input: &String) -> usize {
    let mut min = usize::MAX;
    for i in 'a'..('z' as u8 + 1) as char {
        let modified = input
            .clone()
            .trim()
            .replace(i, "")
            .replace((i as u8 - DIFF as u8) as char, "");
        let reacted = solve_a(&modified);
        if reacted < min {
            min = reacted;
        }
    }
    min
}
