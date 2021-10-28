fn main() {
    solve(7347);
}

fn solve(serial: i32) {
    let mut points: Vec<i32> = Vec::new();
    let size = 300;

    for x in 1..=size {
        for y in 1..=size {
            points.push(power(serial, (x, y)));
        }
    }

    let mut max = 0;
    let mut coord = (0, 0, 0);

    for grid_size in 3..300 {
        println!("Grid size: {}", grid_size);
        for y in 0..size - grid_size {
            for x in 0..size - grid_size {
                let mut sum = 0;
                for j in 0..grid_size {
                    for k in 0..grid_size {
                        sum += points[(x + j + y * size + k * size) as usize];
                    }
                }
                if sum > max {
                    max = sum;
                    coord = (y + 1, x + 1, grid_size);
                }
            }
        }
        println!("Power: {}, {:?}", max, coord);
    }
    println!("Power: {}, {:?}", max, coord);
}

fn power(serial: i32, cell: (i32, i32)) -> i32 {
    ((cell.0 + 10) * cell.1 + serial) * (cell.0 + 10) % 1000 / 100 - 5
}

#[test]
fn power_test() {
    assert_eq!(4, power(8, (3, 5)));
    assert_eq!(-5, power(57, (122, 79)));
    assert_eq!(0, power(39, (217, 196)));
    assert_eq!(4, power(71, (101, 153)));
}
