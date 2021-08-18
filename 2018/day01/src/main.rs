use std::fs;

fn main() {
    let filename = "input.txt";
    part_a(&filename);
}

fn part_a(filename: &str) {
    let contents = fs::read_to_string(filename).expect("Can't read the file.");
    let res = contents
        .lines()
        .map(|l| l.parse::<i32>().unwrap())
        .fold(0, |a, b| a + b);

    println!("Day01(A): {}", res);
}
