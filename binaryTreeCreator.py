import re


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

    def height(self):
        current_level = [self]
        treeHeight = 1
        while len(current_level) > 0:
            treeHeight += 1
            next_level = []
            for node in current_level:
                if node.left is not None:
                    next_level.append(node.left)
                if node.right is not None:
                    next_level.append(node.right)

            current_level = next_level

        return treeHeight

    def inorder(self):
        result = []
        stack = []
        node = self

        while node or stack:
            while node:
                stack.append(node)
                node = node.left
            if stack:
                node = stack.pop()
                result.append(str(node.value))
                node = node.right

        return result

    def preorder(self):
        result = []
        stack = [self]

        while stack:
            node = stack.pop()
            if node:
                result.append(str(node.value))
                stack.append(node.right)
                stack.append(node.left)

        return result

    def postorder(self):
        result = []
        stack = [self]

        while stack:
            node = stack.pop()
            if node:
                result.append(str(node.value))
                stack.append(node.left)
                stack.append(node.right)

        return result[::-1]

    def staticArray(self):
        current_level = [self]
        result = []
        level = 1
        height = self.height()
        while level < height:
            next_level = []
            for node in current_level:
                if node != None:
                    result.append(str(node.value))
                    next_level.append(node.left)
                    next_level.append(node.right)
                else:
                    result.append('-1')
                    next_level.append(None)
                    next_level.append(None)

            current_level = next_level
            level += 1

        return result


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

    if len(leftInOrder):
        root.left = subtreeFinder(answer, leftInOrder, leftString)
    if len(rightInOrder):
        root.right = subtreeFinder(answer, rightInOrder, rightString)

    return root


def staticTree(array):
    nodes = [None if v == "-1" else Node(v) for v in array]

    for index in range(1, len(nodes)):
        node = nodes[index]
        if node is not None:
            parent_index = (index - 1) // 2
            parent = nodes[parent_index]
            if parent is None:
                print('parent node missing at index {}. Exiting...'.format(
                    parent_index))
                exit()
            elif index % 2:
                parent.left = node
            else:
                parent.right = node

    return nodes[0] if nodes else None


def createBST(array):
    if not array:
        return
    root = Node(array.pop(0))
    for index in range(0, len(array)):
        temp = root
        while(True):
            if array[index] > temp.value:
                if temp.right == None:
                    temp.right = Node(array[index])
                    break
                else:
                    temp = temp.right
            elif array[index] < temp.value:
                if temp.left == None:
                    temp.left = Node(array[index])
                    break
                else:
                    temp = temp.left
            else:
                break
    return root


def infixToPostfix(expression):
    stack = []
    postfix = []
    index = 0
    prec = {'+': 2, '-': 2, '*': 3, '/': 3, '(': 1}
    while(index < len(expression)):
        element = expression[index]
        if(element in "+-*/"):
            if stack == []:
                stack.append(element)
            else:
                top = stack[-1]
                if prec[element] > prec[top]:
                    stack.append(element)
                elif prec[top] == prec[element]:
                    postfix.append(stack.pop())
                    stack.append(element)
                else:
                    postfix.append(stack.pop())
                    continue
        elif element == '(':
            stack.append(element)
        elif element == ')':
            top = stack.pop()
            while top != '(':
                postfix.append(top)
                top = stack.pop()
        else:
            postfix.append(element)
        index += 1

    while stack != []:
        postfix.append(stack.pop())

    return [Node(x) for x in postfix]


def expressionTree(expression):
    expression = re.findall(r"([A-Z]+|\d+|[-+()/*])", expression)
    postfix = infixToPostfix(expression)
    stack = []
    for node in postfix:
        if node.value in "+-*/":
            try:
                rightVal = int(stack.pop())
                leftVal = int(stack.pop())
            except ValueError:
                print("\nCannot calculate result. Expression has non integer operands.")
                break
            except IndexError:
                print("\nInvalid Expression. Exiting...")
                exit()
            if node.value == '+':
                stack.append(leftVal + rightVal)
            elif node.value == '-':
                stack.append(leftVal - rightVal)
            elif node.value == '*':
                stack.append(leftVal * rightVal)
            else:
                stack.append(leftVal / rightVal)
        else:
            stack.append(node.value)
    else:
        if not stack:
            stack.append(0)
        print(f"\nResult = {stack.pop()}")

    stack = []
    for node in postfix:
        if node.value in '+-*/':
            node.right = stack.pop()
            node.left = stack.pop()
            stack.append(node)
        else:
            stack.append(node)

    return stack.pop() if stack != [] else None


def maxHeapify(root: Node):
    array = root.staticArray()
    for i in reversed(array):
        if(i == '-1'):
            del array[-1]
        else:
            break
    if '-1' in array:
        print("Cannot convert incomplete tree to heap.")
        return root

    try:
        array = [int(x) for x in array]
    except ValueError:
        print("Cannot convert tree with non integer characters")
        return root

    n = len(array)
    for i in range((n//2)-1, -1, -1):
        parent = largest = i
        while(True):
            left = 2*parent+1
            right = 2*parent+2
            if left < n and array[left] > array[largest]:
                largest = left
            if right < n and array[right] > array[largest]:
                largest = right
            if largest == parent:
                break
            else:
                array[largest], array[parent] = array[parent], array[largest]
                parent = largest

    root = staticTree([str(x) for x in array])
    print('\n', root)
    return root


def minHeapify(root: Node):
    array = root.staticArray()
    for i in reversed(array):
        if(i == '-1'):
            del array[-1]
        else:
            break

    if '-1' in array:
        print("Cannot convert incomplete tree to heap.")
        return root

    try:
        array = [int(x) for x in array]
    except ValueError:
        print("Cannot convert tree with non integer characters")
        return root

    n = len(array)
    for i in range((n//2)-1, -1, -1):
        parent = smallest = i
        while(True):
            left = 2*smallest+1
            right = 2*smallest+2
            if left < n and array[left] < array[smallest]:
                smallest = left
            if right < n and array[right] < array[smallest]:
                smallest = right
            if smallest == parent:
                break
            else:
                array[parent], array[smallest] = array[smallest], array[parent]
                parent = smallest

    root = staticTree([str(x) for x in array])
    print('\n', root)
    return root
