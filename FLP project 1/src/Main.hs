-----------------------------------
-- FLP 2021 - bkg-2-cnf
-- Bc. Marian Kapisinsky, xkapis00
-- 11.4.2021
-----------------------------------

module Main (main) where

import System.Environment (getArgs)
import System.Exit
import System.IO
import Data.Char
import Data.List

import Types
import Parser
import Simple
import Chomsky

main :: IO ()
main = do
  (action, input) <- parseArgs =<< getArgs
  case parseInput input of
    Left e -> do
      print e
      death "Error"
    Right r -> action r
  
parseArgs :: [String] -> IO (Grammar -> IO (), String)
parseArgs [x] = parseArgs [x, ""]
parseArgs [x,xs] = do
  input <- if null xs then getContents else readFile xs
  case x of
    "-i" -> return (printUCFG, input)
    "-1" -> return (printMCFG, input)
    "-2" -> return (printCNF, input)
    _    -> death ("Unkown option " ++ x)
parseArgs _ = death "Expecting two arguments: {-i|-1|-2} FILE"

-- PRINT UNCHANGED CFG

printUCFG :: Grammar -> IO ()
printUCFG grammar = do
  putStrLn $ show grammar
  
-- PRINT MODIFIED CFG (WITHOUT SIMPLE RULES)

printMCFG :: Grammar -> IO ()
printMCFG grammar = do
  let mGrammar = Grammar (nonterminals grammar)
                         (terminals grammar)
                         (startN grammar)
                         (removeSimple (nonterminals grammar) (rules grammar))
  putStrLn $ show mGrammar
  
-- PRINT CFG IN CHOMSKY NORMAL FORM

printCNF :: Grammar -> IO ()
printCNF grammar = do
  let cnfRules = nub $ createCNF (rules grammar)
  let mGrammar = Grammar (readNts cnfRules)
                         (terminals grammar)
                         (startN grammar)
                         (cnfRules)
  putStrLn $ show mGrammar
  
-- DEATH / DIE
-- death is the die function of base-4.8.0.0 package
-- which is yet not included in the package version
-- currently installed on the school server

death :: String -> IO a
death err = hPutStrLn stderr err >> exitFailure