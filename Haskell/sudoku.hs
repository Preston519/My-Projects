type Grid = [[Int]]

possibilities:: Grid -> [[[Int]]]
possibilities = map (map f)
    where f 0 = [1..9]
          f n = [n]

mergesort:: [Int] -> [Int]
mergesort xs = merge ls rs
    where (ls, rs) = splitAt (length xs `div` 2) xs

merge:: [Int] -> [Int] -> [Int]
merge [] ys = ys
merge xs [] = xs
merge (x:xs) (y:ys) | x <= y = x:merge xs (y:ys)
                    | otherwise = y:merge (x:xs) ys