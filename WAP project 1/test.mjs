/**
 * Binary Tree Module Tests - WAP 2022
 * @author xkapis00
 * @file test.mjs
 */

import * as fs from "fs";

import { Tree } from "./tree.mjs";

function equals ( a, b ) {
    return a.length === b.length && a.every((v, i) => v === b[i]);
}

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

const inputs = process.argv.slice(2);

run( inputs );