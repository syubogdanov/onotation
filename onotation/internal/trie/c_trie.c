#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

#define ALPHABET_SIZE 256

typedef struct TrieNode {
    struct TrieNode* children[ALPHABET_SIZE];
    int terminal; // 1 if word ends here
} TrieNode;

typedef struct {
    PyObject_HEAD
    TrieNode* root;
    Py_ssize_t size;
} TrieObject;

static PyTypeObject TrieType;



static TrieNode* create_node(void) {
    TrieNode* node = (TrieNode*)calloc(1, sizeof(TrieNode));
    return node;
}

static void free_node(TrieNode* node) {
    if (!node) return;
    for (int i = 0; i < ALPHABET_SIZE; i++) {
        if (node->children[i]) free_node(node->children[i]);
    }
    free(node);
}



static bool trie_contains(TrieNode* root, const char* str) {
    TrieNode* node = root;
    for (size_t i = 0; str[i]; i++) {
        unsigned char c = (unsigned char)str[i];
        if (!node->children[c]) return false;
        node = node->children[c];
    }
    return node && node->terminal;
}

static int trie_add(TrieNode* root, const char* str) {
    TrieNode* node = root;
    for (size_t i = 0; str[i]; i++) {
        unsigned char c = (unsigned char)str[i];
        if (!node->children[c]) {
            node->children[c] = create_node();
        }
        node = node->children[c];
    }

    if (node->terminal) return 0;
    node->terminal = 1;
    return 1;
}



static int trie_remove(TrieNode* node, const char* str, int depth) {
    if (!node) return 0;

    if (str[depth] == '\0') {
        if (!node->terminal) return 0;
        node->terminal = 0;
        return 1;
    }

    unsigned char c = (unsigned char)str[depth];
    if (!node->children[c]) return 0;

    int removed = trie_remove(node->children[c], str, depth + 1);

    if (removed) {
        TrieNode* child = node->children[c];

        int has_children = 0;
        for (int i = 0; i < ALPHABET_SIZE; i++) {
            if (child->children[i]) {
                has_children = 1;
                break;
            }
        }

        if (!child->terminal && !has_children) {
            free(child);
            node->children[c] = NULL;
        }
    }

    return removed;
}



static void dfs_collect(TrieNode* node, char* buffer, int depth, PyObject* list) {
    if (!node) return;

    if (node->terminal) {
        buffer[depth] = '\0';
        PyList_Append(list, PyUnicode_FromString(buffer));
    }

    for (int i = 0; i < ALPHABET_SIZE; i++) {
        if (node->children[i]) {
            buffer[depth] = (char)i;
            dfs_collect(node->children[i], buffer, depth + 1, list);
        }
    }
}


static PyObject* Trie_new(PyTypeObject* type, PyObject* args, PyObject* kwds) {
    TrieObject* self = (TrieObject*)type->tp_alloc(type, 0);
    if (self) {
        self->root = create_node();
        self->size = 0;
    }
    return (PyObject*)self;
}

static void Trie_dealloc(TrieObject* self) {
    free_node(self->root);
    Py_TYPE(self)->tp_free((PyObject*)self);
}

static PyObject* Trie_len(TrieObject* self) {
    return PyLong_FromSsize_t(self->size);
}

static PyObject* Trie_contains(TrieObject* self, PyObject* args) {
    const char* s;
    if (!PyArg_ParseTuple(args, "s", &s)) return NULL;
    return PyBool_FromLong(trie_contains(self->root, s));
}

static PyObject* Trie_add(TrieObject* self, PyObject* args) {
    const char* s;
    if (!PyArg_ParseTuple(args, "s", &s)) return NULL;

    int added = trie_add(self->root, s);
    if (added) self->size++;

    Py_RETURN_NONE;
}

static PyObject* Trie_remove(TrieObject* self, PyObject* args) {
    const char* s;
    if (!PyArg_ParseTuple(args, "s", &s)) return NULL;

    int removed = trie_remove(self->root, s, 0);
    if (!removed) {
        PyErr_SetString(PyExc_KeyError, "not found");
        return NULL;
    }

    self->size--;
    Py_RETURN_NONE;
}

static PyObject* Trie_discard(TrieObject* self, PyObject* args) {
    const char* s;
    if (!PyArg_ParseTuple(args, "s", &s)) return NULL;

    int removed = trie_remove(self->root, s, 0);
    if (removed) self->size--;

    Py_RETURN_NONE;
}

static PyObject* Trie_clear(TrieObject* self, PyObject* Py_UNUSED(args)) {
    free_node(self->root);
    self->root = create_node();
    self->size = 0;
    Py_RETURN_NONE;
}

static PyObject* Trie_iter(TrieObject* self) {
    PyObject* list = PyList_New(0);
    char buffer[1024];

    dfs_collect(self->root, buffer, 0, list);

    PyObject* iter = PyObject_GetIter(list);
    Py_DECREF(list);
    return iter;
}


static PyMethodDef Trie_methods[] = {
    {"add", (PyCFunction)Trie_add, METH_VARARGS},
    {"remove", (PyCFunction)Trie_remove, METH_VARARGS},
    {"discard", (PyCFunction)Trie_discard, METH_VARARGS},
    {"clear", (PyCFunction)Trie_clear, METH_NOARGS},
    {"__contains__", (PyCFunction)Trie_contains, METH_VARARGS},
    {NULL}
};

static PySequenceMethods Trie_as_sequence = {
    (lenfunc)Trie_len
};

static PyTypeObject TrieType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "onotation.internal.trie.c_trie.Trie",
    .tp_basicsize = sizeof(TrieObject),
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_new = Trie_new,
    .tp_dealloc = (destructor)Trie_dealloc,
    .tp_iter = (getiterfunc)Trie_iter,
    .tp_methods = Trie_methods,
    .tp_as_sequence = &Trie_as_sequence,
};