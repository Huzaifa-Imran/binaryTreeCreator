class Node():
    def __init__(self, value):
        self.value = self.val = value
        self.left = None
        self.right = None

    def __str__(self):
        lines = _build_tree_string(self, 0, False, '-')[0]
        return '\n' + '\n'.join((line.rstrip() for line in lines))

    def __len__(self):  
        current_level = [self]
        size = 0
        while len(current_level) > 0:
            next_level = []
            for node in current_level:
                size += 1
                if node.left is not None:
                    next_level.append(node.left)
                if node.right is not None:
                    next_level.append(node.right)
            
            current_level = next_level
        return size

    def inorder(self):
        result = ""
        stack = []
        node = self

        while node or stack:
            while node:
                stack.append(node)
                node = node.left
            if stack:
                node = stack.pop()
                result += str(node.value) + " " 
                node = node.right

        return result

    def preorder(self):
        result = ""
        stack = [self]

        while stack:
            node = stack.pop()
            if node:
                result += str(node.value) + " "
                stack.append(node.right)
                stack.append(node.left)

        return result

    def postorder(self):
        result = ""
        stack = [self]

        while stack:
            node = stack.pop()
            if node:
                result += " " + str(node.value)
                stack.append(node.left)
                stack.append(node.right)

        return result[::-1]

def _build_tree_string(root, curr_index, index=False, delimiter='-'):
    if root is None:
        return [], 0, 0, 0

    line1 = []
    line2 = []
    if index:
        node_repr = '{}{}{}'.format(curr_index, delimiter, root.val)
    else:
        node_repr = str(root.val)

    new_root_width = gap_size = len(node_repr)

    # Get the left and right sub-boxes, their widths, and root repr positions
    l_box, l_box_width, l_root_start, l_root_end = \
        _build_tree_string(root.left, 2 * curr_index + 1, index, delimiter)
    r_box, r_box_width, r_root_start, r_root_end = \
        _build_tree_string(root.right, 2 * curr_index + 2, index, delimiter)

    # Draw the branch connecting the current root node to the left sub-box
    # Pad the line with whitespaces where necessary
    if l_box_width > 0:
        l_root = (l_root_start + l_root_end) // 2 + 1
        line1.append(' ' * (l_root + 1))
        line1.append('_' * (l_box_width - l_root))
        line2.append(' ' * l_root + '/')
        line2.append(' ' * (l_box_width - l_root))
        new_root_start = l_box_width + 1
        gap_size += 1
    else:
        new_root_start = 0

    # Draw the representation of the current root node
    line1.append(node_repr)
    line2.append(' ' * new_root_width)

    # Draw the branch connecting the current root node to the right sub-box
    # Pad the line with whitespaces where necessary
    if r_box_width > 0:
        r_root = (r_root_start + r_root_end) // 2
        line1.append('_' * r_root)
        line1.append(' ' * (r_box_width - r_root + 1))
        line2.append(' ' * r_root + '\\')
        line2.append(' ' * (r_box_width - r_root))
        gap_size += 1
    new_root_end = new_root_start + new_root_width - 1

    # Combine the left and right sub-boxes with the branches drawn above
    gap = ' ' * gap_size
    new_box = [''.join(line1), ''.join(line2)]
    for i in range(max(len(l_box), len(r_box))):
        l_line = l_box[i] if i < len(l_box) else ' ' * l_box_width
        r_line = r_box[i] if i < len(r_box) else ' ' * r_box_width
        new_box.append(l_line + gap + r_line)

    # Return the new box, its width and its root repr positions
    return new_box, len(new_box[0]), new_root_start, new_root_end

def subtreeFinder(answer, inorder, string):
    if string == []:
        return
    if len(inorder) != len(string):
        print("Invalid strings. Number of elements are unequal. Exiting...")
        exit()
    if answer:
        root = Node(string[0])
        string = string[1:]
    else:
        root = Node(string[-1])
        string = string[:-1]
    try:
        rootIndex = inorder.index(root.val)
    except ValueError:
        print("Invalid strings. Strings have different elements. Exiting...")
        exit()
    leftInOrder = inorder[0:rootIndex]
    rightInOrder = inorder[rootIndex+1:]
    leftString = string[:rootIndex]
    rightString = string[rootIndex:]
    
    if not answer:
        print(root.value, end=" ")

    if len(leftInOrder):
        root.left = subtreeFinder(answer, leftInOrder, leftString)
    if len(rightInOrder):
        root.right = subtreeFinder(answer, rightInOrder, rightString)

    if answer:
        print(root.value, end=" ")
        
    return root

def staticTree(string):
    nodes = [None if v == "-1" else Node(v) for v in string]

    for index in range(1, len(nodes)):
        node = nodes[index]
        if node is not None:
            parent_index = (index - 1) // 2
            parent = nodes[parent_index]
            if parent is None:
                print('parent node missing at index {}. Exiting...'.format(parent_index))
                exit()
            elif index % 2:
                parent.left = node
            else:
                parent.right = node

    return nodes[0] if nodes else None

def createBST(string):
    if string == []:
        return
    root = Node(string.pop(0))
    for index in range(0, len(string)):
        temp = root
        while(True):
            if string[index] > temp.value:
                if temp.right == None:
                    temp.right = Node(string[index])
                    break
                else:
                    temp = temp.right
            elif string[index] < temp.value:
                if temp.left == None:
                    temp.left = Node(string[index])
                    break
                else:
                    temp = temp.left
            else:
                break
    return root

def main():
    global answer
    print("[1] Create a Binary Tree using inorder and preorder strings.")
    print("[2] Create a Binary Tree using inorder and postorder strings.")
    print("[3] Create a Binary Tree using array string.")
    print("[4] Create a BST.")
    while(True):
        answer = input("Enter your choice: ")
        if answer == '1' or answer == '2':
            print("\nEnter the strings with each character separated by spaces.")
            inorder = input("In Order string: ").split()
            if answer == '1':
                preorder = input("Pre Order string: ").split()
                print("\nPost Order String = ", end="")
                root = subtreeFinder(True, inorder, preorder)
            else:
                postorder = input("Post Order string: ").split()
                print("\nPre Order String = ", end="")
                root = subtreeFinder(False, inorder, postorder)
            break
        elif answer == '3' or answer == '4':
            if answer == '3':
                print("\nEnter the string with each character separated by spaces. Use -1 as a character to represent no node.")
                string = input("String: ").split()
                root = staticTree(string)
            else:
                print("\nEnter the string with each number separated by spaces.")
                try:
                    string = [int(x) for x in input("String: ").split()]
                except ValueError:
                    print("BST can only contain numbers! Exiting...")
                    exit()
                root = createBST(string)
            if root != None:
                print(f"\nPreorder string = {root.preorder()}")
                print(f"Inorder string = {root.inorder()}")
                print(f"Postorder string = {root.postorder()}")
            break
        else:
            print("Invalid choice!")

    print()
    print(root)

if __name__ == '__main__':
    main()