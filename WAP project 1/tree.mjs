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
    this.value = value;
    this.left = null;
    this.right = null;
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
 * @param {any} value value
 */ 

Tree.prototype.insertValue = function( value ) {

    var node = new Node( value );

    if ( !this.root ) {
        this.root = node;
    }
    else {
        
        var current = this.root;
    
        while (current) {
            if ( this.compare( node.value, current.value ) ) {
                if (!current.left) {
                    current.left = node;
                    break;
                }
                else {
                    current = current.left;
                }
            }
            else {
                if (!current.right) {
                    current.right = node;
                    break;
                }
                else {
                    current = current.right;
                }
            }
        }
    }
}

/**
 * Preorder traversal.
 * @returns a generator for iterable preorder traversal
 */ 

Tree.prototype.preorder = function* () {

    var preorderIterator = function* preorderIterator(node) {
        if(node) {
            yield node.value;
            yield* preorderIterator(node.left);
            yield* preorderIterator(node.right);
        }
    }

    yield* preorderIterator(this.root)
}

/**
 * Inorder traversal.
 * @returns a generator for iterable inorder traversal
 */ 

Tree.prototype.inorder = function* () {

    var inorderIterator = function* inorderIterator(node) {
        if(node) {
            yield* inorderIterator(node.left);
            yield node.value;
            yield* inorderIterator(node.right);
        }
    }

    yield* inorderIterator(this.root)
}

/**
 * Postorder traversal.
 * @returns a generator for iterable postorder traversal
 */ 

Tree.prototype.postorder = function* () {

    var postorderIterator = function* postorderIterator(node) {
        if(node) {
            yield* postorderIterator(node.left);
            yield* postorderIterator(node.right);
            yield node.value;
        }
    }

    yield* postorderIterator(this.root)
}
