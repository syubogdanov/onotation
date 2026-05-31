// SPDX-License-Identifier: MIT

#define PY_SSIZE_T_CLEAN
#define TRIE_MAX_DEPTH 4096

#include <Python.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

typedef struct TrieNode {
    bool terminal;
    struct TrieNode* children[256];
} TrieNode;

typedef struct {
    PyObject_HEAD
    TrieNode* root;
    Py_ssize_t size;
} TrieObject;

static PyTypeObject TrieType;
static PyObject* Trie_to_set(TrieObject* self);

static TrieNode* create_node(void) {
    TrieNode* node = (TrieNode*)calloc(1, sizeof(TrieNode));
    return node;
}

static void free_trie(TrieNode* node) {
    if (!node) {
        return;
    }

    for (int i = 0; i < 256; i++) {
        free_trie(node->children[i]);
    }

    free(node);
}
static int insert_word(TrieNode* root, const char* word) {
    TrieNode* node = root;

    while (*word) {
        unsigned char c = (unsigned char)*word;

        if (!node->children[c]) {
            node->children[c] = create_node();

            if (!node->children[c]) {
                return 0;
            }
        }

        node = node->children[c];
        word++;
    }

    if (node->terminal) {
        return 0;
    }

    node->terminal = 1;
    return 1;
}

static bool search_word(TrieNode* root, const char* word) {
    TrieNode* node = root;

    while (*word) {
        unsigned char c = (unsigned char)*word;

        if (!node->children[c]) {
            return false;
        }

        node = node->children[c];
        word++;
    }

    return node->terminal;
}

static bool node_empty(TrieNode* node) {
    if (node->terminal) {
        return false;
    }

    for (int i = 0; i < 256; i++) {
        if (node->children[i]) {
            return false;
        }
    }

    return true;
}
static int delete_word_recursive(
    TrieNode* node,
    const unsigned char* word,
    int depth
) {
    if (!node) {
        return 0;
    }

    if (word[depth] == '\0') {

        if (!node->terminal) {
            return 0;
        }

        node->terminal = 0;

        return node_empty(node);
    }

    unsigned char c = word[depth];

    TrieNode* child = node->children[c];

    if (!child) {
        return 0;
    }

    int remove_child =
        delete_word_recursive(child, word, depth + 1);

    if (remove_child) {
        free_trie(child);
        node->children[c] = NULL;
    }

    return node_empty(node);
}

static int remove_word(
    TrieNode* root,
    const char* word
) {
    if (!search_word(root, word)) {
        return 0;
    }

    delete_word_recursive(
        root,
        (const unsigned char*)word,
        0
    );

    return 1;
}
static void collect_words(
    TrieNode* node,
    char* buffer,
    int depth,
    PyObject* list
)
{
    if (!node) return;

    if (node->terminal) {
        buffer[depth] = '\0';

        PyObject* str = PyUnicode_FromString(buffer);
        if (str) {
            PyList_Append(list, str);
            Py_DECREF(str);
        }
    }

    unsigned char children[256];
    int count = 0;

    for (int i = 0; i < 256; i++) {
        if (node->children[i]) {
            children[count++] = (unsigned char)i;
        }
    }

    for (int j = count - 1; j >= 0; j--) {
        int i = children[j];

        buffer[depth] = (char)i;
        collect_words(node->children[i], buffer, depth + 1, list);
    }
}

static void collect_words_reverse(
    TrieNode* node,
    char* buffer,
    int depth,
    PyObject* list
)
{
    if (!node) return;

    if (node->terminal) {
        buffer[depth] = '\0';

        PyObject* str = PyUnicode_FromString(buffer);
        if (str) {
            PyList_Append(list, str);
            Py_DECREF(str);
        }
    }

    unsigned char children[256];
    int count = 0;

    for (int i = 0; i < 256; i++) {
        if (node->children[i]) {
            children[count++] = (unsigned char)i;
        }
    }

    for (int j = 0; j < count; j++) {
        int i = children[j];

        buffer[depth] = (char)i;
        collect_words_reverse(node->children[i], buffer, depth + 1, list);
    }
}
static PyObject* Trie_new(
    PyTypeObject* type,
    PyObject* args,
    PyObject* kwds
) {
    TrieObject* self =
        (TrieObject*)type->tp_alloc(type, 0);

    if (self != NULL) {
        self->root = create_node();
        self->size = 0;
    }

    return (PyObject*)self;
}

