/**
 * Binary Tree Module Tests - WAP 2022
 * @author xkapis00
 * @file test.mjs
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

    return a.length === b.length ? eq( a, b ) : false;
}

/**
 * Obtains preorder traversal of a given binary tree
 * and compares it to the ground truth data
 * @param t a binary tree
 * @param gt ground truth data
 */

function preorder ( t, gt ) {

    let output = Array();

    for (let n of t.preorder()) {
        output.push(n);
    }

    if (equals(output, gt)) {
        console.log("[OK] Preorder passed");
    }
    else {
        console.log("[FAIL] Preorder failed");
    }
}

/**
 * Obtains inorder traversal of a given binary tree
 * and compares it to the ground truth data
 * @param t a binary tree
 * @param gt ground truth data
 */

function inorder ( t, gt ) {

    let output = Array();

    for (let n of t.inorder()) {
        output.push(n);
    }

    if (equals(output, gt)) {
        console.log("[OK] Inorder passed");
    }
    else {
        console.log("[FAIL] Inorder failed");
    }
}

/**
 * Obtains postorder traversal of a given binary tree
 * and compares it to the ground truth data
 * @param t a binary tree
 * @param gt ground truth data
 */

function postorder ( t, gt ) {

    let output = Array();

    for (let n of t.postorder()) {
        output.push(n);
    }

    if (equals(output, gt)) {
        console.log("[OK] Postorder passed");
    }
    else {
        console.log("[FAIL] Postorder failed");
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

        let preorderOutput = output[1].split(",").map(Number);

        let inorderOutput = output[3].split(",").map(Number);

        let postorderOutput = output[5].split(",").map(Number);

        let t = new Tree ( (a,b) => a < b );

        input.forEach( i => t.insertValue( i ) );
        
        preorder( t, preorderOutput );

        inorder( t, inorderOutput );

        postorder( t, postorderOutput );

    });
}

const inputs = process.argv.slice(2); // read files from command line

run( inputs );