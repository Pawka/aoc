use regex::Regex;
use std::fs;

fn main() {
    let filename = "input.txt";
    let lines = fs::read_to_string(filename).expect("Can't read file");

    part_a(&lines);
}

#[derive(Copy, Clone, Debug)]
struct Claim {
    id: usize,
    left: usize,
    top: usize,
    width: usize,
    height: usize,
}

const SIZE: usize = 1000;
type Matrix = [[u8; SIZE]; SIZE];

fn part_a(contents: &String) {
    let re = Regex::new(r"^#(?P<id>\d+) @ (\d+),(\d+): (\d+)x(\d+)").unwrap();
    let claims: Vec<Claim> = contents.lines().map(|line| parse(&line, &re)).collect();
    let mut matrix: Matrix = [[0; SIZE]; SIZE];
    for claim in &claims {
        fill(&mut matrix, &claim);
    }
    let total = matrix.iter().flatten().filter(|x| **x > 1 as u8).count();
    println!("Day03(a): {}", total);
}

fn parse(line: &str, re: &Regex) -> Claim {
    let cap = re.captures(line).unwrap();
    Claim {
        id: cap[1].parse().unwrap(),
        left: cap[2].parse().unwrap(),
        top: cap[3].parse().unwrap(),
        width: cap[4].parse().unwrap(),
        height: cap[5].parse().unwrap(),
    }
}

fn fill(matrix: &mut Matrix, claim: &Claim) {
    for i in 0..claim.height {
        for j in 0..claim.width {
            matrix[claim.top + i][claim.left + j] += 1;
        }
    }
}
