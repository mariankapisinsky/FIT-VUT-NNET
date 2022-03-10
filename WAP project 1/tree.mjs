/**
 * @file Binary Tree Module - WAP 2022
 * @author xkapis00
 */

export { Tree };

/**
 * Empty Tree constructor.
 * @constructor
 * @param {function} compare comparison function
 */

function EmptyTree ( compare ) {

    this.cmp = compare;

    /**
     * Create a tree from and empty tree.
     * @param {any} value a value to be inserted
     */

    EmptyTree.prototype.insertValue = function ( value ) {

        this.value = value;

        this.left = new EmptyTree( this.cmp );

        this.right = new EmptyTree( this.cmp );

        Object.setPrototypeOf( this, Tree.prototype );
    }
}

/**
 * Tree constructor.
 * @constructor
 * @param {function} compare comparison function
 */

function Tree ( compare ) { 
    
    return new EmptyTree( compare );
}

/**
 * Insert value into the tree.
 * @param {any} value a value to be inserted
 */

Tree.prototype.insertValue = function ( value ) {

    if ( this.cmp( value, this.value) ) {
        
        this.left.insertValue( value );
    }
    else {

        this.right.insertValue( value );
    }
}

/**
 * Preorder traversal.
 * @returns a generator for iterable preorder traversal
 */
 
Tree.prototype.preorder = function () {
        
    var preorderIterator = function* ( tree ) {
                
        if (tree.value) yield tree.value;
        if (tree.left) yield* preorderIterator ( tree.left );
        if (tree.right) yield* preorderIterator ( tree.right );
    }
            
    return preorderIterator ( this );
}

/**
 * Inorder traversal.
 * @returns a generator for iterable inorder traversal
 */ 

Tree.prototype.inorder = function () {
        
    var inorderIterator = function* ( tree ) {
                
        if (tree.left) yield* inorderIterator ( tree.left );
        if (tree.value) yield tree.value;
        if (tree.right) yield* inorderIterator ( tree.right );
    }
        
    return inorderIterator ( this );
}

/**
 * Postorder traversal.
 * @returns a generator for iterable postorder traversal
 */ 

 Tree.prototype.postorder = function () {
        
    var postorderIterator = function* ( tree ) {

        if (tree.left) yield* postorderIterator ( tree.left );
        if (tree.right) yield* postorderIterator ( tree.right );
        if (tree.value) yield tree.value;
    }
        
    return postorderIterator ( this );
}
