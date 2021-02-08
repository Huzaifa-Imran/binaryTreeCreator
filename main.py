from binaryTreeCreator import *


def takeInput():
    global answer
    print("[1] Create a Binary Tree using inorder and preorder strings.")
    print("[2] Create a Binary Tree using inorder and postorder strings.")
    print("[3] Create a Binary Tree using array string.")
    print("[4] Create a BST.")
    print("[5] Create an Expression Tree.")
    print("[6] Create Huffman Tree.")
    while(True):
        answer = input("Enter your choice: ")
        if answer == '1' or answer == '2':
            print("\nEnter the strings with each character separated by spaces.")
            inorder = input("In Order string: ").split()
            if answer == '1':
                preorder = input("Pre Order string: ").split()
                root = subtreeFinder(True, inorder, preorder)
            else:
                postorder = input("Post Order string: ").split()
                root = subtreeFinder(False, inorder, postorder)
            break
        elif answer == '3' or answer == '4':
            if answer == '3':
                print(
                    "\nEnter the string with each character separated by spaces. Use -1 as a character to represent no node.")
                array = input("String: ").split()
                root = staticTree(array)
            else:
                print("\nEnter the string with each number separated by spaces.")
                try:
                    array = [int(x) for x in input("String: ").split()]
                except ValueError:
                    print("BST can only contain numbers! Exiting...")
                    exit()
                root = createBST(array)
            break
        elif answer == '5':
            expression = input("Expression: ")
            root = expressionTree(expression)
            break
        elif answer == '6':
            text = input("Enter text to compress: ")
            root = huffmanTree(text)
            break
        else:
            print("Invalid choice!")

    print('\n', root)
    return root


def applyOperations(root: Node):
    if root == None:
        print("Tree is empty. Exiting...")
        exit()
    print("'preorder'  ->  Print Preorder string")
    print("'inorder'   ->  Print Inorder string")
    print("'postorder' ->  Print Postorder string")
    print("'static'    ->  Print static array")
    print("'maxheap'   ->  Convert tree to max heap")
    print("'minheap'   ->  Convert tree to min heap")
    print("'exit'      ->  Exit the program")
    while(True):
        choice = input("\nEnter your choice: ")
        if choice.lower() == "preorder":
            print(
                f"Preorder string = {' '.join(root.preorder())}")
        elif choice.lower() == "inorder":
            print(
                f"Inorder string = {' '.join(root.inorder())}")
        elif choice.lower() == "postorder":
            print(
                f"Postorder string = {' '.join(root.postorder())}")
        elif choice.lower() == "static":
            array = root.staticArray()
            print(
                f"Static array[{len(array)}] = {' '.join(array)}")
        elif choice.lower() == "maxheap":
            root = heapifyTree(root, True)
        elif choice.lower() == "minheap":
            root = heapifyTree(root, False)
        elif choice.lower() == "exit":
            break
        else:
            print("\nInvalid Choice!")


def main():
    root = takeInput()
    applyOperations(root)


if __name__ == '__main__':
    main()
