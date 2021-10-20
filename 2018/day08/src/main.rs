use std::fs;

fn main() {
    let filename = "input.txt";
    let input = fs::read_to_string(filename).expect("can't read file");
    let numbers: Vec<i32> = input
        .split_whitespace()
        .map(|x| x.parse().unwrap())
        .collect();
    solve_a(&numbers);
    solve_b(&numbers);
}

fn solve_a(numbers: &Vec<i32>) {
    let mut childs = Vec::new();
    let mut meta = Vec::new();
    let mut sum: i32 = 0;
    let mut iter = numbers.iter();
    while let Some(n) = iter.next() {
        childs.push(*n);
        meta.push(iter.next().unwrap());

        while let Some(0) = childs.last() {
            let m = meta.pop().unwrap();
            sum += iter.by_ref().take(*m as usize).sum::<i32>();
            childs.pop();
        }

        if let Some(n) = childs.last_mut() {
            *n -= 1;
        }
    }

    println!("Day08(a): {}", sum);
}

#[derive(Debug)]
struct Node {
    id: i32,
    childs: Vec<i32>,
    metadata: Vec<i32>,
}

impl Node {
    fn new(id: i32) -> Node {
        Node {
            id: id,
            childs: Vec::new(),
            metadata: Vec::new(),
        }
    }
}

struct Ids {
    stack: Vec<i32>,
    max: i32,
}

impl Ids {
    fn new() -> Ids {
        Ids {
            stack: Vec::new(),
            max: 0,
        }
    }

    fn next(&mut self) -> i32 {
        self.max += 1;
        self.stack.push(self.max);
        self.max
    }

    fn pop(&mut self) -> Option<i32> {
        self.stack.pop()
    }

    fn peek(&self) -> Option<&i32> {
        self.stack.last()
    }
}

#[test]
fn ids_test() {
    let mut ids = Ids::new();
    assert_eq!(None, ids.pop());
    assert_eq!(1, ids.next());
    assert_eq!(2, ids.next());
    assert_eq!(3, ids.next());
    assert_eq!(Some(3), ids.pop());
    assert_eq!(4, ids.next());
}

fn solve_b(numbers: &Vec<i32>) {
    let mut childs = Vec::new();
    let mut meta = Vec::new();
    let mut iter = numbers.iter();
    let mut nodes: Vec<Node> = Vec::new();
    let mut ids = Ids::new();
    while let Some(n) = iter.next() {
        childs.push(*n);
        meta.push(iter.next().unwrap());

        let node = Node::new(ids.next());
        nodes.push(node);

        while let Some(0) = childs.last() {
            let m = meta.pop().unwrap();
            let id = ids.pop().unwrap();

            nodes
                .get_mut(id as usize - 1)
                .unwrap()
                .metadata
                .extend(iter.by_ref().take(*m as usize));
            childs.pop();
            if let Some(parent) = ids.peek() {
                nodes.get_mut(*parent as usize - 1).unwrap().childs.push(id);
            }
        }

        if let Some(n) = childs.last_mut() {
            *n -= 1;
        }
    }

    println!("Day08(b): {}", get_sum(&nodes, 0));
}

fn get_sum(nodes: &Vec<Node>, i: usize) -> i32 {
    let node = nodes.get(i).unwrap();
    if node.childs.len() == 0 {
        return node.metadata.iter().sum();
    }

    let mut sum: i32 = 0;
    for m in &node.metadata {
        if *m as usize <= node.childs.len() {
            sum += get_sum(nodes, node.childs[*m as usize - 1] as usize - 1);
        }
    }

    sum
}
