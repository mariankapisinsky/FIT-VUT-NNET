/**
 * @file Binary Tree Module Tests - WAP 2022 /
 * Tested on Node.js version 17.6.0
 * @author xkapis00
 */

// Import the file system lib for file manipulation.
import * as fs from "fs";

// Import the created lib for binary trees.
import { Tree } from "./tree.mjs";

/**
 * Comparison function of two given arrays.
 * @param {any} a first array
 * @param {any} b second array
 * @returns true, if arrays are equal, false otherwise
 */

function equals ( a, b ) {

    var eq = function ( a, b ) {
        return a.every( function(value, index) {
            return value === b[index];
        });
    };

    return a.length === b.length ? eq ( a, b ) : false;
}

/**
 * Obtains preorder traversal of a given binary tree
 * and compares it to the ground truth data.
 * @param t a binary tree
 * @param gt ground truth data
 */

function preorder ( t, gt ) {

    let output = Array();

    for ( let n of t.preorder() ) {
        output.push(n);
    }

    if ( equals(output, gt) ) {
        console.log("[OK] Preorder passed");
    }
    else {
        console.log("[FAIL] Preorder failed");
    }
}

/**
 * Obtains inorder traversal of a given binary tree
 * and compares it to the ground truth data.
 * @param t a binary tree
 * @param gt ground truth data
 */

function inorder ( t, gt ) {

    let output = Array();

    for ( let n of t.inorder() ) {
        output.push(n);
    }

    if ( equals( output, gt ) ) {
        console.log("[OK] Inorder passed");
    }
    else {
        console.log("[FAIL] Inorder failed");
    }
}

/**
 * Obtains postorder traversal of a given binary tree
 * and compares it to the ground truth data.
 * @param t a binary tree
 * @param gt ground truth data
 */

function postorder ( t, gt ) {

    let output = Array();

    for ( let n of t.postorder() ) {
        output.push(n);
    }

    if ( equals( output, gt ) ) {
        console.log("[OK] Postorder passed");
    }
    else {
        console.log("[FAIL] Postorder failed");
    }
}

/**
 * Obtains two preorder traversal generators
 * and compares a mix of them to the ground truth data.
 * @param t a binary tree
 * @param gt ground truth data
 */

function mix ( t, gt ) {

    let output = Array();

    let pre1 = t.preorder();

    let pre2 = t.preorder();

    output.push( pre1.next().value );
    output.push( pre1.next().value );
    output.push( pre2.next().value );
    output.push( pre1.next().value );
    output.push( pre2.next().value );
    output.push( pre2.next().value );
    output.push( pre1.next().value );

    if ( equals( output, gt ) ) {
        console.log("[OK] Mix passed");
    }
    else {
        console.log("[FAIL] Mix failed");
    }
}

/**
 * This function reads input files one by one,
 * creates trees and compares preorder, inorder,
 * and postorder traversals to given ground truth files.
 * @param files input files with data
 */

function run ( files ) {
    
    files.forEach( function ( ifile ) {

        const input = fs.readFileSync( ifile, "utf-8" ).split(",").map(Number);

        let filename = ifile.slice(0, -3);
        let ofile = filename + ".out";

        const output = fs.readFileSync( ofile, "utf-8" ).split("\n");
        
        console.log("[TEST] Test file: " + filename)

        let t = new Tree ( (a,b) => a < b );

        input.forEach( i => t.insertValue( i ) );

        if ( output[0].trim() === "mix" ) {

            let mixOutput = output[1].split(",").map(Number);

            mix ( t, mixOutput );
        }
        else {

            let preorderOutput = output[1].split(",").map(Number);

            let inorderOutput = output[3].split(",").map(Number);

            let postorderOutput = output[5].split(",").map(Number);

            preorder ( t, preorderOutput );

            inorder ( t, inorderOutput );

            postorder ( t, postorderOutput );
        }

    });
}

const inputs = process.argv.slice(2); // read files from command line

run( inputs );