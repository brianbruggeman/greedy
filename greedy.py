#!/usr/bin/env python
"""
Just an example of greedy mesh algorithm in python.
"""


def capture_row_indices(materials, shape_only=False):
    """Captures the start and stop indices of an array based on the
    contents of the array.

    shape_only provides a method to control binary gap vs no-gap as
    opposed to actual details of materials.  This should provide a close
    to optimal pairing of indices.

    >>> materials = [2, 0, 0, 1]
    >>> capture_row_indices(materials, shape_only=True)
    [(0, 0), (3, 3)]

    >>> materials = [2, 0, 0, 1]
    >>> capture_row_indices(materials)
    [(0, 0), (3, 3)]

    >>> materials = [1, 2, 2, 1]
    >>> capture_row_indices(materials, shape_only=True)
    [(0, 3)]

    >>> materials = [1, 2, 2, 1]
    >>> indices = capture_row_indices(materials)
    >>> print indices
    [(0, 0), (1, 2), (3, 3)]

    """
    last = None
    last_idx = None
    start = None
    start_idx = None
    row_data = []
    for idx, m_id in enumerate(materials):
        if m_id:
            if not last:
                start = m_id
                start_idx = idx
            elif not shape_only:
                if start != m_id:
                    row_data.append((start_idx, last_idx))
                    start = m_id
                    start_idx = idx
        else:
            if start:
                row_data.append((start_idx, last_idx))
                start = None
        last = m_id
        last_idx = idx
    if start and last:
        row_data.append((start_idx, last_idx))
    return row_data


def merge_row_indices(rows):
    """Parses each row and merges indices as they are found.

    >>> rows = [
    ...     [(0, 3)],
    ...     [(0, 0), (3, 3)],
    ...     [(0, 0), (3, 3)],
    ...     [(0, 3)]
    ... ]
    >>> merge_row_indices(rows)
    [[(0, 0), (0, 3)], [(1, 0), (2, 0)], [(1, 3), (2, 3)], [(3, 0), (3, 3)]
    """
    new_grid = []
    last_row = []
    for row_index, row in enumerate(rows):
        if row_index > 0:
            combined = set(last_row + row)
        last_row = row


def greedy_index(materials, stride=None, dim=None, shape_only=False):
    """Converts a flat, sparse array of material id's into a mesh that
    can be sent to the gpu for display.

    stride and dimensions can be set to convert the materials from a
    flat list into a multi-dimensional list.  The indices returned will
    be a list of a pair of indices in an array.

    shape_only will ignore material id and match based on a binary data
    or no data criteria.

    >>> materials = [[2, 1, 1, 2], [2, 0, 0, 2], [2, 0, 0, 2], [2, 1, 1, 2]]
    >>> greedy_index(materials, shape_only=True)
    [(0, 4), (7, 8), (11, 15)]

    >>> greedy_index(materials)
    [(0, 0), (1, 3), (4, 4), (7, 8), (11, 11), (12, 14), (15, 15)]
    """
    rows = []
    for row in materials:
        indices = capture_row_indices(materials, shape_only)
        rows.append(indices)
    grid = merge_row_indices(rows)
    return grid


if __name__ == "__main__":
    import doctest

    doctest.testmod()
