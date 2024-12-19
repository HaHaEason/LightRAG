import re

class Node:
    def __init__(self, level, title, content='', parent=None):
        self.level = level
        self.title = title
        self.content = content
        self.children = []
        self.parent = parent
        self.contentSize = len(content)

    def __repr__(self):
        return f"Node(title={self.getTitles()}, contentSize={self.contentSize}, children={len(self.children)}, parent={self.parent.title if self.parent else None})"

    def getTitles(self):
        titles = []
        current_node = self
        while current_node:
            if current_node.level == 0:
                break
            titles.append((current_node.title, current_node.level))
            current_node = current_node.parent
        return reversed(titles)

    def addChildren(self, child):
        self.children.append(child)
        child.parent = self

    def updateContentSize(self, size):
        current_node = self
        while current_node:
            current_node.contentSize += size
            current_node = current_node.parent

    def getAllContent(self, isFirst=True):
#         content = f"""<!-- 
#     title: {self.getTitles()}
# -->\n"""
        content = ''
        if isFirst:
            for title, level in self.getTitles():
                content += '#' * level + ' ' + title + '\n'
            content += self.content
        else:
            content += '#' * self.level + ' ' + self.title + '\n' + self.content

        for child in self.children:
            content += child.getAllContent(False)
        return content

class MarkdownParser:
    def __init__(self, lines):
        self.lines = lines

        self.root = Node(0, 'root')
        stack = [(self.root, 0)]

        for line in self.lines:
            header_match = re.match(r'^(#{1,6})\s+(.*)', line)
            if header_match:
                level = len(header_match.group(1))
                title = header_match.group(2)

                if stack:
                    stack[-1][0].updateContentSize(len(stack[-1][0].content))

                for i in range(len(stack) - 1, -1, -1):
                    if stack[i][1] < level:
                        parent = stack[i][0]
                        break

                node = Node(level, title, parent=parent)

                if parent:
                    parent.addChildren(node)

                while stack and stack[-1][1] >= level:
                    stack.pop()

                stack.append((node, level))
            else:
                if stack:
                    stack[-1][0].content += line

        if stack:
            stack[-1][0].updateContentSize(len(stack[-1][0].content))

    def get_chunks(self, max_token_size):
        chunks = []
        stack = [(self.root, 0)]  # 初始化时放入 root 节点

        while stack:
            node, index = stack.pop()
            if node.contentSize <= max_token_size:
                chunks.append(node.getAllContent())
            else:
                if index < len(node.children):
                    stack.append((node, index + 1))  # 继续处理下一个兄弟节点
                    stack.append((node.children[index], 0))  # 处理当前节点的子节点

        return chunks

if __name__ == "__main__":
    with open("/Users/panweiyi/workspaces/graph/legal/company.md", encoding="utf-8-sig") as f:
        LINES = f.readlines()
    parser = MarkdownParser(LINES)
    chunks = parser.get_chunks(max_token_size=1000)
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i + 1}:\n{chunk}\n")