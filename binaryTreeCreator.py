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
        if answer:
            print(root.left.value, end=" ")
    if len(rightInOrder):
        root.right = subtreeFinder(answer, rightInOrder, rightString)
        if answer:
            print(root.right.value, end=" ")
    return root

def main():
    global answer
    print("Enter the strings with each character separated by spaces.")
    inorder = input("In Order string: ").split()
    answer = input("Do you want to enter Pre Order string?('yes' or 'no'): ")
    if answer == 'yes':
        preorder = input("Pre Order string: ").split()
        print("\nPost Order String = ", end="")
        root = subtreeFinder(True, inorder, preorder)
        print(root.value)
    else:
        postorder = input("Post Order string: ").split()
        print("\nPre Order String = ", end="")
        root = subtreeFinder(False, inorder, postorder)
        print()
    print(root)

if __name__ == '__main__':
    main()