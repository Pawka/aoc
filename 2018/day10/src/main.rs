#[macro_use]
extern crate lazy_static;

use regex::Regex;
use std::collections::HashSet;
use std::fs;

lazy_static! {
    static ref RE: Regex = Regex::new(r"^position=<([^,]+), ([^>]+)> velocity=<([^,]+),([^>]+)>$")
        .expect("Error parsing regex");
}

#[derive(Debug, Clone, Copy)]
struct Point {
    x: i32,
    y: i32,
    vx: i32,
    vy: i32,
}

impl Point {
    fn new(line: &str) -> Point {
        let captures = RE.captures(line).ok_or("line do not match").unwrap();
        Point {
            x: captures[1].trim().parse::<i32>().unwrap(),
            y: captures[2].trim().parse::<i32>().unwrap(),
            vx: captures[3].trim().parse::<i32>().unwrap(),
            vy: captures[4].trim().parse::<i32>().unwrap(),
        }
    }

    fn migrate(&mut self) {
        self.x += self.vx;
        self.y += self.vy;
    }

    fn unmigrate(&mut self) {
        self.x -= self.vx;
        self.y -= self.vy;
    }
}

#[test]
fn point_new_test() {
    let line = "position=<-31138,  10302> velocity=< 3, -1>";
    let p = Point::new(line);
    assert_eq!(-31138, p.x);
    assert_eq!(10302, p.y);
    assert_eq!(3, p.vx);
    assert_eq!(-1, p.vy);
}

#[test]
fn point_migrate_test() {
    let mut p = Point {
        x: 10,
        y: 20,
        vx: -2,
        vy: 2,
    };

    p.migrate();
    assert_eq!(8, p.x);
    assert_eq!(22, p.y);
}

fn main() {
    let filename = "input.txt";
    let points: Vec<Point> = fs::read_to_string(filename)
        .expect("can't read file")
        .lines()
        .map(|l| Point::new(l))
        .collect();

    solve(points.clone().as_mut());
}

fn solve(points: &mut Vec<Point>) {
    let mut last = i32::MAX;
    let mut sec = 0;
    loop {
        let min_y = *points.iter().min_by_key(|y| y.y).unwrap();
        let max_y = *points.iter().max_by_key(|y| y.y).unwrap();
        let delta = i32::abs(max_y.y - min_y.y);
        if delta > last {
            sec -= 1;
            break;
        }
        last = delta;

        for p in points.iter_mut() {
            p.migrate();
        }
        sec += 1;
    }

    for p in points.iter_mut() {
        p.unmigrate();
    }
    print(points);
    println!("Seconds: {}", sec);
}

fn print(points: &mut Vec<Point>) {
    points.sort_by(|a, b| {
        if a.y == b.y {
            return a.x.cmp(&b.x);
        }
        a.y.cmp(&b.y)
    });

    let hs: HashSet<(i32, i32)> = points.iter().map(|p| (p.x, p.y)).collect();
    let min_y = *points.iter().min_by_key(|p| p.y).unwrap();
    let max_y = *points.iter().max_by_key(|p| p.y).unwrap();
    let min_x = *points.iter().min_by_key(|p| p.x).unwrap();
    let max_x = *points.iter().max_by_key(|p| p.x).unwrap();

    for y in min_y.y..=max_y.y {
        for x in min_x.x..=max_x.x {
            if hs.contains(&(x, y)) {
                print!("X");
            } else {
                print!(".");
            }
        }
        print!("\n");
    }
}
