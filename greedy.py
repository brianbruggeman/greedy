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


def greedy_index(materials, stride=None, dim=None, shape_only=False):
    """Converts a flat, sparse array of material id's into a mesh that
    can be sent to the gpu for display.

    stride and dimensions can be set to convert the materials from a
    flat list into a multi-dimensional list.  The indices returned will
    be a list of a pair of indices in an array.

    shape_only will ignore material id and match based on a binary data
    or no data criteria.

    >>> materials = [2, 1, 1, 1, 2, 0, 0, 2, 2, 0, 0, 2, 1, 1, 1, 2]
    >>> indices = greedy_index(materials, shape_only=True)
    >>> print indices
    [(0, 4), (7, 8), (11, 15)]
    >>> indices = greedy_index(materials)
    >>> print indices
    [(0, 0), (1, 3), (4, 4), (7, 8), (11, 11), (12, 14), (15, 15)]
    """
    return capture_row_indices(materials, shape_only)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
