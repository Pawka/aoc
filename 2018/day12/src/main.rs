use std::collections::HashMap;
use std::fs;

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

    solve_a(initial, &rules);
}

fn solve_a(input: &str, rules: &HashMap<&str, char>) {
    let mut shift = 0;
    let mut current = input.to_string();
    shift += grow(&mut current);
    println!("{:#?}", rules);
    println!("{}", current);

    for _ in 0..20 {
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
        println!("{}", current);
    }
    let mut sum = 0;
    for (k, c) in current.chars().enumerate() {
        if c == '#' {
            sum += k as i32 - shift;
        }
    }
    println!("{:?}", sum);
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
