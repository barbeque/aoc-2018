fn hunnets(power_level: i32) -> i32 {
    let x = power_level.to_string();
    if x.len() < 3 {
        return 0;
    }
    x.chars().rev().nth(2).unwrap().to_string().parse::<i32>().unwrap()
}

fn sum_square(cells: &[[i32; 300]; 300], x: usize, y: usize, w: usize) -> i32 {
    let mut s = 0;
    for dx in 0..w {
        if x + dx >= 300 {
            continue;
        }

        for dy in 0..w {
            if y + dy >= 300 {
                continue;
            }

            s += cells[y + dy][x + dx];
        }
    }
    s
}

fn main() {
    assert_eq!(hunnets(0), 0);
    assert_eq!(hunnets(5), 0);
    assert_eq!(hunnets(45), 0);
    assert_eq!(hunnets(12345), 3);
    assert_eq!(hunnets(128), 1);

    let serial_number = 1309;

    let mut cells = [ [0; 300]; 300];

    for x in 1..301usize {
        for y in 1..301usize {
            let rack_id = x as i32 + 10;
            let mut power_level : i32 = rack_id * y as i32;
            power_level += serial_number;
            power_level *= rack_id;
            // keep only the hundreds digit of the power level
            power_level = hunnets(power_level);
            power_level -= 5;

            cells[y - 1][x - 1] = power_level
        }
    }

    let mut best_power = 0;
    let mut best_coord = (0usize, 0usize, 0usize);

    // now we have the cells
    for sq_size in 0..300 {
        println!("Square size = {}", sq_size);
        for x in 0..300usize {
            for y in 0..300usize {
                let total_power = sum_square(&cells, x, y, sq_size);
                if total_power > best_power {
                    best_power = total_power;
                    best_coord = (x, y, sq_size);
                    println!("\tNew best power = {} at coord = {},{},{}", best_power, best_coord.0 + 1, best_coord.1 + 1, best_coord.2);
                }
            }
        }
    }

    println!("Best power = {} at coord = {},{},{}", best_power, best_coord.0 + 1, best_coord.1 + 1, best_coord.2);
}
