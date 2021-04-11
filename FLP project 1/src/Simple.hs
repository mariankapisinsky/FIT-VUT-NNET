-----------------------------------
-- FLP 2021 - bkg-2-cnf
-- Bc. Marian Kapisinsky, xkapis00
-- 11.4.2021
-----------------------------------

module Simple (removeSimple) where

import Data.Char
import Data.List

import Types

removeSimple :: [Nonterminal] -> [Rule] -> [Rule]
removeSimple nt rules = remove rules []
  where
    remove :: [Rule] -> [Rule] -> [Rule]
    remove [] new = new
    remove (r:rs) new
      | not (isSimpleRule r) = remove rs $ nub (new ++ [r] ++ (createRules (rules ++ new) (getNonterminals (rules ++ new) (left r) nt)))
      | otherwise = remove rs new
      
createRules :: [Rule] -> [Nonterminal] -> [Rule]
createRules rules nt = foldl (\list r -> list ++ createRule rules r) [] (get nt)
  where get = foldl (\list n -> list ++ getRulesByRight rules n) []
  
createRule :: [Rule] -> Rule -> [Rule]
createRule rules rule = map (Rule (left rule) . right) (filter (\(Rule l r) -> l == (right rule) && not (isOneNt r)) rules)

getNonterminals :: [Rule] -> Nonterminal -> [Nonterminal] -> [Nonterminal]
getNonterminals _ _ [] = []
getNonterminals rules n (nt:nts)
  | n `elem` (reachablesFromN rules nt) = nt : getNonterminals rules n nts
  | otherwise = getNonterminals rules n nts

isSimpleRule :: Rule -> Bool
isSimpleRule rule = isOneNt (right rule)
  
reachablesFromN :: [Rule] -> Nonterminal -> [Nonterminal]
reachablesFromN rules start = reachables [start] []
  where
    reachables :: [Nonterminal] -> [Nonterminal] -> [Nonterminal]
    reachables [] _ = []
    reachables (nt:nts) seen
      | nt `elem` seen = reachables nts seen
      | otherwise = nt : reachables ((getReachables (getRulesByLeft rules nt)) ++ nts) (nt:seen)
    
getRulesByLeft :: [Rule] -> Nonterminal -> [Rule]
getRulesByLeft rules nt = filter (\(Rule l r) -> l == nt && isOneNt r) rules

getRulesByRight :: [Rule] -> Nonterminal -> [Rule]
getRulesByRight rules nt = filter (\(Rule _ r) -> r == nt && isOneNt r) rules

getReachables :: [Rule] -> [Nonterminal]
getReachables [] = []
getReachables (r:rs) = nub $ convert2nt (right r) ++ getReachables rs
  
convert2nt :: [Symbol] -> [Nonterminal]
convert2nt s = [s]
