use std::fs;

fn main() {
    let filename = "input.txt";
    part_a(&filename);
}

fn part_a(filename: &str) {
    let contents = fs::read_to_string(filename).expect("Can't read the file.");

    let iter = contents.lines();
    let mut res = 0;
    for line in iter {
        let prefixes: &[_] = &['-', '+'];
        let num_str = line.trim_start_matches(prefixes);
        let num: i32 = num_str.parse().unwrap();
        let op = line.chars().nth(0).unwrap();
        if op == '+' {
            res = res + num
        } else {
            res = res - num
        }
    }

    println!("Day01(A): {}", res);
}
