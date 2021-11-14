fn main() {
    println!("Day14.a: {}", solve_a(513401));
    println!("Day14.b: {}", solve_b("513401"));
    // println!("Day14.b: {}", solve_b(51589));
}

fn solve_a(number: usize) -> String {
    let mut receipes: Vec<usize> = vec![3, 7];

    let mut e1: usize = 0;
    let mut e2: usize = 1;

    for _ in 0..number + 10 {
        receipes.extend(get_new_receipes(receipes[e1] + receipes[e2]));
        e1 = (e1 + receipes[e1] + 1) % receipes.len();
        e2 = (e2 + receipes[e2] + 1) % receipes.len();
    }
    receipes
        .iter()
        .skip(number)
        .take(10)
        .map(|x| x.to_string())
        .collect::<Vec<String>>()
        .join("")
}

fn get_new_receipes(input: usize) -> Vec<usize> {
    match input < 10 {
        true => vec![input],
        false => vec![input / 10, input % 10],
    }
}

#[test]
fn get_new_receipes_test() {
    assert_eq!(vec![9], get_new_receipes(9));
    assert_eq!(vec![1, 9], get_new_receipes(19));
}

fn solve_b(number: &str) -> usize {
    let mut receipes: Vec<usize> = vec![3, 7];
    let mut e1: usize = 0;
    let mut e2: usize = 1;

    let want = number.to_string();

    loop {
        let ext = get_new_receipes(receipes[e1] + receipes[e2]);
        receipes.extend(ext);
        e1 = (e1 + receipes[e1] + 1) % receipes.len();
        e2 = (e2 + receipes[e2] + 1) % receipes.len();

        let end: String = receipes
            .iter()
            .rev()
            .take(number.to_string().len() + 1)
            .rev()
            .fold(String::new(), |mut acc, x| {
                acc.push_str(&x.to_string());
                acc
            });

        if want == end.get(1..).unwrap() {
            return receipes.len() - want.len();
        }
        if let Some(_end) = end.get(..5) {
            if want == _end {
                return receipes.len() - want.len() - 1;
            }
        };
    }
}

#[test]
fn solve_b_test() {
    assert_eq!(9, solve_b("51589"));
    assert_eq!(5, solve_b("01245"));
    assert_eq!(18, solve_b("92510"));
    assert_eq!(2018, solve_b("59414"));
}
