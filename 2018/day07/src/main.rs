use regex::Regex;
use std::collections::{HashMap, HashSet};
use std::fs;

fn main() {
    let filename = "input.txt";
    let input = fs::read_to_string(filename).expect("can't read file");
    solve(&input);
}

fn solve(input: &String) {
    let re = Regex::new(r"^Step (.) must be finished before step (.) can begin.$").unwrap();

    let mut childs: HashMap<char, HashSet<char>> = HashMap::new();
    let mut dependencies: HashMap<char, HashSet<char>> = HashMap::new();

    for ch in 'A'..='Z' {
        dependencies.insert(ch, HashSet::new());
        childs.insert(ch, HashSet::new());
    }
    for line in input.lines() {
        let c = re.captures(line).unwrap();
        let from = c[1].parse().unwrap();
        let to = c[2].parse().unwrap();

        dependencies.get_mut(&to).unwrap().insert(from);
        childs.get_mut(&from).unwrap().insert(to);
    }

    let mut queue: Vec<char> = Vec::new();
    for (ch, d) in &dependencies {
        if d.len() == 0 {
            queue.push(*ch);
        }
    }

    let mut result = String::new();
    loop {
        queue.sort();
        if queue.len() == 0 {
            break;
        }
        let current = queue[0];
        queue.remove(0);

        for child in childs.get(&current).unwrap() {
            let deps = dependencies.get_mut(&child).unwrap();
            deps.remove(&current);

            if deps.len() == 0 {
                queue.push(*child);
            }
        }

        result.push(current);
    }
    println!("Day07(a): {}", result);
}
