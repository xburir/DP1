def get_point_indexes(lst):
    element_indices = {}
    same_elements_array = []

    for i, element in enumerate(lst):
        if element in element_indices:
            same_elements_array.append(element_indices[element])
        else:
            same_elements_array.append(i)
            element_indices[element] = i

    return same_elements_array


def remove_duplicite_points(points):


    tuple_points = []

    for pt in points:
        tuple_points.append(tuple(pt))

    pts = get_point_indexes(tuple_points)


    i = 0
    while i < len(pts):
        if pts[i] < i and pts[i] != -1:
            val = i
            i = pts[i]+1
            pts[val] = -1
            while i != val:
                pts[i] = -1
                i+=1
        else:     
            i+=1


    arrr = []
    for n in pts:
        if n != -1:
            arrr.append(tuple_points[n])


    arr = []
    for pt in arrr:
        arr.append(list(pt))

    return(arr)