import Data.Char (digitToInt)
type Grid a = [[a]]

test :: [[Int]]
test = [
        [0,1,2],
        [2,0,0],
        [1,2,3]
    ]

example = "2....1.38\n........5\n.7...6...\n.......13\n.981..257\n31....8..\n9..8...2.\n.5..69784\n4..25....\n"

parseSudoku:: String -> Grid Int
parseSudoku = map f . lines
    where f [] = []
          f ('.':xs) = 0:f xs
          f (x:xs) = digitToInt x : f xs

showPossibilities:: Grid [Int] -> String
showPossibilities = unlines . map (map f)
    where f [x] = head (show x)
          f _ = '.'

fullNaiveSolve:: String -> IO ()
fullNaiveSolve = putStrLn . unlines . map showPossibilities . naiveSolve . possibilities . parseSudoku

naiveSolve:: Grid [Int] -> [Grid [Int]]
naiveSolve xss | complete xss = [xss]
               | not (valid xss) = []
               | otherwise = concat [naiveSolve (pruneGrid (replace i j [n] xss)) | n <- xss !! i !! j]
        where (i, j) = getMinSlot xss

showCompleted:: Grid [Int] -> Grid Int
showCompleted = map (map head)

printIt = putStrLn


possibilities:: Grid Int -> Grid [Int]
possibilities = map (map f)
    where f 0 = [1..9]
          f n = [n]

possible:: [[[Int]]] -> Bool
possible = all ([] `notElem`)

minIndex:: [[Int]] -> (Int, Int)
minIndex = foldr f (-1, 10)
    where f xs (i, l) | length xs < l && length xs /= 1 = (0, length xs)
                      | otherwise = (i+1, l)

getMinSlot:: [[[Int]]] -> (Int, Int)
getMinSlot = fst . f
    where f [] = ((-1, -1), 10)
          f (xs:xss) | snd (minIndex xs) < snd (f xss) = ((0, fst (minIndex xs)), snd (minIndex xs))
                     | otherwise = let ((a, b), c) = f xss in ((a+1, b), c)

nodups:: [Int] -> Bool
nodups = f . mergesort
    where f [] = True
          f [_] = True
          f (x0:x1:xs) = x0 /= x1 && f (x1:xs)

prune:: [[Int]] -> [[Int]]
prune xss = [if length xs == 1 then xs else filter (`notElem` nums) xs | xs <- xss]
    where nums = [x | xs <- xss, length xs == 1, x <- xs]

cols:: [[a]] -> [[a]]
cols = foldr (zipWith (:)) (repeat [])

boxes:: [[a]] -> [[a]]
boxes = concatMap (foldr (zipWith (++)) (repeat [])) . split3 . map split3

split3:: [a] -> [[a]]
split3 xs | length xs < 3 = []
          | otherwise = l : split3 r
    where (l, r) = splitAt 3 xs

pruneGrid:: Grid [Int] -> Grid [Int]
pruneGrid = boxes . map prune . boxes . cols . map prune . cols . map prune

expand:: (Int, Int) -> Grid [Int] -> [Grid [Int]]
expand (i, j) xsss = [replace i j [x] xsss | x <- xsss !! i !! j]

replace:: Int -> Int -> a -> Grid a -> Grid a
replace 0 0 x ((y:ys):yss) = (x:ys):yss
replace 0 j x ((y:ys):yss) = (y : head (replace 0 (j-1) x (ys:yss))) : tail (replace 0 (j-1) x (ys:yss))
replace i j x (ys:yss) = ys : replace (i-1) j x yss

valid:: Grid [Int] -> Bool
valid = not . any (any null)

complete:: Grid [Int] -> Bool
complete = all (all (\x -> length x == 1))


mergesort:: [Int] -> [Int]
mergesort [] = []
mergesort [x] = [x]
mergesort xs = merge (mergesort ls) (mergesort rs)
    where (ls, rs) = splitAt (length xs `div` 2) xs

isSorted:: [Int] -> Bool
isSorted [] = True
isSorted [x] = True
isSorted (x0:x1:xs) = x0 <= x1 && isSorted (x1:xs)

merge:: [Int] -> [Int] -> [Int]
merge [] ys = ys
merge xs [] = xs
merge (x:xs) (y:ys) | x <= y = x:merge xs (y:ys)
                    | otherwise = y:merge (x:xs) ys