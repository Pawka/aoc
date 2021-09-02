use regex::Regex;
use std::collections::HashSet;
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
type Matrix = [[isize; SIZE]; SIZE];

const FREE_CELL: isize = 0;
const OVERLAP_CELL: isize = -1;

fn part_a(contents: &String) {
    let re = Regex::new(r"^#(?P<id>\d+) @ (\d+),(\d+): (\d+)x(\d+)").unwrap();
    let mut matrix: Matrix = [[FREE_CELL; SIZE]; SIZE];
    let mut set = HashSet::new();

    contents
        .lines()
        .map(|line| parse(&line, &re))
        .for_each(|claim| fill(&mut matrix, &mut set, &claim));

    println!(
        "Day03(a): {}",
        matrix.iter().flatten().filter(|x| **x < 0).count()
    );
    println!("Day03(b): {}", set.iter().nth(0).unwrap());
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

fn fill(matrix: &mut Matrix, set: &mut HashSet<usize>, claim: &Claim) {
    set.insert(claim.id);
    for i in 0..claim.height {
        for j in 0..claim.width {
            match matrix[claim.top + i][claim.left + j] {
                FREE_CELL => matrix[claim.top + i][claim.left + j] = claim.id as isize,
                OVERLAP_CELL => {
                    set.remove(&claim.id);
                }
                _ => {
                    set.remove(&claim.id);
                    set.remove(&(matrix[claim.top + i][claim.left + j] as usize));
                    matrix[claim.top + i][claim.left + j] = OVERLAP_CELL;
                }
            };
        }
    }
}
