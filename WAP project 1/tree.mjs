/**
 * Binary Tree Module - WAP 2022
 * @author xkapis00
 * @file tree.mjs
 */

export { Tree };

/**
 * Tree class.
 * @constructor
 * @param {function} compare Comparison function
 */ 

function Tree (compare) {
    this.root = null;
    this.compare = compare;
}