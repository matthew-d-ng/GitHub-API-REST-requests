{-# LANGUAGE StandaloneDeriving #-}

module Main where

import Test.HUnit
import Test.Framework as TF (defaultMain, testGroup, Test)
import Test.Framework.Providers.HUnit (testCase)
import Test.Framework.Providers.QuickCheck2 (testProperty)

import GithubREST

{- HUnit Tests -}

test_hello =  hello @?= "hello this is working B)"

{- QuickCheck Tests -}


main = defaultMain tests

tests :: [TF.Test]
tests = [ testGroup "\nPlaceholder Test" [
            testCase "Main works so far" test_hello
          ]
        ]
