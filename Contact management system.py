class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def __init__(self):
        self.root = None

    def get_height(self, node):
        if node is None:
            return 0
        return node.height

    def update_height(self, node):
        if node is None:
            return
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

    def get_balance(self, node):
        if node is None:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def rotate_left(self, z):     # LL rotation
        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        self.update_height(z)
        self.update_height(y)

        return y

    def rotate_right(self, y):   # RR rotation
        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2

        self.update_height(y)
        self.update_height(x)

        return x

    def _insert(self, node, value):
        if node is None:
            return TreeNode(value)
        elif value < node.value:
            node.left = self._insert(node.left, value)
        else:
            node.right = self._insert(node.right, value)

        self.update_height(node)     

        balance = self.get_balance(node)             # After inserting, we're checking continously the balane factor of all nodes.


        # Abnormal balance factors
        # If it is greater than 1
        # Left subtree is longer than the right sub tree
        if balance > 1:
            if value < node.left.value:
                return self.rotate_right(node)
            else:
                node.left = self.rotate_left(node.left)
                return self.rotate_right(node)

        # If it is lesser than -1
        # If the right subtree is larger than the left subtree
        if balance < -1:
            if value > node.right.value:
                return self.rotate_left(node)
            else:
                node.right = self.rotate_right(node.right)
                return self.rotate_left(node)

        return node

    def insert(self, value):
        self.root = self._insert(self.root, value)


class PhoneHistoryManager:
    def __init__(self):
        self.hash_table = {}

    def get_hash_key(self, phone_number, name):
        return hash(phone_number + name) % 1000  

    def get_height(self, node):
        if node is None:
            return 0
        return node.height

    def update_height(self, key):
        if key in self.hash_table:
            avl_tree = self.hash_table[key]
            avl_tree.update_height(avl_tree.root)

    # If a user is added we'll atomically put it as the key of the hash table and we'll assign a AVL tree value for it
    def add_user(self, phone_number, name):
        key = self.get_hash_key(phone_number, name)
        if key not in self.hash_table:
            self.hash_table[key] = AVLTree()

    
    def remove_user(self, phone_number, name):
        key = self.get_hash_key(phone_number, name)
        if key in self.hash_table:
            del self.hash_table[key]

    def add_history(self, phone_number, name, call_time):
        key = self.get_hash_key(phone_number, name)
        if key in self.hash_table:
            avl_tree = self.hash_table[key]
            avl_tree.insert(call_time)
            self.update_height(key)
        else:
            self.add_user(phone_number, name)
            self.add_history(phone_number, name, call_time)

    def remove_history(self, phone_number, name, call_time):
        key = self.get_hash_key(phone_number, name)
        if key in self.hash_table:
            avl_tree = self.hash_table[key]
            avl_tree.root = self.remove_call_history(avl_tree.root, call_time)

    def remove_call_history(self, node, call_time):
        if node is None:
            return None

        if node.value == call_time:
            if node.left is None and node.right is None:
                return None
            elif node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            else:
                successor = self.get_successor(node.right)
                node.value = successor.value
                node.right = self.remove_call_history(node.right, successor.value)
        elif node.value < call_time:
            node.right = self.remove_call_history(node.right, call_time)
        else:
            node.left = self.remove_call_history(node.left, call_time)

        self.update_height(node)

        balance = self.get_balance(node)

        if balance > 1:
            if self.get_balance(node.left) >= 0:
                return self.rotate_right(node)
            else:
                node.left = self.rotate_left(node.left)
                return self.rotate_right(node)

        if balance < -1:
            if self.get_balance(node.right) <= 0:
                return self.rotate_left(node)
            else:
                node.right = self.rotate_right(node.right)
                return self.rotate_left(node)

        return node

    def get_successor(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def get_history_before(self, phone_number, name, call_time):
        key = self.get_hash_key(phone_number, name)
        if key in self.hash_table:
            avl_tree = self.hash_table[key]
            return self.get_call_history_before(avl_tree.root, call_time)
        return None

    def get_call_history_before(self, node, call_time):
        if node is None:
            return []

        if node.value < call_time:
            left_history = self.get_call_history_before(node.left, call_time)
            right_history = self.get_call_history_before(node.right, call_time)
            return left_history + [node.value] + right_history
        elif node.value == call_time:
            return [node.value]
        else:
            return self.get_call_history_before(node.left, call_time)

    def get_balance(self, node):
        if node is None:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)
    
    def print_contacts(self):
        for key in self.hash_table:
            phone_number, name = divmod(key, 1000)
            print(f"Phone Number: {phone_number}, Name: {name}")


# Create a PhoneHistoryManager instance
phone_manager = PhoneHistoryManager()

# Add users and call history
phone_manager.add_user("555-1234", "John")
phone_manager.add_user("555-5678", "Jane")

phone_manager.add_history("555-1234", "John", "2023-06-10 14:45")
phone_manager.add_history("555-1234", "John", "2022-06-11 14:45")
phone_manager.add_history("555-1234", "John", "2023-06-11 14:45")
phone_manager.add_history("555-5678", "Jane", "2023-06-12 09:15")

# Retrieve call history before a specific time
call_time = "2023-06-12 11:45"
history = phone_manager.get_history_before("555-1234", "John", call_time)
if history:
    print(f"Call history for John (555-1234) before {call_time}:")
    for item in history:
        print(item)
else:
    print(f"No call history found for John (555-1234) before {call_time}")

# Remove a call history entry
call_time_to_remove = "2022-06-11 14:45"
phone_manager.remove_history("555-1234", "John", call_time_to_remove)

# Retrieve call history after removing the entry
history = phone_manager.get_history_before("555-1234", "John", call_time)
if history:
    print(f"Updated call history for John (555-1234) before {call_time}:")
    for item in history:
        print(item)
else:
    print(f"No call history found for John (555-1234) before {call_time}")

# Remove a user
phone_manager.remove_user("555-5678", "Jane")