static int Trie_init(
    TrieObject* self,
    PyObject* args,
    PyObject* kwds
) {
    PyObject* iterable = NULL;

    if (!PyArg_ParseTuple(args, "|O", &iterable)) {
        return -1;
    }

    if (iterable && iterable != Py_None) {

        PyObject* iterator =
            PyObject_GetIter(iterable);

        if (!iterator) {
            return -1;
        }

        PyObject* item;

        while ((item = PyIter_Next(iterator))) {

            const char* word =
                PyUnicode_AsUTF8(item);

            if (word) {

                if (
                    insert_word(
                        self->root,
                        word
                    )
                ) {
                    self->size++;
                }
            }

            Py_DECREF(item);
        }

        Py_DECREF(iterator);
    }

    return 0;
}

static void Trie_dealloc(
    TrieObject* self
) {
    free_trie(self->root);

    Py_TYPE(self)->tp_free(
        (PyObject*)self
    );
}
static PyObject* Trie_add(
    TrieObject* self,
    PyObject* args
) {
    const char* word;

    if (!PyArg_ParseTuple(
        args,
        "s",
        &word
    )) {
        return NULL;
    }

    int inserted =
        insert_word(self->root, word);

    if (inserted) {
        self->size++;
    }

    Py_RETURN_NONE;
}

static PyObject* Trie_remove(
    TrieObject* self,
    PyObject* args
) {
    const char* word;

    if (!PyArg_ParseTuple(
        args,
        "s",
        &word
    )) {
        return NULL;
    }

    int removed =
        remove_word(self->root, word);

    if (!removed) {
        PyErr_SetString(
            PyExc_KeyError,
            word
        );

        return NULL;
    }

    self->size--;

    Py_RETURN_NONE;
}

static PyObject* Trie_discard(
    TrieObject* self,
    PyObject* args
) {
    const char* word;

    if (!PyArg_ParseTuple(
        args,
        "s",
        &word
    )) {
        return NULL;
    }

    int removed =
        remove_word(self->root, word);

    if (removed) {
        self->size--;
    }

    Py_RETURN_NONE;
}
static PyObject* Trie_len(
    TrieObject* self,
    PyObject* Py_UNUSED(args)
) {
    return PyLong_FromSsize_t(
        self->size
    );
}

static PyObject* Trie_contains(
    TrieObject* self,
    PyObject* args
) {
    const char* word;

    if (!PyArg_ParseTuple(
        args,
        "s",
        &word
    )) {
        return NULL;
    }

    if (
        search_word(
            self->root,
            word
        )
    ) {
        Py_RETURN_TRUE;
    }

    Py_RETURN_FALSE;
}
static PyObject* Trie_clear(TrieObject* self, PyObject* Py_UNUSED(args))
{
    if (self->root) {
        free_trie(self->root);
    }

    self->root = create_node();
    self->size = 0;

    Py_RETURN_NONE;
}
static PyObject* Trie_iter(TrieObject* self, PyObject* Py_UNUSED(args))
{
    PyObject* list = PyList_New(0);
    if (!list) return NULL;

    char buffer[TRIE_MAX_DEPTH];

    collect_words(self->root, buffer, 0, list);

    PyObject* iter = PyObject_GetIter(list);
    Py_DECREF(list);

    return iter;
}
static PyObject* Trie_reversed(
    TrieObject* self,
    PyObject* Py_UNUSED(args)
) {
    PyObject* list =
        PyList_New(0);

    if (!list) {
        return NULL;
    }

    char buffer[TRIE_MAX_DEPTH];

    collect_words_reverse(
        self->root,
        buffer,
        0,
        list
    );

    PyObject* iter =
        PyObject_GetIter(list);

    Py_DECREF(list);

    return iter;
}
static bool find_first_word_recursive(
    TrieNode* node,
    char* buffer,
    int depth
) {
    if (!node) {
        return false;
    }

    if (node->terminal) {
        buffer[depth] = '\0';
        return true;
    }

    for (int i = 0; i < 256; i++) {
        if (node->children[i]) {

            buffer[depth] = (char)i;

            if (
                find_first_word_recursive(
                    node->children[i],
                    buffer,
                    depth + 1
                )
            ) {
                return true;
            }
        }
    }

    return false;
}

