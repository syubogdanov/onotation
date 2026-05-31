#define PY_SSIZE_T_CLEAN

#include <Python.h>
#include <stdlib.h>
#include <stdbool.h>

typedef struct Node {
    long value;
    int height;
    struct Node* parent;
    struct Node* right;
    struct Node* left;
} Node;

typedef struct {
    PyObject_HEAD
    Node* root;
    Py_ssize_t size;
} AVLTreeObject;

static PyTypeObject AVLTreeType;

static Node* create_node(long value) {
    Node* node = (Node*)malloc(sizeof(Node));
    if (!node) return NULL;
    node->value = value;
    node->height = 1;
    node->parent = NULL;
    node->right = NULL;
    node->left = NULL;
    return node;
}

static int height(Node* node) { return node ? node->height : 0; }

static void update_height(Node* node) {
    if (node) node->height = 1 + (height(node->left) > height(node->right) ? height(node->left) : height(node->right));
}

static Node* rotate_right(Node* y) {
    Node* x = y->left; Node* T2 = x->right;
    x->right = y; y->left = T2;
    if (T2) T2->parent = y;
    x->parent = y->parent; y->parent = x;
    update_height(y); update_height(x);
    return x;
}

static Node* rotate_left(Node* x) {
    Node* y = x->right; Node* T2 = y->left;
    y->left = x; x->right = T2;
    if (T2) T2->parent = x;
    y->parent = x->parent; x->parent = y;
    update_height(x); update_height(y);
    return y;
}

static Node* balance(Node* node) {
    if (!node) return NULL;
    update_height(node);
    int bal = height(node->left) - height(node->right);
    if (bal > 1) {
        if (height(node->left->right) > height(node->left->left))
            node->left = rotate_left(node->left);
        return rotate_right(node);
    }
    if (bal < -1) {
        if (height(node->right->left) > height(node->right->right))
            node->right = rotate_right(node->right);
        return rotate_left(node);
    }
    return node;
}

static Node* insert_node(Node* node, long value, Node* parent, int* inserted) {
    if (!node) {
        *inserted = 1;
        Node* n = create_node(value);
        if (n) n->parent = parent;
        return n;
    }
    if (value < node->value)
        node->left = insert_node(node->left, value, node, inserted);
    else if (value > node->value)
        node->right = insert_node(node->right, value, node, inserted);
    else *inserted = 0;
    node->parent = parent;
    return balance(node);
}

static Node* find_min(Node* node) {
    while (node && node->left) node = node->left;
    return node;
}

static Node* delete_node(Node* node, long value, Node* parent, int* deleted) {
    if (!node) { *deleted = 0; return NULL; }
    if (value < node->value)
        node->left = delete_node(node->left, value, node, deleted);
    else if (value > node->value)
        node->right = delete_node(node->right, value, node, deleted);
    else {
        *deleted = 1;
        if (!node->left || !node->right) {
            Node* temp = node->left ? node->left : node->right;
            if (temp) temp->parent = parent;
            free(node);
            return temp;
        }
        Node* minr = find_min(node->right);
        node->value = minr->value;
        node->right = delete_node(node->right, minr->value, node, deleted);
    }
    node->parent = parent;
    return balance(node);
}

static bool search_tree(Node* node, long value) {
    while (node) {
        if (value == node->value) return true;
        node = value < node->value ? node->left : node->right;
    }
    return false;
}

static void free_tree(Node* node) {
    if (!node) return;
    free_tree(node->left);
    free_tree(node->right);
    free(node);
}

static void inorder_collect(Node* node, PyObject* list) {
    if (!node) return;
    inorder_collect(node->left, list);
    PyList_Append(list, PyLong_FromLong(node->value));
    inorder_collect(node->right, list);
}

/* Python bindings */
static PyObject* AVLTree_new(PyTypeObject* type, PyObject* args, PyObject* kwds) {
    AVLTreeObject* self = (AVLTreeObject*)type->tp_alloc(type, 0);
    if (self) { self->root = NULL; self->size = 0; }
    return (PyObject*)self;
}

