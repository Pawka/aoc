use std::collections::HashSet;
use std::convert::From;
use std::fs;

type Grid = Vec<Vec<Cell>>;

fn main() {
    let filename = "input.txt";
    let content = fs::read_to_string(filename).expect("can't read file");

    let mut carts: Vec<Cart> = Vec::new();
    let grid: Grid = content
        .lines()
        .enumerate()
        .map(|(y, line)| {
            line.chars()
                .enumerate()
                .map(|(x, cell)| match cell {
                    'v' | '^' | '<' | '>' => {
                        carts.push(Cart::new((x, y), cell));
                        Cell::from(cell)
                    }
                    _ => Cell::from(cell),
                })
                .collect::<Vec<Cell>>()
        })
        .collect();

    let mut positions = HashSet::new();
    loop {
        let mut crash: HashSet<(usize, usize)> = HashSet::new();
        for cart in &mut carts {
            let pos = (cart.x, cart.y);
            if crash.contains(&pos) {
                continue;
            }
            positions.remove(&pos);
            cart.ride(&grid);
            if positions.insert((cart.x, cart.y)) == false {
                crash.insert((cart.x, cart.y));
            }
        }
        if !crash.is_empty() {
            println!("{:?}", crash);
            carts.retain(|&c| !crash.contains(&(c.x, c.y)));
            positions.retain(|&c| !crash.contains(&(c.0, c.1)));
            if positions.len() == 1 {
                println!("{:?}", positions);
                return;
            }
        }

        carts.sort_by(|a, b| {
            if a.y == b.y {
                return a.x.cmp(&b.x);
            }
            a.y.cmp(&b.y)
        });
    }
}

#[derive(Debug, Copy, Clone)]
enum Cell {
    Empty,
    Vertical,
    Horizontal,
    Intersection,
    Slash,
    Backslash,
}

impl From<char> for Cell {
    fn from(item: char) -> Self {
        match item {
            '/' => Cell::Slash,
            '\\' => Cell::Backslash,
            '|' | 'v' | '^' => Cell::Vertical,
            '-' | '>' | '<' => Cell::Horizontal,
            '+' => Cell::Intersection,
            _ => Cell::Empty,
        }
    }
}

use self::Direction::*;

#[derive(Debug, Clone, Copy, PartialEq)]
enum Direction {
    Up,
    Down,
    Left,
    Right,
    Straight,
}

impl Direction {
    fn next(self) -> Direction {
        match self {
            Up => Right,
            Right => Down,
            Down => Left,
            Left => Up,
            _ => {
                panic!("unknown direction");
            }
        }
    }
    fn prev(self) -> Direction {
        match self {
            Up => Left,
            Right => Up,
            Down => Right,
            Left => Down,
            _ => {
                panic!("unknown direction");
            }
        }
    }

    fn next_turn(self) -> Direction {
        match self {
            Left => Straight,
            Straight => Right,
            Right => Left,
            _ => {
                panic!("unknown turn");
            }
        }
    }
}

#[test]
fn direction_test() {
    let val = Up;
    assert_eq!(Left, val.prev());
    assert_eq!(Right, val.next());
    assert_eq!(Down, val.next().next());
}

#[derive(Debug, Clone, Copy)]
struct Cart {
    x: usize,
    y: usize,
    direction: Direction,
    turn: Direction,
}

impl Cart {
    fn new(pos: (usize, usize), face: char) -> Self {
        Self {
            x: pos.0,
            y: pos.1,
            direction: match face {
                '>' => Right,
                '<' => Left,
                'v' => Down,
                '^' => Up,
                _ => panic!("Unknown direction"),
            },
            turn: Left,
        }
    }

    fn ride(&mut self, grid: &Grid) {
        let current = grid[self.y][self.x];
        let next = match current {
            Cell::Intersection => {
                let direction = match self.turn {
                    Left => self.direction.prev(),
                    Right => self.direction.next(),
                    Straight => self.direction,
                    _ => panic!("unknown turn: {:?}", self.turn),
                };
                let cell = match direction {
                    Up | Down => Cell::Vertical,
                    Left | Right => Cell::Horizontal,
                    _ => panic!("unknown direction: {:?}", direction),
                };
                self.turn = self.turn.next_turn();
                next_cell(self.x, self.y, cell, direction)
            }
            _ => next_cell(self.x, self.y, current, self.direction),
        };
        self.x = next.0 .0;
        self.y = next.0 .1;
        self.direction = next.1;
    }
}

fn next_cell(
    x: usize,
    y: usize,
    current: Cell,
    direction: Direction,
) -> ((usize, usize), Direction) {
    match (current, direction) {
        (Cell::Horizontal, Right) | (Cell::Backslash, Down) | (Cell::Slash, Up) => {
            ((x + 1, y), Right)
        }
        (Cell::Horizontal, Left) | (Cell::Backslash, Up) | (Cell::Slash, Down) => {
            ((x - 1, y), Left)
        }
        (Cell::Vertical, Up) | (Cell::Slash, Right) | (Cell::Backslash, Left) => ((x, y - 1), Up),
        (Cell::Vertical, Down) | (Cell::Slash, Left) | (Cell::Backslash, Right) => {
            ((x, y + 1), Down)
        }
        (_, _) => {
            panic!(
                "unsuported ride ({}, {}): {:?} {:?}",
                x, y, current, direction
            );
        }
    }
}
