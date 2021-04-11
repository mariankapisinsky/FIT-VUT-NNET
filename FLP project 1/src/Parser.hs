-----------------------------------
-- FLP 2021 - bkg-2-cnf
-- Bc. Marian Kapisinsky, xkapis00
-- 11.4.2021
-----------------------------------

module Parser (parseInput) where

import Control.Applicative ((<$>), (<*>), (<$), (<*), (<|>))
import Control.Monad ((<=<))
import Text.Parsec
import Text.Parsec.String (Parser)

import Types

comma :: Parser Char
comma = char ','

arrow :: Parser String
arrow = string "->"

parseInput :: String -> Either ParseError Grammar
parseInput = parse parseCFG ""

parseCFG :: Parser Grammar
parseCFG = Grammar <$> nonterminalsP <* newline
                   <*> terminalsP <* newline
                   <*> (many1 upper) <* newline
                   <*> rulesP

nonterminalsP :: Parser [Nonterminal]
nonterminalsP = sepBy1 (many1 upper) comma

terminalsP :: Parser [Terminal]
terminalsP = sepBy1 lower comma

rulesP :: Parser [Rule]
rulesP = endBy ruleP newline

ruleP :: Parser Rule
ruleP = Rule <$> (many1 upper) <* arrow <*> many1 letter
