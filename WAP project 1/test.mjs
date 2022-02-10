/**
 * Binary Tree Module Tests - WAP 2022
 * @author xkapis00
 * @file test.mjs
 */

import { Tree } from "./tree.mjs";

function preorder ( t ) {

    console.log("preorder")
    for (let n of t.preorder()) {
        console.log(n);
    }
}

function inorder ( t ) {

    console.log("inorder")
    for (let n of t.inorder()) {
        console.log(n);
    }
}

function postorder ( t ) {

    console.log("postorder")
    for (let n of t.postorder()) {
        console.log(n);
    }
}

function run ( inputs ) {
    
    inputs.forEach( function (input) {

        let t = new Tree ( (a,b) => a < b );

        input.forEach(i => t.insertValue(i));
        
        preorder(t);

        inorder(t);

        postorder(t);

    });
}

let input = [5, 7, 2131345646, 9, 4, 13, 12415486];
let input1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
let input2 = [377, 603, 158, 55, 21, 44, 583, 35, 534, 435];

let inputs = [input, input1, input2]

run( inputs )