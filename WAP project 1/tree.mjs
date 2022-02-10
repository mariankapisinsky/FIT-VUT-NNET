/**
 * Binary Tree Module - WAP 2022
 * @author xkapis00
 * @file tree.mjs
 */

export { Tree };

/**
 * Node class.
 * @constructor
 * @param {any} value value to be stored in this node
 */ 

function Node ( value ) {
    this.left = null;
    this.right = null;
    this.value = value;
}

/**
 * Tree class.
 * @constructor
 * @param {function} compare comparison function
 */ 

function Tree ( compare ) {
    this.root = null;
    this.compare = compare;
}

/**
 * Insert value into the tree.
 * @param {any} value a value to be inserted
 */

Tree.prototype.insertValue = function ( value ) {

    this.root = this.insert ( this.root, value )
}

/**
 * Helper function for recursive value insert into the tree.
 * @param {any} node a node to insert to
 * @param {any} value a value to be inserted into a new node
 */

Tree.prototype.insert = function ( node, value ) {

    if ( !node ) {
        return new Node ( value );
    }

    if ( this.compare( value, node.value ) ) {
        node.left = this.insert ( node.left, value )
    }
    else {
        node.right = this.insert ( node.right, value )
    }

    return node;
} 

/**
 * Preorder traversal.
 * @returns a generator for iterable preorder traversal
 */ 

Tree.prototype.preorder = function* () {

    var preorderIterator = function* preorderIterator ( node ) {
        if ( node ) {
            yield node.value;
            yield* preorderIterator ( node.left );
            yield* preorderIterator ( node.right );
        }
    }

    yield* preorderIterator ( this.root )
}

/**
 * Inorder traversal.
 * @returns a generator for iterable inorder traversal
 */ 

Tree.prototype.inorder = function* () {

    var inorderIterator = function* inorderIterator ( node ) {
        if ( node ) {
            yield* inorderIterator ( node.left );
            yield node.value;
            yield* inorderIterator ( node.right );
        }
    }

    yield* inorderIterator ( this.root )
}

/**
 * Postorder traversal.
 * @returns a generator for iterable postorder traversal
 */ 

Tree.prototype.postorder = function* () {

    var postorderIterator = function* postorderIterator ( node ) {
        if ( node ) {
            yield* postorderIterator ( node.left );
            yield* postorderIterator ( node.right );
            yield node.value;
        }
    }

    yield* postorderIterator ( this.root )
}