static PyObject* Trie_pop(TrieObject* self, PyObject* Py_UNUSED(args))
{
    if (self->size == 0) {
        PyErr_SetString(PyExc_KeyError, "pop from an empty trie");
        return NULL;
    }

    PyObject* iter = PyObject_GetIter((PyObject*)self);
    if (!iter) return NULL;

    PyObject* first = PyIter_Next(iter);
    Py_DECREF(iter);

    if (!first) {
        if (!PyErr_Occurred()) {
            PyErr_SetString(PyExc_RuntimeError, "trie corrupted");
        }
        return NULL;
    }

    if (!PyUnicode_Check(first)) {
        Py_DECREF(first);
        PyErr_SetString(PyExc_TypeError, "invalid trie element");
        return NULL;
    }

    const char* word = PyUnicode_AsUTF8(first);

    char copy[1024];
    snprintf(copy, sizeof(copy), "%s", word);

    Py_DECREF(first);

    remove_word(self->root, copy);
    self->size--;

    return PyUnicode_FromString(copy);
}
static PyObject* Trie_eq(PyObject* self, PyObject* other)
{
    if (!PyObject_TypeCheck(other, &TrieType)) {
        Py_RETURN_NOTIMPLEMENTED;
    }

    TrieObject* a = (TrieObject*)self;
    TrieObject* b = (TrieObject*)other;

    if (a->size != b->size) {
        Py_RETURN_FALSE;
    }

    PyObject* set_a = Trie_to_set(a);
    if (!set_a) return NULL;

    PyObject* set_b = Trie_to_set(b);
    if (!set_b) {
        Py_DECREF(set_a);
        return NULL;
    }

    int res = PyObject_RichCompareBool(set_a, set_b, Py_EQ);

    Py_DECREF(set_a);
    Py_DECREF(set_b);

    if (res < 0) return NULL;
    return res ? Py_RETURN_TRUE : Py_RETURN_FALSE;
}

static PyObject* Trie_to_set(TrieObject* self)
{
    PyObject* list = PyList_New(0);
    if (!list) return NULL;

    char buffer[TRIE_MAX_DEPTH];

    collect_words(self->root, buffer, 0, list);

    PyObject* set = PySet_New(list);

    Py_DECREF(list);
    return set;
}

static PyObject* Trie_from_set(
    PyObject* set_obj
) {
    PyObject* trie_obj =
        PyObject_CallObject(
            (PyObject*)&TrieType,
            NULL
        );

    if (!trie_obj) {
        return NULL;
    }

    TrieObject* trie =
        (TrieObject*)trie_obj;

    PyObject* iterator =
        PyObject_GetIter(set_obj);

    if (!iterator) {
        Py_DECREF(trie_obj);
        return NULL;
    }

    PyObject* item;

    while ((item = PyIter_Next(iterator))) {

        const char* word =
            PyUnicode_AsUTF8(item);

        if (!word) {
            Py_DECREF(item);
            Py_DECREF(iterator);
            Py_DECREF(trie_obj);
            return NULL;
        }

        if (
            insert_word(
                trie->root,
                word
            )
        ) {
            trie->size++;
        }

        Py_DECREF(item);
    }

    Py_DECREF(iterator);

    return trie_obj;
}
static PyObject* Trie_isdisjoint(TrieObject* self, PyObject* other)
{
    PyObject* iter = PyObject_GetIter(other);
    if (!iter) return NULL;

    PyObject* item;

    while ((item = PyIter_Next(iter))) {

        if (!PyUnicode_Check(item)) {
            Py_DECREF(item);
            Py_DECREF(iter);
            PyErr_SetString(PyExc_TypeError, "expected strings");
            return NULL;
        }

        const char* word = PyUnicode_AsUTF8(item);

        if (word && search_word(self->root, word)) {
            Py_DECREF(item);
            Py_DECREF(iter);
            Py_RETURN_FALSE;
        }

        Py_DECREF(item);
    }

    Py_DECREF(iter);

    if (PyErr_Occurred()) return NULL;

    Py_RETURN_TRUE;
}

static PyObject* Trie_le(TrieObject* self, PyObject* other)
{
    PyObject* iter = PyObject_GetIter((PyObject*)self);
    if (!iter) return NULL;

    PyObject* item;

    while ((item = PyIter_Next(iter))) {

        if (!PyUnicode_Check(item)) {
            Py_DECREF(item);
            Py_DECREF(iter);
            PyErr_SetString(PyExc_TypeError, "Trie contains non-string");
            return NULL;
        }

        int contains = PySequence_Contains(other, item);
        if (contains < 0) {
            Py_DECREF(item);
            Py_DECREF(iter);
            return NULL;
        }

        if (contains == 0) {
            Py_DECREF(item);
            Py_DECREF(iter);
            Py_RETURN_FALSE;
        }

        Py_DECREF(item);
    }

    Py_DECREF(iter);

    if (PyErr_Occurred()) return NULL;

    Py_RETURN_TRUE;
}

