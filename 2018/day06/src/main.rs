#[macro_use]
extern crate lazy_static;
use regex::Regex;
use std::collections::HashSet;
use std::fs;

fn main() {
    let filename = "input.txt";
    let input: String = fs::read_to_string(filename).expect("can't open file");
    let points = parse(&input);
    solve(&points);
}

#[derive(Debug)]
struct Point {
    x: usize,
    y: usize,
}

fn parse(input: &String) -> Vec<Point> {
    lazy_static! {
        static ref RE: Regex = Regex::new(r"(\d+), (\d+)").unwrap();
    }
    input
        .trim()
        .lines()
        .map(|line| {
            let l = RE.captures(line).unwrap();
            Point {
                x: l[1].parse().unwrap(),
                y: l[2].parse().unwrap(),
            }
        })
        .collect::<Vec<Point>>()
}

#[derive(Clone, Debug, Hash)]
enum Field {
    None,
    Point(usize),
}

fn solve(points: &Vec<Point>) {
    let max_x = points
        .iter()
        .max_by(|a, b| a.x.cmp(&b.x))
        .map(|p| p.x)
        .unwrap()
        + 1;
    let max_y = points
        .iter()
        .max_by(|a, b| a.y.cmp(&b.y))
        .map(|p| p.y)
        .unwrap()
        + 1;

    let mut counts = vec![0; points.len()];
    let mut matrix = vec![vec![Field::None; max_x]; max_y];
    let mut inf_points = HashSet::new();
    let mut within_distance = 0;
    for y in 0..max_y {
        for x in 0..max_x {
            matrix[y][x] = nearest(x, y, &points);
            if near(x, y, &points, 10000) {
                within_distance += 1;
            }
            if let Field::Point(point) = matrix[y][x] {
                counts[point as usize] += 1;
                if x == 0 || y == 0 || x == max_x - 1 || y == max_y - 1 {
                    inf_points.insert(point);
                }
            }
        }
    }

    println!(
        "Day06(a): {}",
        counts
            .iter()
            .enumerate()
            .filter(|(k, _)| !inf_points.contains(k))
            .map(|(_, v)| v)
            .max()
            .unwrap()
    );

    println!("Day06(b): {}", within_distance);
}

fn nearest(x: usize, y: usize, points: &Vec<Point>) -> Field {
    let mut min = usize::MAX;
    let mut nearest = Field::None;
    let mut min_count = 0;
    for (key, p) in points.iter().enumerate() {
        if p.x == x && p.y == y {
            return Field::Point(key);
        }
        let dist = (isize::abs(p.x as isize - x as isize) + isize::abs(p.y as isize - y as isize))
            as usize;
        if dist == min {
            min_count += 1;
        }
        if dist < min {
            min = dist;
            min_count = 1;
            nearest = Field::Point(key);
        }
    }

    match min_count {
        1 => nearest,
        _ => Field::None,
    }
}

fn near(x: usize, y: usize, points: &Vec<Point>, limit: usize) -> bool {
    let mut distance = 0;
    for p in points.iter() {
        distance += (isize::abs(p.x as isize - x as isize) + isize::abs(p.y as isize - y as isize))
            as usize;

        if distance >= limit {
            return false;
        }
    }
    true
}