static void AVLTree_dealloc(AVLTreeObject* self) {
    free_tree(self->root);
    Py_TYPE(self)->tp_free((PyObject*)self);
}

static Py_ssize_t AVLTree_len(AVLTreeObject* self) { return self->size; }

static PyObject* AVLTree_contains(AVLTreeObject* self, PyObject* args) {
    long v;
    if (!PyArg_ParseTuple(args, "l", &v)) return NULL;
    return PyBool_FromLong(search_tree(self->root, v));
}

static PyObject* AVLTree_add(AVLTreeObject* self, PyObject* args) {
    long v; if (!PyArg_ParseTuple(args, "l", &v)) return NULL;
    int ins = 0;
    self->root = insert_node(self->root, v, NULL, &ins);
    if (ins) self->size++;
    Py_RETURN_NONE;
}

static PyObject* AVLTree_remove(AVLTreeObject* self, PyObject* args) {
    long v; if (!PyArg_ParseTuple(args, "l", &v)) return NULL;
    int del = 0;
    self->root = delete_node(self->root, v, NULL, &del);
    if (!del) { PyErr_SetString(PyExc_ValueError, "value not in tree"); return NULL; }
    self->size--;
    Py_RETURN_NONE;
}

static PyObject* AVLTree_discard(AVLTreeObject* self, PyObject* args) {
    long v; if (!PyArg_ParseTuple(args, "l", &v)) return NULL;
    int del = 0;
    self->root = delete_node(self->root, v, NULL, &del);
    if (del) self->size--;
    Py_RETURN_NONE;
}

static PyObject* AVLTree_pop(AVLTreeObject* self, PyObject* Py_UNUSED(args)) {
    if (self->size == 0) { PyErr_SetString(PyExc_KeyError, "pop from an empty tree"); return NULL; }
    Node* minn = find_min(self->root);
    long v = minn->value;
    int del = 0;
    self->root = delete_node(self->root, v, NULL, &del);
    self->size--;
    return PyLong_FromLong(v);
}

static PyObject* AVLTree_clear(AVLTreeObject* self, PyObject* Py_UNUSED(args)) {
    free_tree(self->root);
    self->root = NULL; self->size = 0;
    Py_RETURN_NONE;
}

static PySequenceMethods AVLTree_as_sequence = { (lenfunc)AVLTree_len };

static PyMethodDef methods[] = {
    {"add", (PyCFunction)AVLTree_add, METH_VARARGS},
    {"remove", (PyCFunction)AVLTree_remove, METH_VARARGS},
    {"discard", (PyCFunction)AVLTree_discard, METH_VARARGS},
    {"pop", (PyCFunction)AVLTree_pop, METH_NOARGS},
    {"clear", (PyCFunction)AVLTree_clear, METH_NOARGS},
    {"__contains__", (PyCFunction)AVLTree_contains, METH_VARARGS},
    {NULL}
};

static PyObject* AVLTree_iter(AVLTreeObject* self) {
    PyObject* list = PyList_New(0);
    if (!list) return NULL;
    inorder_collect(self->root, list);
    PyObject* iter = PyObject_GetIter(list);
    Py_DECREF(list);
    return iter;
}

static PyTypeObject AVLTreeType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "onotation.internal.avl_tree.c_avl_tree.AVLTree",
    .tp_basicsize = sizeof(AVLTreeObject),
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_new = AVLTree_new,
    .tp_dealloc = (destructor)AVLTree_dealloc,
    .tp_iter = (getiterfunc)AVLTree_iter,
    .tp_methods = methods,
    .tp_as_sequence = &AVLTree_as_sequence,
};

static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT, "c_avl_tree", NULL, -1, NULL
};

PyMODINIT_FUNC PyInit_c_avl_tree(void) {
    if (PyType_Ready(&AVLTreeType) < 0) return NULL;
    PyObject* m = PyModule_Create(&moduledef);
    if (!m) return NULL;
    Py_INCREF(&AVLTreeType);
    PyModule_AddObject(m, "AVLTree", (PyObject*)&AVLTreeType);
    return m;
}