static PyObject* Trie_lt(
    TrieObject* self,
    PyObject* other
) {
    PyObject* self_set =
        Trie_to_set(self);

    if (!self_set) {
        return NULL;
    }

    PyObject* result =
        PyObject_RichCompare(
            self_set,
            other,
            Py_LT
        );

    Py_DECREF(self_set);

    return result;
}

static PyObject* Trie_ge(
    TrieObject* self,
    PyObject* other
) {
    PyObject* self_set =
        Trie_to_set(self);

    if (!self_set) {
        return NULL;
    }

    PyObject* result =
        PyObject_RichCompare(
            self_set,
            other,
            Py_GE
        );

    Py_DECREF(self_set);

    return result;
}

static PyObject* Trie_gt(
    TrieObject* self,
    PyObject* other
) {
    PyObject* self_set =
        Trie_to_set(self);

    if (!self_set) {
        return NULL;
    }

    PyObject* result =
        PyObject_RichCompare(
            self_set,
            other,
            Py_GT
        );

    Py_DECREF(self_set);

    return result;
}

static PyMethodDef Trie_methods[] = {
    {
        "add",
        (PyCFunction)Trie_add,
        METH_VARARGS,
        "Add word"
    },
    {
        "remove",
        (PyCFunction)Trie_remove,
        METH_VARARGS,
        "Remove word"
    },
    {
        "discard",
        (PyCFunction)Trie_discard,
        METH_VARARGS,
        "Discard word"
    },
    {
        "pop",
        (PyCFunction)Trie_pop,
        METH_NOARGS,
        "Pop word"
    },
    {
        "clear",
        (PyCFunction)Trie_clear,
        METH_NOARGS,
        "Clear trie"
    },
    {
        "__len__",
        (PyCFunction)Trie_len,
        METH_NOARGS,
        "Length"
    },
    {
        "__contains__",
        (PyCFunction)Trie_contains,
        METH_VARARGS,
        "Contains"
    },
    {
        "__iter__",
        (PyCFunction)Trie_iter,
        METH_NOARGS,
        "Iterator"
    },
    {
        "__reversed__",
        (PyCFunction)Trie_reversed,
        METH_NOARGS,
        "Reverse iterator"
    },
    {
        "__eq__",
        (PyCFunction)Trie_eq,
        METH_O,
        "Compare"
    },
    {
        "isdisjoint",
        (PyCFunction)Trie_isdisjoint,
        METH_O,
        "Is disjoint"
    },
    {
        "__le__",
        (PyCFunction)Trie_le,
        METH_O,
        "Subset"
    },
    {
        "__lt__",
        (PyCFunction)Trie_lt,
        METH_O,
        "Proper subset"
    },
    {
        "__ge__",
        (PyCFunction)Trie_ge,
        METH_O,
        "Superset"
    },
    {
        "__gt__",
        (PyCFunction)Trie_gt,
        METH_O,
        "Proper superset"
    },
    {
        NULL,
        NULL,
        0,
        NULL
    }
};
static PyTypeObject TrieType = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name =
        "onotation.internal.trie.c_trie.Trie",
    .tp_doc =
        "C implementation of Trie",
    .tp_basicsize =
        sizeof(TrieObject),
    .tp_itemsize = 0,
    .tp_flags =
        Py_TPFLAGS_DEFAULT,
    .tp_new = Trie_new,
    .tp_init =
        (initproc)Trie_init,
    .tp_dealloc =
        (destructor)Trie_dealloc,
    .tp_methods =
        Trie_methods,
};
static struct PyModuleDef c_trie_module = {
    PyModuleDef_HEAD_INIT,
    "c_trie",
    "C implementation of Trie",
    -1,
    NULL,
};
PyMODINIT_FUNC
PyInit_c_trie(void)
{
    PyObject* m =
        PyModule_Create(
            &c_trie_module
        );

    if (m == NULL) {
        return NULL;
    }

    if (
        PyType_Ready(
            &TrieType
        ) < 0
    ) {
        Py_DECREF(m);
        return NULL;
    }

    Py_INCREF(
        &TrieType
    );

    if (
        PyModule_AddObject(
            m,
            "Trie",
            (PyObject*)&TrieType
        ) < 0
    ) {
        Py_DECREF(
            &TrieType
        );

        Py_DECREF(m);

        return NULL;
    }

    return m;
}
