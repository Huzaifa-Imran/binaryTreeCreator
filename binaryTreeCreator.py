class Node():
    def __init__(self, value):
        self.value = self.val = value
        self.left = None
        self.right = None

    def __str__(self):
        lines = self._build_tree_string(0, False, '-')[0]
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

    def _build_tree_string(self, curr_index, index=False, delimiter='-'):
        root = self
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
    if answer:
        root = Node(string[0])
        string = string[1:]
    else:
        root = Node(string[-1])
        string = string[:-1]
    
    rootIndex = inorder.index(root.val)
    leftInOrder = inorder[0:rootIndex]
    rightInOrder = inorder[rootIndex+1:]
    leftString = [x for x in string if x in leftInOrder]
    rightString = [x for x in string if x in rightInOrder]
    if len(leftInOrder):
        root.left = subtreeFinder(answer, leftInOrder, leftString)
    if len(rightInOrder):
        root.right = subtreeFinder(answer, rightInOrder, rightString)
    return root

def main():
    global answer
    inorder = input("Enter in order string: ").split(' ')
    answer = input("Do you want to enter pre order string?('yes' or 'no'): ")
    if answer == 'yes':
        preorder = input("Enter pre order string: ").split(' ')
        root = subtreeFinder(True, inorder, preorder)
    else:
        postorder = input("Enter post order string: ").split(' ')
        # postorder = [int(x) for x in postorder]
        root = subtreeFinder(False, inorder, postorder)
    print(root)

if __name__ == '__main__':
    main()