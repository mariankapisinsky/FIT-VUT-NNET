-----------------------------------
-- FLP 2021 - bkg-2-cnf
-- Bc. Marian Kapisinsky, xkapis00
-- 11.4.2021
-----------------------------------

{-# LANGUAGE RecordWildCards #-}
module Types where

import Data.Char
import Data.List

type Symbol = Char
type Nonterminal = [Symbol]
type Terminal = Symbol

data Rule = Rule
  { left :: Nonterminal
  , right :: [Symbol]
  } deriving (Eq)
  
instance Show Rule where
  show (Rule left right) = intercalate "->" [left, right]

data Grammar = Grammar
  { nonterminals :: [Nonterminal]
  , terminals :: [Terminal]
  , startN :: Nonterminal
  , rules :: [Rule]
  } deriving (Eq)
  
instance Show Grammar where
  show Grammar{..} = unlines $ [intercalate "," nonterminals, intersperse  ',' terminals, startN] ++ map show rules
  
-- Some useful functions

isTerm :: Symbol -> Bool
isTerm x = isLower x

isOneTerm :: [Symbol] -> Bool
isOneTerm [x] = isLower x
isOneTerm _ = False

isOneNt :: [Symbol] -> Bool
isOneNt [x] = isUpper x
isOneNt _ = False

isTwoNt :: [Symbol] -> Bool
isTwoNt [x,y] = isUpper x && isUpper y
isTwoNt _ = False

  