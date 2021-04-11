-----------------------------------
-- FLP 2021 - bkg-2-cnf
-- Bc. Marian Kapisinsky, xkapis00
-- 11.4.2021
-----------------------------------

module Chomsky (createCNF, readNts) where

import Data.Char
import Data.List

import Types

-- Read all nonterminals for the CNF
readNts :: [Rule] -> [Nonterminal]
readNts r = nub $ map (readNt) r
  where
    readNt r = (left r)

-- Go through the gives set of rules and create the Chomsky Normal Form
createCNF :: [Rule] -> [Rule]
createCNF [] = []
createCNF (r:rs)
  | isOneNt (right r) = error "Please remove simple rules"
  | isTwoNt (right r) || isOneTerm (right r) = [r] ++ createCNF rs
  | otherwise = create (left r) (right r) ++ createCNF rs
  where
    create :: Nonterminal -> [Symbol] -> [Rule]
    create nt [x,y]
      | isTerm x && isTerm y = (Rule nt ((createFromT x)++(createFromT y))) :
                               (Rule (createFromT x) [x]) :
                               (Rule (createFromT y) [y]) : []
      | isTerm x = (Rule nt ((createFromT x)++[y])) :
                    (Rule (createFromT x) [x]) : []
      | isTerm y = (Rule nt ([x]++(createFromT y))) :
                    (Rule (createFromT y) [y]) : []
      | otherwise = (Rule nt ([x]++[y])) : []
    create nt (x:xs)
      | isTerm x = (Rule nt ((createFromT x) ++ (createFromS xs))) :
                    (Rule (createFromT x) [x]):
                    create (createFromS xs) xs
      | otherwise = (Rule nt ([x] ++ (createFromS xs))) :
                    create (createFromS xs) xs
    create _ _ = []

-- Create new nonterminal for given terminal    
createFromT :: Terminal -> Nonterminal
createFromT x = [x] ++ "'"

-- Create new nonterminal for given symbols
createFromS :: [Symbol] -> Nonterminal
createFromS x = "<" ++ x ++ ">"
